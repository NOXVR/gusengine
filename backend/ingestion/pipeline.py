# backend/ingestion/pipeline.py
# V10 SPEC: Full ingestion pipeline with semaphores, circuit breaker, UUID5
import asyncio
import os
import threading
import time
import uuid
from backend.ingestion.parser import parse_and_chunk, IngestionError
from backend.embedding.client import embed_text
from backend.ingestion.qdrant_setup import index_chunk
from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)

# AUDIT FIX (DT-P2-04): Limit concurrent ingestion workers to prevent OOM.
# Without a semaphore, asyncio.to_thread spawns ~32 concurrent Docling/EasyOCR workers,
# each consuming ~2GB RAM. Limit to 2 concurrent jobs.
# AUDIT FIX (DT-P10-01): Deferred initialization — asyncio.Semaphore() at module scope
# crashes Python 3.10+ because no event loop exists during import.
_INGEST_SEMAPHORE: asyncio.Semaphore | None = None


async def _get_ingest_semaphore() -> asyncio.Semaphore:
    global _INGEST_SEMAPHORE
    if _INGEST_SEMAPHORE is None:
        _INGEST_SEMAPHORE = asyncio.Semaphore(1)  # THROTTLE FIX: 1 concurrent PDF to prevent Qdrant overload
    return _INGEST_SEMAPHORE


# AUDIT FIX (P3-04): Rate-limit concurrent TEI embedding requests.
# AUDIT FIX (DT-P10-01): Deferred initialization, matching ingest semaphore pattern.
_EMBED_SEMAPHORE: asyncio.Semaphore | None = None


async def _get_embed_semaphore() -> asyncio.Semaphore:
    global _EMBED_SEMAPHORE
    if _EMBED_SEMAPHORE is None:
        _EMBED_SEMAPHORE = asyncio.Semaphore(4)  # THROTTLE FIX: Reduced from 8 to 4 to ease Qdrant pressure
    return _EMBED_SEMAPHORE


# AUDIT FIX (P5-10): Path constant for failure manifest.
# Must match Docker volume mount (./storage/extracted:/app/extracted).
# For RunPod: use /workspace/GusEngine/storage/extracted/
FAILURE_MANIFEST_PATH = os.environ.get(
    "FAILURE_MANIFEST_PATH",
    "/app/extracted/.ingest_failures.log"
)
# AUDIT FIX (P10-20): Thread-safe manifest writes. With INGEST_SEMAPHORE=2,
# two concurrent ingestion failures can race on append.
_manifest_lock = threading.Lock()


async def ingest_pdf(pdf_path: str, client: QdrantClient) -> int:
    """Full ingestion pipeline: parse → embed → index.

    Returns number of chunks indexed.
    Raises IngestionError if parsing fails (caller should quarantine).

    AUDIT FIX (DT-3): Uses deterministic UUID5 based on (pdf_path, chunk_index)
    so that re-ingesting the same PDF produces the same IDs (idempotent upsert),
    but different PDFs never collide.
    """
    # AUDIT FIX: parse_and_chunk is synchronous and CPU-bound.
    # Must dispatch to threadpool to avoid deadlocking the asyncio event loop.
    # AUDIT FIX (DT-P2-04): Acquire semaphore to limit concurrent OCR workers.
    async with (await _get_ingest_semaphore()):
        chunks = await asyncio.to_thread(parse_and_chunk, pdf_path)

    if not chunks:
        # AUDIT FIX (DT-5b): Zero extractable text = silent failure.
        raise IngestionError(f"No chunks extracted from {pdf_path} — likely blank/corrupt PDF")

    # AUDIT FIX (P5-01): Track actual indexed vs failed counts.
    indexed_count = 0
    failed_count = 0

    # AUDIT FIX (P7-04): Circuit breaker for consecutive failures.
    # When TEI/Qdrant dies, ConnectError returns instantly (~1ms). Without a
    # circuit breaker, the for-loop burns through all remaining chunks at CPU
    # speed — discarding hours of parsed OCR data in milliseconds.
    consecutive_failures = 0
    for i, chunk in enumerate(chunks):
        # AUDIT FIX (DT-3): Deterministic UUID from (path, index).
        # AUDIT FIX (P2-08): Use str() not .hex — Qdrant needs hyphenated UUID format.
        chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{pdf_path}_{i}"))

        # AUDIT FIX (P4-08): Per-chunk error handling for embed+index.
        try:
            # AUDIT FIX (P3-04): Rate-limit TEI requests
            async with (await _get_embed_semaphore()):
                dense, sparse = await embed_text(chunk["text"])
            sparse_dict = sparse or {"indices": [], "values": []}

            # index_chunk() uses synchronous client.upsert() — dispatch to threadpool
            await asyncio.to_thread(
                index_chunk,
                client=client,
                chunk=chunk,
                chunk_id=chunk_id,
                dense_vector=dense,
                sparse_vector=sparse_dict,
            )
            indexed_count += 1
            consecutive_failures = 0  # reset on success
            # THROTTLE FIX: Sleep 250ms between upserts to prevent Qdrant deadlock.
            # Without this, hundreds of rapid-fire upserts overwhelm Qdrant's WAL
            # and cause it to hang indefinitely (observed at ~1100 points).
            await asyncio.sleep(0.25)
        except Exception as e:
            failed_count += 1
            consecutive_failures += 1
            logger.warning(f"Chunk {i}/{len(chunks)} failed for {pdf_path}: {e} — skipping")
            # AUDIT FIX (P7-04): Circuit breaker — 5 consecutive failures means
            # the downstream service (TEI/Qdrant) is dead, not flaky.
            if consecutive_failures >= 5:
                raise IngestionError(
                    f"Circuit breaker: {consecutive_failures} consecutive failures at "
                    f"chunk {i}/{len(chunks)} for {pdf_path}. TEI or Qdrant likely down."
                )
            continue

    # AUDIT FIX (P5-01): Report actual indexed count
    logger.info(
        f"Indexed {indexed_count}/{len(chunks)} chunks from {pdf_path}"
        f"{f' ({failed_count} failed)' if failed_count else ''}"
    )
    # AUDIT FIX (P6-03): Write PARTIAL manifest entry when some chunks succeeded but some failed
    if failed_count > 0 and indexed_count > 0:
        logger.warning(
            f"PARTIAL INGESTION: {pdf_path} — {failed_count}/{len(chunks)} chunks failed. "
            f"Re-ingest after resolving TEI/Qdrant issues."
        )
        with _manifest_lock:
            with open(FAILURE_MANIFEST_PATH, "a") as f:
                f.write(f"{pdf_path}\tPARTIAL: {indexed_count}/{len(chunks)} indexed, {failed_count} failed\n")
    # AUDIT FIX (DT-P5-04): If EVERY chunk failed, raise IngestionError
    if indexed_count == 0 and len(chunks) > 0:
        raise IngestionError(
            f"All {len(chunks)} chunks failed to index for {pdf_path} — "
            f"TEI or Qdrant may be down."
        )
    return indexed_count


# AUDIT FIX (P2-06): Background task wrapper with error handling.
# When called via FastAPI BackgroundTasks, exceptions are silently swallowed.
async def ingest_pdf_background(pdf_path: str, client: QdrantClient):
    """Wrapper for BackgroundTask execution with error handling."""
    try:
        count = await ingest_pdf(pdf_path, client)
        logger.info(f"Background ingestion complete: {pdf_path} ({count} chunks)")
    except IngestionError as e:
        logger.error(f"INGESTION FAILED (quarantine candidate): {pdf_path} — {e}")
        with _manifest_lock:
            with open(FAILURE_MANIFEST_PATH, "a") as f:
                f.write(f"{pdf_path}\t{e}\n")
    except Exception as e:
        logger.error(f"UNEXPECTED INGESTION ERROR: {pdf_path} — {e}", exc_info=True)
        # AUDIT FIX (P3-09): Also log unexpected errors to failure manifest
        with _manifest_lock:
            with open(FAILURE_MANIFEST_PATH, "a") as f:
                f.write(f"{pdf_path}\tUNEXPECTED: {e}\n")
