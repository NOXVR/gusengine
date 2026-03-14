# backend/routes/image_ops.py
# Endpoints for PDF-only upload (no ingestion) and standalone image catalog indexing.
# These allow uploading PDFs to make citations work without re-ingesting text,
# and running the image catalog independently to add image_reference chunks.
import os
import shutil
import asyncio
import logging
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_PDF_DIR = os.environ.get("ALLOWED_PDF_DIR", "/app/pdfs")


@router.post("/api/upload-pdfs-only")
async def upload_pdfs_only(
    files: list[UploadFile] = File(...),
    vehicle_id: str = Form(default=""),
):
    """Upload PDFs to the server for citation viewing ONLY — no ingestion triggered.

    This saves files to the persistent volume so /api/pdf/{source} can serve them,
    without re-parsing or creating duplicate chunks in Qdrant.
    """
    from backend.routes.vehicle import get_vehicle, get_default_vehicle_id

    if not vehicle_id:
        vehicle_id = get_default_vehicle_id()
    vehicle = get_vehicle(vehicle_id)
    pdf_subdir = vehicle.get("pdf_subdir", "") if vehicle else ""
    dest_dir = os.path.join(ALLOWED_PDF_DIR, pdf_subdir) if pdf_subdir else ALLOWED_PDF_DIR

    os.makedirs(dest_dir, exist_ok=True)

    saved = []
    skipped = []
    errors = []

    for file in files:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            skipped.append(file.filename or "unknown")
            continue

        safe_name = os.path.basename(file.filename)
        dest_path = os.path.join(dest_dir, safe_name)

        try:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            saved.append(safe_name)
        except Exception as e:
            errors.append({"file": safe_name, "error": str(e)})
            logger.error(f"Upload-only failed for {safe_name}: {e}")
        finally:
            await file.close()

    logger.info(f"Upload-only: {len(saved)} saved, {len(skipped)} skipped, {len(errors)} errors to {dest_dir}")

    return {
        "status": "complete",
        "saved": len(saved),
        "skipped": len(skipped),
        "errors": errors,
        "destination": dest_dir,
        "files": saved[:20],  # Cap response size
    }


@router.post("/api/run-image-catalog")
async def run_image_catalog(
    vehicle_id: str = Form(default=""),
):
    """Run the image catalog on existing PDFs and index image_reference chunks.

    This scans all PDFs in the vehicle's PDF directory, extracts image references
    (captions, page numbers, image counts), and indexes them into Qdrant as
    image_reference chunks. Does NOT re-ingest text — only adds image metadata.

    The image catalog uses deterministic UUIDs, so re-running is safe (idempotent).
    """
    from backend.routes.vehicle import get_vehicle, get_default_vehicle_id
    from backend.shared.clients import qdrant_ingest_client
    from backend.ingestion.image_catalog import extract_image_references
    from backend.ingestion.qdrant_setup import index_chunk
    from backend.inference.embeddings import embed_text

    if not vehicle_id:
        vehicle_id = get_default_vehicle_id()
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return JSONResponse({"detail": f"Vehicle not found: {vehicle_id}"}, status_code=404)

    collection_name = vehicle["collection"]
    pdf_subdir = vehicle.get("pdf_subdir", "")
    pdf_dir = os.path.join(ALLOWED_PDF_DIR, pdf_subdir) if pdf_subdir else ALLOWED_PDF_DIR

    if not os.path.isdir(pdf_dir):
        return JSONResponse(
            {"detail": f"PDF directory not found: {pdf_dir}"},
            status_code=404,
        )

    # Find all PDFs (including in .splits_ subdirs)
    pdf_files = []
    for root, dirs, filenames in os.walk(pdf_dir):
        for fn in filenames:
            if fn.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, fn))

    if not pdf_files:
        return JSONResponse(
            {"detail": f"No PDFs found in {pdf_dir}"},
            status_code=404,
        )

    logger.info(f"Image catalog: scanning {len(pdf_files)} PDFs for {vehicle_id}")

    total_refs = 0
    total_indexed = 0
    errors = []
    client = qdrant_ingest_client()

    for pdf_path in pdf_files:
        try:
            # Compute the source path (relative to ALLOWED_PDF_DIR)
            source = os.path.basename(pdf_path)
            for prefix in ["/app/pdfs/", "/app/storage/pdfs/", ALLOWED_PDF_DIR + "/"]:
                if prefix in pdf_path:
                    source = pdf_path.split(prefix, 1)[-1]
                    break

            # Extract image references
            refs = await asyncio.to_thread(extract_image_references, pdf_path, source)
            if not refs:
                continue

            total_refs += len(refs)

            # Embed and index each image reference chunk
            for i, chunk in enumerate(refs):
                # Deterministic UUID — safe to re-run
                chunk_id = str(uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"image_catalog:{pdf_path}_{i}"
                ))

                try:
                    dense, sparse = await embed_text(chunk["text"])
                    sparse_dict = sparse or {"indices": [], "values": []}

                    await asyncio.to_thread(
                        index_chunk,
                        client=client,
                        chunk=chunk,
                        chunk_id=chunk_id,
                        dense_vector=dense,
                        sparse_vector=sparse_dict,
                        collection_name=collection_name,
                    )
                    total_indexed += 1
                    # Throttle to avoid overwhelming Qdrant
                    await asyncio.sleep(0.15)
                except Exception as e:
                    logger.warning(f"Failed to index image ref from {source}: {e}")
                    errors.append({"source": source, "error": str(e)})

        except Exception as e:
            logger.warning(f"Image catalog failed for {os.path.basename(pdf_path)}: {e}")
            errors.append({"file": os.path.basename(pdf_path), "error": str(e)})

    logger.info(
        f"Image catalog complete: {total_refs} refs found, "
        f"{total_indexed} indexed, {len(errors)} errors"
    )

    return {
        "status": "complete",
        "vehicle_id": vehicle_id,
        "collection": collection_name,
        "pdfs_scanned": len(pdf_files),
        "image_refs_found": total_refs,
        "image_refs_indexed": total_indexed,
        "errors": errors[:20],
    }
