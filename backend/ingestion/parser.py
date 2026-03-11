# backend/ingestion/parser.py
# V10 SPEC: Docling PDF parser with OCR support and thread-safe tokenization
# MEMORY OPT: Page-windowed processing, PyPdfiumDocumentBackend, single-threaded CPU
import gc
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
    from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer  # AUDIT FIX (DT-7)
    _HAS_HF_TOKENIZER = True
except ImportError:
    _HAS_HF_TOKENIZER = False
from backend.shared.tokenizer import TOKENIZER, _TOKENIZER_LOCK, count_tokens  # AUDIT FIX (P3-13 + P11-14)
import os
import logging

logger = logging.getLogger(__name__)

# MEMORY OPT: Process PDFs in page windows to limit peak RAM.
# 20 pages keeps Docling+EasyOCR under ~3-4GB additional RAM.
PAGE_WINDOW_SIZE = int(os.environ.get("DOCLING_PAGE_WINDOW", "20"))


def _resolve_artifacts_path():
    """Resolve Docling model artifacts path.
    
    Priority: DOCLING_MODELS_PATH env var → Docker default → None (auto-download).
    In Docker (air-gapped), uses /app/models/docling-models with pre-cached models.
    """
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
    """Create memory-optimized Docling converter with OCR enabled for scanned PDFs.
    
    MEMORY OPT: Uses PyPdfiumDocumentBackend (lighter than default), single-threaded
    CPU inference (AcceleratorOptions), and generate_parsed_pages=False to prevent
    retaining intermediate page data in memory.
    """
    artifacts_path = _resolve_artifacts_path()
    pipeline_options = PdfPipelineOptions(
        artifacts_path=artifacts_path,
        do_ocr=True,  # CRITICAL: Must be True for scanned FSM PDFs
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=False,  # OCR on CPU — no GPU on Hetzner VPS
        ),
        do_table_structure=True,
        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
        # MEMORY OPT: Single-threaded model inference across the pipeline
        accelerator_options=AcceleratorOptions(
            num_threads=1,
            device=AcceleratorDevice.CPU,
        ),
        # MEMORY OPT: Don't retain intermediate parsed page representations
        generate_parsed_pages=False,
    )
    return DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend,  # MEMORY OPT: lighter PDF backend
            )
        }
    )


class IngestionError(Exception):
    """Raised when a PDF fails to parse or chunk. Caller should quarantine."""
    pass


def _get_pdf_page_count(pdf_path: str) -> int:
    """Get total page count using PyPdfium2 (lightweight, no model loading)."""
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(pdf_path)
        count = len(pdf)
        pdf.close()
        return count
    except Exception:
        # Fallback: let Docling handle it as a single window
        return 0


def _build_chunker(max_tokens: int):
    """Build a HybridChunker with appropriate tokenizer wrapping."""
    # AUDIT FIX (P7-01): Wrap TOKENIZER for Docling with lock protection.
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
        # Fallback: pass raw TOKENIZER directly — LockedTokenizer wrapper fails
        # Pydantic isinstance(PreTrainedTokenizerBase) validation in newer Docling.
        # Thread safety is guaranteed by the ingest semaphore (max 1 concurrent job).
        return HybridChunker(
            tokenizer=TOKENIZER,
            max_tokens=max_tokens,
            merge_peers=True,
        )


def _resolve_source(pdf_path: str) -> str:
    """Resolve source path for chunk metadata.
    
    AUDIT FIX (DT-P9-03): Preserve relative path, not just basename.
    """
    source = os.path.basename(pdf_path)
    for prefix in ["/app/pdfs/", "/app/storage/pdfs/", "/workspace/GusEngine/storage/pdfs/"]:
        if prefix in pdf_path:
            source = pdf_path.split(prefix, 1)[-1]
            break
    return source


def _process_window(pdf_path: str, page_range: tuple[int, int] | None,
                    chunker, source: str, window_label: str) -> list[dict]:
    """Process a single page window through Docling and return chunks.
    
    Args:
        page_range: 1-indexed inclusive tuple (start, end) or None for full document.
    
    MEMORY OPT: Creates and destroys the converter per window to force
    memory release of Docling's internal document representation.
    """
    if page_range:
        logger.info(f"  {window_label}: Parsing pages {page_range[0]}-{page_range[1]}...")
    else:
        logger.info(f"  {window_label}: Parsing full document...")

    converter = _create_converter()
    try:
        if page_range:
            result = converter.convert(pdf_path, page_range=page_range)
        else:
            result = converter.convert(pdf_path)
    except Exception as e:
        label = f"pages {page_range[0]}-{page_range[1]}" if page_range else "full"
        logger.error(f"DOCLING PARSE FAILURE: {pdf_path} {label} — {e}")
        raise IngestionError(f"Failed to parse {pdf_path} {label}: {e}") from e

    doc = result.document
    if doc is None:
        label = f"pages {page_range[0]}-{page_range[1]}" if page_range else "full"
        logger.warning(f"DOCLING EMPTY WINDOW: {pdf_path} {label} — skipping")
        return []

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
        label = f"pages {page_range[0]}-{page_range[1]}" if page_range else "full"
        logger.error(f"CHUNKER FAILURE: {pdf_path} {label} — {e}")
        raise IngestionError(f"Chunking failed for {pdf_path} {label}: {e}") from e

    logger.info(f"  {window_label}: Extracted {len(chunks)} chunks")

    # MEMORY OPT: Explicitly delete converter and doc to release Docling internals
    del converter, result, doc
    gc.collect()

    return chunks


def parse_and_chunk(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a PDF with Docling and chunk using HybridChunker.

    MEMORY OPT: Processes the PDF in page windows (default 20 pages at a time)
    to limit peak RAM. Each window creates/destroys its own converter instance,
    forcing memory release of Docling's internal representations between windows.

    Returns list of chunks with metadata:
    - text: chunk text content
    - source: relative path under storage/pdfs/
    - page_numbers: list of page numbers this chunk spans
    - headings: hierarchical heading path
    - token_count: exact token count via native tokenizer

    Raises:
        IngestionError: If parsing fails. Caller should quarantine.
    """
    source = _resolve_source(pdf_path)
    chunker = _build_chunker(max_tokens)
    total_pages = _get_pdf_page_count(pdf_path)

    # Small PDFs or unknown page count: process in one shot (no page_range filter)
    if total_pages <= PAGE_WINDOW_SIZE or total_pages == 0:
        logger.info(f"Parsing {pdf_path} ({total_pages} pages) in single pass")
        return _process_window(pdf_path, None,
                              chunker, source, "single-pass")

    # Large PDFs: process in page windows
    num_windows = (total_pages + PAGE_WINDOW_SIZE - 1) // PAGE_WINDOW_SIZE
    logger.info(f"Parsing {pdf_path} ({total_pages} pages) in {num_windows} windows of {PAGE_WINDOW_SIZE}")

    all_chunks = []
    for window_idx in range(num_windows):
        # Docling page_range is 1-indexed inclusive: (start_page, end_page)
        page_start = window_idx * PAGE_WINDOW_SIZE + 1
        page_end = min(page_start + PAGE_WINDOW_SIZE - 1, total_pages)
        window_label = f"[{window_idx+1}/{num_windows}]"

        window_chunks = _process_window(
            pdf_path, (page_start, page_end),
            chunker, source, window_label
        )
        all_chunks.extend(window_chunks)

    if not all_chunks:
        raise IngestionError(f"No chunks extracted from {pdf_path} — likely blank/corrupt PDF")

    logger.info(f"Total: {len(all_chunks)} chunks from {total_pages} pages")
    return all_chunks
