# backend/routes/upload.py
# V10 PROTOTYPE: File upload endpoint for browser-based PDF uploads
import os
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from backend.shared.clients import qdrant_ingest_client
from backend.ingestion.pipeline import ingest_pdf_background

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_PDF_DIR = os.environ.get("ALLOWED_PDF_DIR", "/app/pdfs")


@router.post("/api/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload a PDF from the browser, save it, and queue for ingestion."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"status": "rejected", "message": "Only PDF files are accepted"}

    # Sanitize filename — strip path components
    safe_name = os.path.basename(file.filename)
    if not safe_name:
        return {"status": "rejected", "message": "Invalid filename"}

    dest_path = os.path.join(ALLOWED_PDF_DIR, safe_name)

    try:
        os.makedirs(ALLOWED_PDF_DIR, exist_ok=True)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"PDF uploaded: {dest_path} ({os.path.getsize(dest_path)} bytes)")
    except Exception as e:
        logger.error(f"Upload failed for {safe_name}: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        await file.close()

    # Queue for ingestion
    background_tasks.add_task(ingest_pdf_background, dest_path, qdrant_ingest_client)
    return {
        "status": "accepted",
        "message": f"Uploaded and queued for ingestion: {safe_name}",
        "filename": safe_name
    }
