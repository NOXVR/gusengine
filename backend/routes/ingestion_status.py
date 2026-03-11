# backend/routes/ingestion_status.py
# Ingestion status endpoint — frontend polls this for real-time progress
from fastapi import APIRouter
from backend.ingestion.pipeline import get_ingestion_status, clear_ingestion_status

router = APIRouter()


@router.get("/api/ingestion/status")
async def ingestion_status():
    """Return current ingestion status for all files being processed."""
    return get_ingestion_status()


@router.delete("/api/ingestion/status")
async def clear_status():
    """Clear all completed/failed ingestion statuses."""
    clear_ingestion_status()
    return {"status": "cleared"}
