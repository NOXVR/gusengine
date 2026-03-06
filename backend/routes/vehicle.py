# backend/routes/vehicle.py
# V10 FIREWALL: Vehicle registry API for multi-vehicle routing
import json
import os
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()

# Load vehicle registry at module import
_REGISTRY_PATH = os.environ.get(
    "VEHICLE_REGISTRY_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "vehicle_registry.json")
)

_REGISTRY: dict = {}
_VEHICLES_BY_ID: dict = {}


def _load_registry():
    """Load vehicle registry from JSON file."""
    global _REGISTRY, _VEHICLES_BY_ID
    if not os.path.exists(_REGISTRY_PATH):
        logger.critical(f"Vehicle registry not found: {_REGISTRY_PATH}")
        raise SystemExit(f"Fatal: vehicle registry missing at {_REGISTRY_PATH}")
    with open(_REGISTRY_PATH) as f:
        _REGISTRY = json.load(f)
    _VEHICLES_BY_ID = {v["id"]: v for v in _REGISTRY.get("vehicles", [])}
    logger.info(f"Vehicle registry loaded: {len(_VEHICLES_BY_ID)} vehicles")


def get_vehicle(vehicle_id: str) -> dict | None:
    """Look up a vehicle by ID. Returns None if not found."""
    if not _VEHICLES_BY_ID:
        _load_registry()
    return _VEHICLES_BY_ID.get(vehicle_id)


def get_default_vehicle_id() -> str:
    """Return the default vehicle ID from the registry."""
    if not _REGISTRY:
        _load_registry()
    return _REGISTRY.get("default_vehicle_id", "1976_mercedes_450sl")


def get_all_vehicles() -> list[dict]:
    """Return all registered vehicles."""
    if not _VEHICLES_BY_ID:
        _load_registry()
    return _REGISTRY.get("vehicles", [])


def get_all_collection_names() -> list[str]:
    """Return all Qdrant collection names from the registry."""
    if not _VEHICLES_BY_ID:
        _load_registry()
    return [v["collection"] for v in _REGISTRY.get("vehicles", [])]


@router.get("/api/vehicles")
async def list_vehicles():
    """Return the vehicle registry for frontend dropdown population."""
    vehicles = get_all_vehicles()
    return {
        "vehicles": vehicles,
        "default_vehicle_id": get_default_vehicle_id(),
    }


@router.get("/api/vehicles/{vehicle_id}")
async def get_vehicle_detail(vehicle_id: str):
    """Return a single vehicle config."""
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return {"error": f"Unknown vehicle: {vehicle_id}"}, 404
    return vehicle
