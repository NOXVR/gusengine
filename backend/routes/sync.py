# backend/routes/sync.py
# Database sync API for local ↔ production data integrity
import hashlib
import json
import logging
from fastapi import APIRouter
from backend.db import (
    get_all_base_vehicles, get_all_customers,
    get_modifications, get_service_history,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _build_snapshot() -> dict:
    """Build a full snapshot of all DB state."""
    vehicles = get_all_base_vehicles()
    customers = get_all_customers()

    # Attach modifications and service history to each customer
    for c in customers:
        vin = c["vin"]
        c["modifications"] = get_modifications(vin)
        c["service_history"] = get_service_history(vin)

    return {
        "base_vehicles": vehicles,
        "customer_vehicles": customers,
    }


def _snapshot_hash(snapshot: dict) -> str:
    """Deterministic SHA-256 hash of snapshot for integrity comparison."""
    canonical = json.dumps(snapshot, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


@router.get("/api/sync/export")
async def sync_export():
    """Export full DB state as JSON snapshot with integrity hash.
    
    Used by scripts/sync_from_production.py to pull production data locally.
    """
    snapshot = _build_snapshot()
    h = _snapshot_hash(snapshot)
    logger.info(
        f"Sync export: {len(snapshot['base_vehicles'])} vehicles, "
        f"{len(snapshot['customer_vehicles'])} customers, hash={h[:12]}"
    )
    return {
        "snapshot": snapshot,
        "hash": h,
        "vehicle_count": len(snapshot["base_vehicles"]),
        "customer_count": len(snapshot["customer_vehicles"]),
    }


@router.get("/api/sync/hash")
async def sync_hash():
    """Lightweight hash-only check for pre-deploy integrity verification.
    
    Used by scripts/check_sync.py to detect data mismatches without
    transferring the full snapshot.
    """
    snapshot = _build_snapshot()
    h = _snapshot_hash(snapshot)
    return {
        "hash": h,
        "vehicle_count": len(snapshot["base_vehicles"]),
        "customer_count": len(snapshot["customer_vehicles"]),
    }
