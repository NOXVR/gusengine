# backend/ingestion/parser.py
# V10 SPEC: Smart PDF parser with auto-detection (digital vs scanned)
# Routes to PyMuPDF (fast, digital) or Docling (OCR, scanned) automatically
import gc
import os
import re
import logging
import random
from enum import Enum

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    TableFormerMode,
    TableStructureOptions,
    AcceleratorOptions,
    AcceleratorDevice,
)
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.chunking import HybridChunker
try:
    from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
    _HAS_HF_TOKENIZER = True
except ImportError:
    _HAS_HF_TOKENIZER = False
from backend.shared.tokenizer import TOKENIZER, _TOKENIZER_LOCK, count_tokens

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# PDF TYPE DETECTION
# ──────────────────────────────────────────────────────────────────────────────

class PdfType(Enum):
    DIGITAL = "digital"   # Has embedded text — use PyMuPDF
    SCANNED = "scanned"   # Image-only — needs Docling + OCR
    MIXED = "mixed"       # Some pages text, some scanned — per-page routing

# Thresholds for detection
_TEXT_CHARS_THRESHOLD = 100     # Min chars on a page to count as "has text"
_DIGITAL_RATIO_THRESHOLD = 0.8  # >80% text pages = DIGITAL
_SCANNED_RATIO_THRESHOLD = 0.2  # <20% text pages = SCANNED
_SAMPLE_SIZE = 20               # Pages to sample for detection


def _detect_pdf_type(pdf_path: str) -> tuple[PdfType, int]:
    """Detect whether a PDF has embedded text or needs OCR.
    
    Samples pages (first 10 + 10 random) to determine text coverage.
    Returns (PdfType, total_page_count).
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.warning("PyMuPDF not installed — defaulting to Docling for all PDFs")
        return PdfType.SCANNED, 0

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"Cannot open PDF for detection: {e}")
        return PdfType.SCANNED, 0

    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        return PdfType.SCANNED, 0

    # Sample pages: first 10 + 10 random from the rest
    sample_indices = list(range(min(10, total_pages)))
    if total_pages > 10:
        remaining = list(range(10, total_pages))
        sample_indices.extend(random.sample(remaining, min(10, len(remaining))))

    text_pages = 0
    for idx in sample_indices:
        text = doc[idx].get_text().strip()
        if len(text) >= _TEXT_CHARS_THRESHOLD:
            text_pages += 1

    doc.close()

    ratio = text_pages / len(sample_indices)
    if ratio >= _DIGITAL_RATIO_THRESHOLD:
        pdf_type = PdfType.DIGITAL
    elif ratio <= _SCANNED_RATIO_THRESHOLD:
        pdf_type = PdfType.SCANNED
    else:
        pdf_type = PdfType.MIXED

    logger.info(
        f"PDF detection: {pdf_path} — {pdf_type.value} "
        f"({text_pages}/{len(sample_indices)} sampled pages have text, "
        f"ratio={ratio:.2f}, total={total_pages} pages)"
    )
    return pdf_type, total_pages


# ──────────────────────────────────────────────────────────────────────────────
# PYMUPDF DIGITAL PATH — High-quality text extraction + smart chunking
# ──────────────────────────────────────────────────────────────────────────────

def _extract_text_pymupdf(pdf_path: str) -> list[dict]:
    """Extract text from a digital PDF using PyMuPDF.
    
    Returns a list of page-level text blocks with metadata.
    Each entry: {"text": str, "page_number": int, "headings": [str]}
    """
    import fitz
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if not text:
            continue
        
        # Extract likely headings: lines that are short, capitalized, or bold
        headings = _detect_headings(text)
        
        pages.append({
            "text": text,
            "page_number": page_num + 1,  # 1-indexed
            "headings": headings,
        })
    
    total_doc_pages = len(doc)
    doc.close()
    logger.info(f"PyMuPDF extracted text from {len(pages)}/{total_doc_pages} pages")
    return pages


def _detect_headings(text: str) -> list[str]:
    """Detect likely section headings from a page's text.
    
    Heuristics for FSM-style documents:
    - Lines that are ALL CAPS and short (<80 chars)
    - Lines that start with chapter/section numbering (e.g., "6-12", "SECTION 4")
    """
    headings = []
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line or len(line) > 80:
            continue
        # ALL CAPS lines that aren't just numbers/symbols
        if line == line.upper() and len(line) > 3 and any(c.isalpha() for c in line):
            headings.append(line)
            continue
        # Section numbering patterns: "6-12 STARTER MOTOR", "SECTION 4", "Chapter 6"
        if re.match(r'^(\d+[-\.]\d+|SECTION\s+\d+|Chapter\s+\d+|CHAPTER\s+\d+)', line, re.IGNORECASE):
            headings.append(line)
    return headings[:3]  # Keep top 3 most likely headings


def _smart_chunk_text(pages: list[dict], source: str, max_tokens: int = 512) -> list[dict]:
    """Split extracted text into search-optimized chunks with sliding window overlap.
    
    Two-pass strategy:
    1. PASS 1 — Build primary chunks at paragraph boundaries (max_tokens limit)
    2. PASS 2 — Create overlap chunks between consecutive primary chunks
       (tail of chunk N + head of chunk N+1, capped at max_tokens)
    
    The overlap pass ensures no content falls in a boundary gap. If a torque spec
    sentence sits right at the split between two primary chunks, the overlap chunk
    captures both sides together — acting as retrieval insurance.
    
    Primary chunks are untouched. Overlap chunks are purely additive.
    Target: ~4-5 chunks per page (matching Docling's HybridChunker baseline).
    """
    # ── PASS 1: Build primary chunks (same logic as before) ──
    primary_chunks = []
    
    for page_data in pages:
        page_text = page_data["text"]
        page_num = page_data["page_number"]
        page_headings = page_data["headings"]
        
        # Split into paragraphs: double newlines, or heading-like lines
        paragraphs = _split_into_paragraphs(page_text)
        
        current_text = ""
        current_tokens = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_tokens = count_tokens(para)
            
            # If a single paragraph exceeds max_tokens, split it by sentences
            if para_tokens > max_tokens:
                # Flush current buffer first
                if current_text.strip():
                    primary_chunks.append({
                        "text": current_text.strip(),
                        "source": source,
                        "page_numbers": [page_num],
                        "headings": page_headings,
                        "token_count": current_tokens,
                    })
                    current_text = ""
                    current_tokens = 0
                
                # Split long paragraph into sentence-level chunks
                sentence_chunks = _split_long_text(para, max_tokens)
                for sc in sentence_chunks:
                    sc_tokens = count_tokens(sc)
                    primary_chunks.append({
                        "text": sc,
                        "source": source,
                        "page_numbers": [page_num],
                        "headings": page_headings,
                        "token_count": sc_tokens,
                    })
                continue
            
            # Would adding this paragraph exceed the limit?
            if current_tokens + para_tokens > max_tokens and current_text.strip():
                primary_chunks.append({
                    "text": current_text.strip(),
                    "source": source,
                    "page_numbers": [page_num],
                    "headings": page_headings,
                    "token_count": current_tokens,
                })
                current_text = ""
                current_tokens = 0
            
            current_text += ("\n\n" if current_text else "") + para
            current_tokens += para_tokens
        
        # Flush remaining text for this page
        if current_text.strip():
            primary_chunks.append({
                "text": current_text.strip(),
                "source": source,
                "page_numbers": [page_num],
                "headings": page_headings,
                "token_count": current_tokens,
            })
    
    # ── PASS 2: Create overlap chunks between consecutive primary chunks ──
    overlap_chunks = _build_overlap_chunks(primary_chunks, max_tokens)
    
    # Combine: all primary chunks + all overlap chunks
    all_chunks = primary_chunks + overlap_chunks
    logger.info(
        f"SmartChunk: {len(primary_chunks)} primary + "
        f"{len(overlap_chunks)} overlap = {len(all_chunks)} total chunks"
    )
    return all_chunks


def _build_overlap_chunks(primary_chunks: list[dict], max_tokens: int) -> list[dict]:
    """Build overlap chunks from consecutive primary chunk pairs.
    
    For each pair (chunk_i, chunk_i+1) that share the same source:
    - Take the last ~40% of chunk_i's text
    - Take the first ~40% of chunk_i+1's text
    - Combine them into an overlap chunk (capped at max_tokens)
    - The overlap chunk inherits page numbers from both chunks
    
    This ensures content at chunk boundaries always has a dedicated
    chunk where it appears in full context — not split across two.
    """
    if len(primary_chunks) < 2:
        return []
    
    overlaps = []
    
    for i in range(len(primary_chunks) - 1):
        chunk_a = primary_chunks[i]
        chunk_b = primary_chunks[i + 1]
        
        # Only overlap chunks from the same source file
        if chunk_a["source"] != chunk_b["source"]:
            continue
        
        # Get the tail of chunk A and head of chunk B
        text_a = chunk_a["text"]
        text_b = chunk_b["text"]
        
        # Split into sentences for clean boundaries
        sentences_a = re.split(r'(?<=[.!?])\s+', text_a)
        sentences_b = re.split(r'(?<=[.!?])\s+', text_b)
        
        # Take roughly the last 40% of sentences from A
        tail_count = max(1, len(sentences_a) * 2 // 5)
        tail_sentences = sentences_a[-tail_count:]
        
        # Take roughly the first 40% of sentences from B
        head_count = max(1, len(sentences_b) * 2 // 5)
        head_sentences = sentences_b[:head_count]
        
        # Combine
        overlap_text = " ".join(tail_sentences) + "\n\n" + " ".join(head_sentences)
        overlap_text = overlap_text.strip()
        
        if not overlap_text:
            continue
        
        overlap_tokens = count_tokens(overlap_text)
        
        # Cap at max_tokens — trim from the edges if needed
        if overlap_tokens > max_tokens:
            # Trim sentences from both ends proportionally
            while overlap_tokens > max_tokens and (len(tail_sentences) > 1 or len(head_sentences) > 1):
                if len(tail_sentences) > len(head_sentences) and len(tail_sentences) > 1:
                    tail_sentences = tail_sentences[1:]  # Drop oldest sentence from tail
                elif len(head_sentences) > 1:
                    head_sentences = head_sentences[:-1]  # Drop newest sentence from head
                else:
                    break
                overlap_text = " ".join(tail_sentences) + "\n\n" + " ".join(head_sentences)
                overlap_tokens = count_tokens(overlap_text.strip())
            overlap_text = overlap_text.strip()
            overlap_tokens = count_tokens(overlap_text)
        
        # Skip tiny overlaps that add no value
        if overlap_tokens < 30:
            continue
        
        # Merge page numbers from both chunks
        page_numbers = sorted(set(chunk_a["page_numbers"] + chunk_b["page_numbers"]))
        
        # Merge headings (prefer chunk B's headings as they're "entering" that section)
        headings = chunk_b["headings"] if chunk_b["headings"] else chunk_a["headings"]
        
        overlaps.append({
            "text": overlap_text,
            "source": chunk_a["source"],
            "page_numbers": page_numbers,
            "headings": headings,
            "token_count": overlap_tokens,
        })
    
    return overlaps


def _split_into_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs using multiple heuristics.
    
    Splits on:
    - Double newlines (standard paragraph break)
    - Lines that look like headings (ALL CAPS followed by content)
    - Numbered/lettered list items
    """
    # First split on double newlines
    blocks = re.split(r'\n\s*\n', text)
    
    # Further split blocks that contain heading-like transitions
    paragraphs = []
    for block in blocks:
        lines = block.split('\n')
        if len(lines) <= 2:
            paragraphs.append(block)
            continue
        
        # Look for heading-like lines within the block
        current = []
        for line in lines:
            stripped = line.strip()
            # If this line looks like a heading and we have accumulated text, split here
            if (stripped == stripped.upper() and len(stripped) > 3 
                and any(c.isalpha() for c in stripped) and len(stripped) < 60
                and current):
                paragraphs.append('\n'.join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            paragraphs.append('\n'.join(current))
    
    return paragraphs


def _split_long_text(text: str, max_tokens: int) -> list[str]:
    """Split text that exceeds max_tokens into sentence-level chunks."""
    # Split by sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current = ""
    current_tokens = 0
    
    for sent in sentences:
        sent_tokens = count_tokens(sent)
        if current_tokens + sent_tokens > max_tokens and current:
            chunks.append(current.strip())
            current = ""
            current_tokens = 0
        current += (" " if current else "") + sent
        current_tokens += sent_tokens
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks


def _parse_digital_pdf(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a digital PDF using PyMuPDF with quality chunking.
    
    Fast path for PDFs with embedded text. Produces chunks at ~4+ per page
    with heading hierarchy and token-precise sizing.
    """
    source = _resolve_source(pdf_path)
    pages = _extract_text_pymupdf(pdf_path)
    
    if not pages:
        raise IngestionError(f"PyMuPDF extracted no text from {pdf_path}")
    
    chunks = _smart_chunk_text(pages, source, max_tokens)
    
    if not chunks:
        raise IngestionError(f"No chunks produced from {pdf_path}")
    
    total_pages = _get_pdf_page_count(pdf_path)
    ratio = len(chunks) / max(len(pages), 1)
    logger.info(
        f"PyMuPDF+SmartChunk: {len(chunks)} chunks from {len(pages)} text pages "
        f"({total_pages} total) — {ratio:.1f} chunks/page"
    )
    return chunks


# ──────────────────────────────────────────────────────────────────────────────
# DOCLING SCANNED PATH — OCR + HybridChunker (original path)
# ──────────────────────────────────────────────────────────────────────────────

def _resolve_artifacts_path():
    """Resolve Docling model artifacts path."""
    env_path = os.environ.get("DOCLING_MODELS_PATH")
    if env_path and os.path.isdir(env_path):
        logger.info(f"Using Docling models from env: {env_path}")
        return env_path
    docker_default = "/app/models/docling-models"
    if os.path.isdir(docker_default):
        logger.info(f"Using Docling models from Docker default: {docker_default}")
        return docker_default
    logger.info("No pre-cached Docling models found — will auto-download on first use")
    return None


def _create_converter():
    """Create memory-optimized Docling converter with OCR enabled for scanned PDFs."""
    artifacts_path = _resolve_artifacts_path()
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        do_ocr=True,
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=False,
        ),
        do_table_structure=True,
        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
        accelerator_options=AcceleratorOptions(
            num_threads=1,
            device=AcceleratorDevice.CPU,
        ),
        generate_parsed_pages=False,
    )
    return DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend,
            )
        }
    )


class IngestionError(Exception):
    """Raised when a PDF fails to parse or chunk. Caller should quarantine."""
    pass


def _get_pdf_page_count(pdf_path: str) -> int:
    """Get total page count using PyPdfium2 (lightweight)."""
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        count = len(pdf)
        pdf.close()
        return count
    except Exception:
        return 0


def _build_chunker(max_tokens: int):
    """Build a HybridChunker with appropriate tokenizer wrapping."""
    class LockedTokenizer:
        def __init__(self, tok): self.tok = tok
        def encode(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.encode(text, **kwargs)
        def decode(self, ids, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.decode(ids, **kwargs)
        def __getattr__(self, name):
            with _TOKENIZER_LOCK: return getattr(self.tok, name)
        def tokenize(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.tokenize(text, **kwargs)
        def __call__(self, *args, **kwargs):
            with _TOKENIZER_LOCK: return self.tok(*args, **kwargs)

    if _HAS_HF_TOKENIZER:
        return HybridChunker(
            tokenizer=HuggingFaceTokenizer(
                tokenizer=TOKENIZER,
                max_tokens=max_tokens,
            ),
            max_tokens=max_tokens,
            merge_peers=True,
        )
    else:
        return HybridChunker(
            tokenizer=TOKENIZER,
            max_tokens=max_tokens,
            merge_peers=True,
        )


def _resolve_source(pdf_path: str) -> str:
    """Resolve source path for chunk metadata."""
    source = os.path.basename(pdf_path)
    for prefix in ["/app/pdfs/", "/app/storage/pdfs/", "/workspace/GusEngine/storage/pdfs/"]:
        if prefix in pdf_path:
            source = pdf_path.split(prefix, 1)[-1]
            break
    return source


def _parse_scanned_pdf(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a scanned PDF using Docling + OCR + HybridChunker.
    
    Original Docling path for PDFs that need OCR.
    """
    source = _resolve_source(pdf_path)
    chunker = _build_chunker(max_tokens)
    total_pages = _get_pdf_page_count(pdf_path)
    logger.info(f"Docling OCR path: {pdf_path} ({total_pages} pages)")

    converter = _create_converter()
    try:
        result = converter.convert(pdf_path)
    except Exception as e:
        logger.error(f"DOCLING PARSE FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Failed to parse {pdf_path}: {e}") from e

    doc = result.document
    if doc is None:
        raise IngestionError(f"Docling returned empty document for {pdf_path}")

    chunks = []
    try:
        chunk_iter = chunker.chunk(doc)
        for chunk in chunk_iter:
            text = chunk.text
            if not text or not text.strip():
                continue
            token_count = count_tokens(text)
            page_numbers = sorted(set(
                item.prov[0].page_no
                for item in chunk.meta.doc_items
                if item.prov
            )) if chunk.meta.doc_items else []
            headings = list(chunk.meta.headings or [])
            chunks.append({
                "text": text,
                "source": source,
                "page_numbers": page_numbers,
                "headings": headings,
                "token_count": token_count,
            })
    except Exception as e:
        logger.error(f"CHUNKER FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Chunking failed for {pdf_path}: {e}") from e

    del converter, result, doc
    gc.collect()

    if not chunks:
        raise IngestionError(f"No chunks extracted from {pdf_path} — likely blank/corrupt PDF")

    logger.info(f"Docling: {len(chunks)} chunks from {total_pages} pages")
    return chunks


# ──────────────────────────────────────────────────────────────────────────────
# PUBLIC API — Smart routing
# ──────────────────────────────────────────────────────────────────────────────

def parse_and_chunk(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a PDF with automatic detection and optimal routing.

    DIGITAL PDFs → PyMuPDF (fast text extraction + smart chunking)
    SCANNED PDFs → Docling (OCR + HybridChunker)
    MIXED PDFs   → PyMuPDF for text (best effort, may miss image-only pages)

    Returns list of chunks with metadata.
    Raises IngestionError if parsing fails.
    """
    import traceback
    
    logger.info(f"parse_and_chunk called for: {pdf_path}")
    logger.info(f"  File exists: {os.path.isfile(pdf_path)}")
    if os.path.isfile(pdf_path):
        logger.info(f"  File size: {os.path.getsize(pdf_path)} bytes")
    
    pdf_type, total_pages = _detect_pdf_type(pdf_path)
    
    if pdf_type == PdfType.DIGITAL or pdf_type == PdfType.MIXED:
        # Digital or mixed: use PyMuPDF fast path
        logger.info(f"Routing {pdf_path} to PyMuPDF path ({pdf_type.value})")
        try:
            return _parse_digital_pdf(pdf_path, max_tokens)
        except IngestionError:
            if pdf_type == PdfType.MIXED:
                logger.warning(f"PyMuPDF failed on mixed PDF, falling back to Docling: {pdf_path}")
                return _parse_scanned_pdf(pdf_path, max_tokens)
            raise
        except Exception as e:
            logger.error(f"UNEXPECTED ERROR in PyMuPDF path: {e}\n{traceback.format_exc()}")
            raise IngestionError(f"PyMuPDF failed for {pdf_path}: {e}") from e
    else:
        # Scanned: use Docling OCR path
        logger.info(f"Routing {pdf_path} to Docling OCR path ({pdf_type.value})")
        return _parse_scanned_pdf(pdf_path, max_tokens)

