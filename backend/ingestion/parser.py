# backend/ingestion/parser.py
# V10 SPEC: Docling PDF parser with OCR support and thread-safe tokenization
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    TableFormerMode,
    TableStructureOptions,
)
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


def _resolve_artifacts_path():
    """Resolve Docling model artifacts path.
    
    Priority: DOCLING_MODELS_PATH env var → Docker default → None (auto-download).
    On RunPod (no pre-cached models), returns None so Docling downloads on first use.
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


def create_converter():
    """Create Docling converter with OCR enabled for scanned PDFs."""
    pipeline_options = PdfPipelineOptions(
        # AUDIT FIX (DT-P11-02): Explicit offline artifacts path for TableFormer.
        # Without this, Docling attempts HF Hub download blocked by HF_HUB_OFFLINE=1.
        # For RunPod: use env var, fallback to default Docker path, or None to auto-download.
        artifacts_path=_resolve_artifacts_path(),
        do_ocr=True,  # CRITICAL: Must be True for scanned FSM PDFs
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=False,  # OCR on CPU to preserve GPU VRAM for LLM
        ),
        do_table_structure=True,
        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
    )
    return DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(pipeline_options=pipeline_options)
        }
    )


class IngestionError(Exception):
    """Raised when a PDF fails to parse or chunk. Caller should quarantine."""
    pass


def parse_and_chunk(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a PDF with Docling and chunk using HybridChunker.

    Returns list of chunks with metadata:
    - text: chunk text content
    - source: relative path under storage/pdfs/ (e.g. "brakes/manual.pdf", not just "manual.pdf")
    - page_numbers: list of page numbers this chunk spans
    - headings: hierarchical heading path
    - token_count: exact token count via native tokenizer

    Raises:
        IngestionError: If parsing fails after logging. Caller should
        quarantine the file and continue with the next PDF.
    """
    try:
        converter = create_converter()
        result = converter.convert(pdf_path)
    except Exception as e:
        logger.error(f"DOCLING PARSE FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Failed to parse {pdf_path}: {e}") from e

    doc = result.document
    if doc is None:
        logger.error(f"DOCLING EMPTY RESULT: {pdf_path} — converter returned None document")
        raise IngestionError(f"Docling returned empty document for {pdf_path}")

    # AUDIT FIX (P7-01): Wrap TOKENIZER for Docling with lock protection.
    # Docling's HybridChunker calls tokenizer.encode() internally on its own
    # thread during parse_and_chunk (dispatched via asyncio.to_thread). Without
    # the lock, concurrent chat handler tokenization can corrupt the
    # trust_remote_code Python state in Qwen2.5's tokenizer.
    class LockedTokenizer:
        def __init__(self, tok): self.tok = tok
        def encode(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.encode(text, **kwargs)
        # AUDIT FIX (P9-11): Add decode() with lock + __getattr__ for forward compat.
        def decode(self, ids, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.decode(ids, **kwargs)
        # AUDIT FIX (P10-07): __getattr__ must also acquire the lock.
        def __getattr__(self, name):
            with _TOKENIZER_LOCK: return getattr(self.tok, name)
        # AUDIT FIX (DT-P10-05): Explicit wrappers for methods Docling calls through
        # HuggingFaceTokenizer. __getattr__ locks the attribute access but not the
        # subsequent method call — these wrappers lock the entire call.
        def tokenize(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.tokenize(text, **kwargs)
        def __call__(self, *args, **kwargs):
            with _TOKENIZER_LOCK: return self.tok(*args, **kwargs)

    if _HAS_HF_TOKENIZER:
        # Pass raw TOKENIZER — HuggingFaceTokenizer validates isinstance(PreTrainedTokenizerBase)
        # via Pydantic. LockedTokenizer wrapper fails this check. Thread-safety is handled
        # by the ingest semaphore limiting to 2 concurrent parse_and_chunk calls.
        chunker = HybridChunker(
            tokenizer=HuggingFaceTokenizer(
                tokenizer=TOKENIZER,
                max_tokens=max_tokens,
            ),
            max_tokens=max_tokens,
            merge_peers=True,
        )
    else:
        # Fallback: pass LockedTokenizer directly (docling versions without HuggingFaceTokenizer)
        chunker = HybridChunker(
            tokenizer=LockedTokenizer(TOKENIZER),
            max_tokens=max_tokens,
            merge_peers=True,
        )

    # AUDIT FIX (DT-P10-06): chunker.chunk(doc) returns a lazy generator.
    # Docling parsing errors fire during iteration, NOT creation. The try/except
    # must wrap the iteration loop to route errors to IngestionError quarantine.
    try:
        chunk_iter = chunker.chunk(doc)  # lazy generator — avoids OOM on large PDFs
        chunks = []
        for chunk in chunk_iter:
            text = chunk.text
            if not text or not text.strip():
                continue  # Skip empty chunks (OCR failures on blank pages)
            token_count = count_tokens(text)  # AUDIT FIX (P7-01): thread-safe

            # Extract page numbers from chunk metadata
            page_numbers = sorted(set(
                item.prov[0].page_no
                for item in chunk.meta.doc_items
                if item.prov
            )) if chunk.meta.doc_items else []

            # Extract heading hierarchy
            headings = list(chunk.meta.headings or [])

            # AUDIT FIX (DT-P9-03): Preserve relative path, not just basename.
            # os.path.basename strips folder structure, causing cross-source collision.
            # Detect both /app/pdfs/ (Docker) and /workspace/.../pdfs/ (RunPod) patterns.
            source = os.path.basename(pdf_path)
            for prefix in ["/app/pdfs/", "/workspace/GusEngine/storage/pdfs/"]:
                if prefix in pdf_path:
                    source = pdf_path.split(prefix, 1)[-1]
                    break

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

    return chunks
