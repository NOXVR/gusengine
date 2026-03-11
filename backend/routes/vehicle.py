# backend/routes/vehicle.py
# V10 FIREWALL: Vehicle registry API for multi-vehicle routing
import json
import os
import re
import logging
from fastapi import APIRouter
from pydantic import BaseModel

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


def _save_registry():
    """Persist the current registry to disk."""
    with open(_REGISTRY_PATH, "w") as f:
        json.dump(_REGISTRY, f, indent=4)
    logger.info(f"Vehicle registry saved to {_REGISTRY_PATH}")


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


# --- Dynamic Vehicle Registration ---

class AddVehicleRequest(BaseModel):
    year: int
    make: str
    model: str


def _sanitize_id(text: str) -> str:
    """Convert text to a safe ID component: lowercase, spaces/hyphens to underscores."""
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


@router.post("/api/vehicles")
async def add_vehicle(req: AddVehicleRequest):
    """Register a new vehicle dynamically.
    
    Auto-generates: ID, Qdrant collection, system prompt, ledger filename, PDF subdirectory.
    Creates the Qdrant collection and PDF storage directory.
    """
    from backend.shared.clients import qdrant_ingest_client
    from backend.ingestion.qdrant_setup import create_collection

    # Ensure registry is loaded
    if not _REGISTRY:
        _load_registry()

    # Generate derived fields
    make_id = _sanitize_id(req.make)
    model_id = _sanitize_id(req.model)
    vehicle_id = f"{req.year}_{make_id}_{model_id}"
    collection_name = f"fsm_corpus_{vehicle_id}"

    # Check for duplicates
    if vehicle_id in _VEHICLES_BY_ID:
        return {"status": "error", "message": f"Vehicle already exists: {vehicle_id}"}

    # Build the vehicle entry
    vehicle = {
        "id": vehicle_id,
        "make": req.make.strip(),
        "model": req.model.strip(),
        "year": req.year,
        "collection": collection_name,
        "identity": (
            f'You are "GUS," a Tier-1 Master Mechanic specializing in the '
            f'{req.year} {req.make.strip()} {req.model.strip()}. '
            f'You are authoritative, direct, and grounded in physical verification.'
        ),
        "ledger_filename": f"MASTER_LEDGER_{vehicle_id}.md",
        "pdf_subdir": vehicle_id,
    }

    # Create Qdrant collection
    try:
        create_collection(qdrant_ingest_client, collection_name=collection_name)
        logger.info(f"Created Qdrant collection: {collection_name}")
    except Exception as e:
        # Collection might already exist from a previous partial creation
        logger.warning(f"Qdrant collection creation note: {e}")

    # Create PDF storage subdirectory
    pdf_base = os.environ.get("ALLOWED_PDF_DIR", "/app/storage/pdfs")
    pdf_dir = os.path.join(pdf_base, vehicle_id)
    os.makedirs(pdf_dir, exist_ok=True)
    logger.info(f"Created PDF directory: {pdf_dir}")

    # Add to registry and persist
    _REGISTRY.setdefault("vehicles", []).append(vehicle)
    _VEHICLES_BY_ID[vehicle_id] = vehicle
    _save_registry()

    return {"status": "ok", "vehicle": vehicle}
