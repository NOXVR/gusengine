# backend/routes/upload.py
# V10 PROTOTYPE: File upload endpoint with AUTO-SPLIT for large PDFs
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
AUTO_SPLIT_THRESHOLD = 100  # Pages — auto-split PDFs larger than this
SPLIT_PAGE_SIZE = 50         # Pages per split chunk


def _auto_split_pdf(pdf_path: str, dest_dir: str) -> list[str]:
    """Split a large PDF into smaller chunks using PyMuPDF.
    
    Returns list of split file paths. If PDF is small enough, returns [original_path].
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.warning("PyMuPDF not available — skipping auto-split")
        return [pdf_path]

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
    except Exception as e:
        logger.error(f"Cannot open PDF for split check: {e}")
        return [pdf_path]

    if total_pages <= AUTO_SPLIT_THRESHOLD:
        doc.close()
        return [pdf_path]

    # Split into chunks
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    split_dir = os.path.join(dest_dir, f".splits_{base_name}")
    os.makedirs(split_dir, exist_ok=True)

    split_paths = []
    num_chunks = (total_pages + SPLIT_PAGE_SIZE - 1) // SPLIT_PAGE_SIZE

    for i in range(num_chunks):
        start = i * SPLIT_PAGE_SIZE
        end = min(start + SPLIT_PAGE_SIZE, total_pages)
        
        split_doc = fitz.open()
        split_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
        
        split_name = f"{base_name}_part{i+1:02d}_p{start+1}-{end}.pdf"
        split_path = os.path.join(split_dir, split_name)
        split_doc.save(split_path)
        split_doc.close()
        
        split_paths.append(split_path)

    doc.close()
    logger.info(
        f"Auto-split {os.path.basename(pdf_path)}: {total_pages} pages -> "
        f"{num_chunks} chunks of {SPLIT_PAGE_SIZE} pages in {split_dir}"
    )
    return split_paths


@router.post("/api/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vehicle_id: str = Form(default=""),
):
    """Upload a PDF from the browser, save it, and queue for ingestion.
    
    Large PDFs (>100 pages) are automatically split into 50-page chunks
    for reliable processing.
    """
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
    
    # AUTO-SPLIT: Split large PDFs into manageable chunks
    split_paths = _auto_split_pdf(dest_path, dest_dir)
    
    # Queue each chunk for ingestion
    for split_path in split_paths:
        background_tasks.add_task(
            ingest_pdf_background, split_path, qdrant_ingest_client, collection_name
        )

    if len(split_paths) > 1:
        return {
            "status": "accepted",
            "message": (
                f"Uploaded {safe_name} — auto-split into {len(split_paths)} chunks "
                f"and queued for ingestion (collection: {collection_name})"
            ),
            "filename": safe_name,
            "split_count": len(split_paths),
        }
    else:
        return {
            "status": "accepted",
            "message": f"Uploaded and queued for ingestion: {safe_name} (collection: {collection_name})",
            "filename": safe_name,
        }
