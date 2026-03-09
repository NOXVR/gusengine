# backend/routes/admin.py
# Admin endpoints for corpus maintenance operations.
import asyncio
import logging
import time
from fastapi import APIRouter, BackgroundTasks

from backend.embedding.client import embed_text
from backend.ingestion.qdrant_setup import index_chunk
from backend.shared.clients import qdrant_ingest_client
from backend.routes.vehicle import get_vehicle

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])

# Track re-embedding status
_reembed_status = {"running": False, "processed": 0, "total": 0, "errors": 0, "message": "idle"}


async def _reembed_collection(vehicle_id: str):
    """Re-embed all chunks in a collection using the local TEI server.
    
    This fixes embedding model mismatch between environments by ensuring
    document vectors and query vectors are produced by the same model.
    """
    global _reembed_status
    v = get_vehicle(vehicle_id)
    if not v:
        _reembed_status = {"running": False, "processed": 0, "total": 0, "errors": 0,
                           "message": f"Unknown vehicle: {vehicle_id}"}
        return

    collection = v["collection"]
    _reembed_status = {"running": True, "processed": 0, "total": 0, "errors": 0,
                       "message": f"Starting re-embed for {collection}"}

    try:
        # Get total count
        info = qdrant_ingest_client.get_collection(collection)
        total = info.points_count
        _reembed_status["total"] = total
        logger.info(f"Re-embedding {total} points in {collection}")

        # Scroll through all points
        offset = None
        processed = 0
        errors = 0
        start = time.time()

        while True:
            result = qdrant_ingest_client.scroll(
                collection_name=collection,
                limit=10,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )
            batch, next_offset = result

            if not batch:
                break

            for point in batch:
                pid = point.id
                payload = point.payload
                text = payload.get("text", "")

                if not text.strip():
                    processed += 1
                    _reembed_status["processed"] = processed
                    continue

                try:
                    # Re-embed using local TEI
                    dense, sparse = await embed_text(text)

                    # Build chunk dict for index_chunk
                    chunk = {
                        "text": payload.get("text", ""),
                        "source": payload.get("source", ""),
                        "page_numbers": payload.get("page_numbers", []),
                        "headings": payload.get("headings", []),
                        "token_count": payload.get("token_count", 0),
                    }

                    sparse_dict = sparse if sparse else {"indices": [], "values": []}

                    # Upsert with new vectors (same ID, same payload)
                    await asyncio.to_thread(
                        index_chunk,
                        client=qdrant_ingest_client,
                        chunk=chunk,
                        chunk_id=pid,
                        dense_vector=dense,
                        sparse_vector=sparse_dict,
                        collection_name=collection,
                    )
                    processed += 1
                except Exception as e:
                    errors += 1
                    processed += 1
                    logger.warning(f"Re-embed error on {pid}: {e}")

                _reembed_status["processed"] = processed
                _reembed_status["errors"] = errors

                # Progress logging every 100 points
                if processed % 100 == 0:
                    elapsed = time.time() - start
                    rate = processed / elapsed if elapsed > 0 else 0
                    eta = (total - processed) / rate if rate > 0 else 0
                    _reembed_status["message"] = f"{processed}/{total} ({rate:.1f}/s, ETA {eta:.0f}s)"
                    logger.info(f"Re-embed progress: {_reembed_status['message']}")

            if next_offset is None:
                break
            offset = next_offset

        elapsed = time.time() - start
        _reembed_status = {
            "running": False,
            "processed": processed,
            "total": total,
            "errors": errors,
            "message": f"Done: {processed}/{total} in {elapsed:.0f}s ({errors} errors)",
        }
        logger.info(f"Re-embed complete: {_reembed_status['message']}")

    except Exception as e:
        _reembed_status["running"] = False
        _reembed_status["message"] = f"FATAL: {e}"
        logger.error(f"Re-embed failed: {e}", exc_info=True)


@router.post("/reembed/{vehicle_id}")
async def reembed_collection(vehicle_id: str, background_tasks: BackgroundTasks):
    """Re-embed all chunks in a vehicle's collection using the local TEI model.
    
    This fixes embedding model mismatch between environments.
    Runs as a background task — poll /api/admin/reembed/status for progress.
    """
    if _reembed_status["running"]:
        return {"error": "Re-embedding already in progress", "status": _reembed_status}

    background_tasks.add_task(_reembed_collection, vehicle_id)
    return {"message": f"Re-embedding started for {vehicle_id}", "status": _reembed_status}


@router.get("/reembed/status")
async def reembed_status():
    """Check the status of a running re-embed operation."""
    return _reembed_status
