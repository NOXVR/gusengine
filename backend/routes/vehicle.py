# backend/routes/vehicle.py
# V10 FIREWALL: Vehicle registry API — SQLite-backed with customer vehicles
import os
import re
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import (
    get_all_base_vehicles, get_base_vehicle, add_base_vehicle, delete_base_vehicle,
    get_all_customers, get_customer, add_customer, delete_customer,
    get_modifications, add_modification, delete_modification,
    get_service_history, add_service_entry,
)

logger = logging.getLogger(__name__)
router = APIRouter()


# ──────────────────────────────────────────────────────────────────────────────
# COMPATIBILITY LAYER — These functions are called by chat.py, upload.py, etc.
# Signatures match the old JSON-based implementation exactly.
# ──────────────────────────────────────────────────────────────────────────────

def get_vehicle(vehicle_id: str) -> dict | None:
    """Look up a vehicle by ID. Works for both base and customer vehicles.
    
    If vehicle_id looks like a VIN (customer vehicle), resolves to the base vehicle
    config but keeps the VIN for modification context injection.
    """
    # First try as a base vehicle ID
    vehicle = get_base_vehicle(vehicle_id)
    if vehicle:
        return vehicle
    
    # Try as a customer VIN
    customer = get_customer(vehicle_id)
    if customer:
        # Return the base vehicle config with VIN info attached
        base = customer["base_vehicle"]
        base["_customer_vin"] = customer["vin"]
        base["_customer_name"] = customer["customer_name"]
        return base
    
    return None


def get_default_vehicle_id() -> str:
    """Return the first vehicle ID as default."""
    vehicles = get_all_base_vehicles()
    if vehicles:
        return vehicles[0]["id"]
    return "1976_mercedes_450sl"


def get_all_vehicles() -> list[dict]:
    """Return all base vehicles (for mismatch linting etc)."""
    return get_all_base_vehicles()


def get_all_collection_names() -> list[str]:
    """Return all Qdrant collection names from base vehicles."""
    return [v["collection"] for v in get_all_base_vehicles()]


# ──────────────────────────────────────────────────────────────────────────────
# BASE VEHICLE ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/api/vehicles")
async def list_vehicles():
    """Return base vehicles + customer vehicles for the frontend dropdown."""
    base_vehicles = get_all_base_vehicles()
    customers = get_all_customers()
    return {
        "vehicles": base_vehicles,
        "customers": customers,
        "default_vehicle_id": get_default_vehicle_id(),
    }


@router.get("/api/vehicles/{vehicle_id}")
async def get_vehicle_detail(vehicle_id: str):
    """Return a single base vehicle config."""
    vehicle = get_base_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Unknown vehicle: {vehicle_id}")
    return vehicle


class AddVehicleRequest(BaseModel):
    year: int
    make: str
    model: str


def _sanitize_id(text: str) -> str:
    """Convert text to a safe ID: lowercase, non-alnum to underscores."""
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


@router.post("/api/vehicles")
async def add_vehicle_endpoint(req: AddVehicleRequest):
    """Register a new base vehicle. Creates Qdrant collection and PDF directory."""
    from backend.shared.clients import qdrant_ingest_client
    from backend.ingestion.qdrant_setup import create_collection

    make_id = _sanitize_id(req.make)
    model_id = _sanitize_id(req.model)
    vehicle_id = f"{req.year}_{make_id}_{model_id}"
    collection_name = f"fsm_corpus_{vehicle_id}"

    # Check for duplicates
    if get_base_vehicle(vehicle_id):
        raise HTTPException(status_code=409, detail=f"Vehicle already exists: {vehicle_id}")

    identity = (
        f'You are "GUS," a Tier-1 Master Mechanic specializing in the '
        f'{req.year} {req.make.strip()} {req.model.strip()}. '
        f'You are authoritative, direct, and grounded in physical verification.'
    )

    # Create Qdrant collection
    try:
        create_collection(qdrant_ingest_client, collection_name=collection_name)
        logger.info(f"Created Qdrant collection: {collection_name}")
    except Exception as e:
        logger.warning(f"Qdrant collection creation note: {e}")

    # Create PDF storage directory
    pdf_base = os.environ.get("ALLOWED_PDF_DIR", "/app/storage/pdfs")
    pdf_dir = os.path.join(pdf_base, vehicle_id)
    os.makedirs(pdf_dir, exist_ok=True)

    # Save to database
    vehicle = add_base_vehicle(
        vehicle_id=vehicle_id,
        year=req.year,
        make=req.make.strip(),
        model=req.model.strip(),
        collection=collection_name,
        identity=identity,
        ledger_file=f"MASTER_LEDGER_{vehicle_id}.md",
        pdf_subdir=vehicle_id,
    )
    logger.info(f"Added base vehicle: {vehicle_id}")
    return {"status": "ok", "vehicle": vehicle}


@router.delete("/api/vehicles/{vehicle_id}")
async def delete_vehicle_endpoint(vehicle_id: str):
    """Delete a base vehicle, its Qdrant collection, and uploaded PDFs."""
    vehicle = get_base_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Unknown vehicle: {vehicle_id}")

    # Delete Qdrant collection
    try:
        from backend.shared.clients import qdrant_ingest_client
        qdrant_ingest_client.delete_collection(vehicle["collection"])
        logger.info(f"Deleted Qdrant collection: {vehicle['collection']}")
    except Exception as e:
        logger.warning(f"Qdrant collection deletion failed (may not exist): {e}")

    # Delete PDF directory
    pdf_base = os.environ.get("ALLOWED_PDF_DIR", "/app/storage/pdfs")
    pdf_dir = os.path.join(pdf_base, vehicle.get("pdf_subdir", vehicle_id))
    if os.path.isdir(pdf_dir):
        import shutil
        shutil.rmtree(pdf_dir, ignore_errors=True)
        logger.info(f"Deleted PDF directory: {pdf_dir}")

    # Delete from database (CASCADE removes customer vehicles + mods)
    delete_base_vehicle(vehicle_id)
    logger.info(f"Deleted base vehicle: {vehicle_id}")

    return {"status": "ok", "message": f"Vehicle {vehicle_id} and all associated data deleted"}


# ──────────────────────────────────────────────────────────────────────────────
# CUSTOMER VEHICLE ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

class AddCustomerRequest(BaseModel):
    vin: str
    base_vehicle_id: str
    customer_name: str
    notes: str = ""


@router.post("/api/customers")
async def add_customer_endpoint(req: AddCustomerRequest):
    """Add a customer vehicle linked to a base vehicle."""
    # Validate base vehicle exists
    base = get_base_vehicle(req.base_vehicle_id)
    if not base:
        raise HTTPException(status_code=404, detail=f"Base vehicle not found: {req.base_vehicle_id}")

    # Check for duplicate VIN
    if get_customer(req.vin):
        raise HTTPException(status_code=409, detail=f"VIN already registered: {req.vin}")

    customer = add_customer(
        vin=req.vin.strip().upper(),
        base_vehicle_id=req.base_vehicle_id,
        customer_name=req.customer_name.strip(),
        notes=req.notes.strip(),
    )
    logger.info(f"Added customer vehicle: VIN={req.vin}, base={req.base_vehicle_id}")
    return {"status": "ok", "customer": customer}


@router.get("/api/customers")
async def list_customers():
    """Return all customer vehicles."""
    return {"customers": get_all_customers()}


@router.get("/api/customers/{vin}")
async def get_customer_detail(vin: str):
    """Return a customer vehicle with its modifications and service history."""
    customer = get_customer(vin)
    if not customer:
        raise HTTPException(status_code=404, detail=f"VIN not found: {vin}")
    customer["modifications"] = get_modifications(vin)
    customer["service_history"] = get_service_history(vin)
    return customer


@router.delete("/api/customers/{vin}")
async def delete_customer_endpoint(vin: str):
    """Delete a customer vehicle and all its modifications/service history."""
    if not get_customer(vin):
        raise HTTPException(status_code=404, detail=f"VIN not found: {vin}")
    delete_customer(vin)
    logger.info(f"Deleted customer vehicle: VIN={vin}")
    return {"status": "ok", "message": f"Customer vehicle {vin} deleted"}


# ──────────────────────────────────────────────────────────────────────────────
# MODIFICATION ENDPOINTS
# ──────────────────────────────────────────────────────────────────────────────

class AddModificationRequest(BaseModel):
    system: str         # Engine, Transmission, Brakes, Steering, etc.
    component: str      # Specific component name
    mod_type: str       # Replacement, Upgrade, Repair, Removal
    oem_spec: str = ""
    actual_spec: str = ""
    date_applied: str = ""
    tech_name: str = ""


@router.post("/api/customers/{vin}/modifications")
async def add_modification_endpoint(vin: str, req: AddModificationRequest):
    """Add a structured modification to a customer vehicle."""
    if not get_customer(vin):
        raise HTTPException(status_code=404, detail=f"VIN not found: {vin}")
    mod = add_modification(
        vin=vin,
        system=req.system.strip(),
        component=req.component.strip(),
        mod_type=req.mod_type.strip(),
        oem_spec=req.oem_spec.strip(),
        actual_spec=req.actual_spec.strip(),
        date_applied=req.date_applied.strip(),
        tech_name=req.tech_name.strip(),
    )
    logger.info(f"Added modification to VIN={vin}: {req.system}/{req.component}")
    return {"status": "ok", "modification": mod}


@router.get("/api/customers/{vin}/modifications")
async def list_modifications(vin: str):
    """Return all modifications for a customer vehicle."""
    if not get_customer(vin):
        raise HTTPException(status_code=404, detail=f"VIN not found: {vin}")
    return {"modifications": get_modifications(vin)}


@router.delete("/api/modifications/{mod_id}")
async def delete_modification_endpoint(mod_id: int):
    """Delete a single modification."""
    if not delete_modification(mod_id):
        raise HTTPException(status_code=404, detail=f"Modification not found: {mod_id}")
    return {"status": "ok", "message": f"Modification {mod_id} deleted"}
