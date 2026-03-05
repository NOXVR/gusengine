# backend/routes/ingest.py
# V10 SPEC: PDF ingestion endpoint with BackgroundTasks and cleanup
import asyncio
import os
from fastapi import APIRouter, BackgroundTasks, Request
from qdrant_client import models
from backend.shared.clients import qdrant_ingest_client
from backend.ingestion.pipeline import ingest_pdf_background
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# AUDIT FIX (P2-11): Path traversal prevention.
# For RunPod, use ALLOWED_PDF_DIR env var to override.
ALLOWED_PDF_DIR = os.environ.get("ALLOWED_PDF_DIR", "/app/pdfs")


@router.post("/api/ingest", status_code=202)
async def ingest(request: Request, background_tasks: BackgroundTasks):
    """Queue a PDF for ingestion. Returns 202 immediately; processing happens in background."""
    body = await request.json()
    # AUDIT FIX (DT-P4-04 + DT-P5-05): The host daemon sends absolute HOST paths.
    # Extract the relative path AFTER "pdfs/" to preserve subdirectory structure.
    raw_path = body.get("pdf_path", "")
    if not raw_path or not isinstance(raw_path, str):
        return {"status": "rejected", "message": "Missing or invalid pdf_path"}
    # AUDIT FIX (P6-07): Null bytes cause os.path.realpath() to raise ValueError.
    if "\x00" in raw_path:
        return {"status": "rejected", "message": "Invalid path"}
    rel_path = raw_path.split("pdfs/", 1)[-1] if "pdfs/" in raw_path else os.path.basename(raw_path)
    pdf_path = os.path.realpath(os.path.join(ALLOWED_PDF_DIR, rel_path))
    # AUDIT FIX (P2-11 + DT-P3-04): Validate path is within allowed directory.
    if not pdf_path.startswith(ALLOWED_PDF_DIR + "/"):
        return {"status": "rejected", "message": "Path outside allowed directory"}
    if not pdf_path.endswith(".pdf"):
        return {"status": "rejected", "message": "Not a PDF file"}
    if not os.path.isfile(pdf_path):
        return {"status": "rejected", "message": f"PDF not found: {rel_path}"}
    # AUDIT FIX (P10-25): Use qdrant_ingest_client for write operations.
    background_tasks.add_task(ingest_pdf_background, pdf_path, qdrant_ingest_client)
    return {"status": "accepted", "message": f"Ingestion queued for {pdf_path}"}


# AUDIT FIX (DT-P8-05): Ghost chunk cleanup endpoint.
# Usage: POST /api/cleanup {"source": "brakes/manual.pdf"}
# AUDIT FIX (DT-P10-03): Run BEFORE re-ingestion, not after.
@router.post("/api/cleanup", status_code=200)
async def cleanup_document(request: Request):
    body = await request.json()
    source = body.get("source")
    if not source or not isinstance(source, str):
        return {"status": "rejected", "message": "Missing or invalid 'source' field"}
    # AUDIT FIX (P9-04): Wrap synchronous Qdrant delete in asyncio.to_thread().
    await asyncio.to_thread(
        qdrant_ingest_client.delete,
        collection_name="fsm_corpus",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[models.FieldCondition(
                    key="source",
                    match=models.MatchValue(value=source),
                )]
            )
        ),
    )
    return {"status": "success", "message": f"All chunks with source='{source}' deleted"}
