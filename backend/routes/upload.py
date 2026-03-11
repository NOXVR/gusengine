# backend/routes/upload.py
# V10 PROTOTYPE: File upload endpoint for browser-based PDF uploads
# V10 FIREWALL: Vehicle-scoped collection routing for uploads
import os
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from backend.shared.clients import qdrant_ingest_client
from backend.ingestion.pipeline import ingest_pdf_background
from backend.routes.vehicle import get_vehicle, get_default_vehicle_id

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_PDF_DIR = os.environ.get("ALLOWED_PDF_DIR", "/app/pdfs")


@router.post("/api/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vehicle_id: str = Form(default=""),
):
    """Upload a PDF from the browser, save it, and queue for ingestion."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"status": "rejected", "message": "Only PDF files are accepted"}

    # Sanitize filename — strip path components
    safe_name = os.path.basename(file.filename)
    if not safe_name:
        return {"status": "rejected", "message": "Invalid filename"}

    # V10 FIREWALL: Route into vehicle-specific subdirectory if configured
    if not vehicle_id:
        vehicle_id = get_default_vehicle_id()
    vehicle = get_vehicle(vehicle_id)
    pdf_subdir = vehicle.get("pdf_subdir", "") if vehicle else ""
    if pdf_subdir:
        dest_dir = os.path.join(ALLOWED_PDF_DIR, pdf_subdir)
    else:
        dest_dir = ALLOWED_PDF_DIR
    dest_path = os.path.join(dest_dir, safe_name)

    try:
        os.makedirs(dest_dir, exist_ok=True)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"PDF uploaded: {dest_path} ({os.path.getsize(dest_path)} bytes)")
    except Exception as e:
        logger.error(f"Upload failed for {safe_name}: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        await file.close()

    # V10 FIREWALL: Use already-resolved vehicle for collection routing
    collection_name = vehicle["collection"] if vehicle else "fsm_corpus"
    # Queue for ingestion
    background_tasks.add_task(ingest_pdf_background, dest_path, qdrant_ingest_client, collection_name)
    return {
        "status": "accepted",
        "message": f"Uploaded and queued for ingestion: {safe_name} (collection: {collection_name})",
        "filename": safe_name
    }
