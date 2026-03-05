# backend/routes/health.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
async def health():
    """Service readiness probe."""
    return {"status": "ok"}
