# backend/db.py
# SQLite database layer for GusEngine
# Replaces vehicle_registry.json with persistent storage
# Adds customer vehicles (VIN-scoped) and structured modifications
import os
import json
import sqlite3
import logging
from contextlib import contextmanager
from threading import Lock

logger = logging.getLogger(__name__)

# Database location — must be on a Docker volume for persistence
DB_PATH = os.environ.get("GUSENGINE_DB_PATH", "/app/storage/gusengine.db")

# Thread safety: SQLite connections are not thread-safe
_db_lock = Lock()


def _get_connection() -> sqlite3.Connection:
    """Create a new SQLite connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # Better concurrent read performance
    conn.execute("PRAGMA foreign_keys=ON")     # Enforce FK constraints
    return conn


@contextmanager
def get_db():
    """Thread-safe database connection context manager."""
    with _db_lock:
        conn = _get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


# ──────────────────────────────────────────────────────────────────────────────
# SCHEMA
# ──────────────────────────────────────────────────────────────────────────────

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS base_vehicles (
    id          TEXT PRIMARY KEY,
    year        INTEGER NOT NULL,
    make        TEXT NOT NULL,
    model       TEXT NOT NULL,
    collection  TEXT NOT NULL UNIQUE,
    identity    TEXT NOT NULL,
    ledger_file TEXT NOT NULL,
    pdf_subdir  TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_vehicles (
    vin             TEXT PRIMARY KEY,
    base_vehicle_id TEXT NOT NULL REFERENCES base_vehicles(id) ON DELETE CASCADE,
    customer_name   TEXT NOT NULL,
    notes           TEXT DEFAULT '',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    vin         TEXT NOT NULL REFERENCES customer_vehicles(vin) ON DELETE CASCADE,
    system      TEXT NOT NULL,
    component   TEXT NOT NULL,
    mod_type    TEXT NOT NULL,
    oem_spec    TEXT DEFAULT '',
    actual_spec TEXT DEFAULT '',
    date_applied TEXT DEFAULT '',
    tech_name   TEXT DEFAULT '',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS service_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    vin         TEXT NOT NULL REFERENCES customer_vehicles(vin) ON DELETE CASCADE,
    date        TEXT NOT NULL,
    tech_name   TEXT DEFAULT '',
    description TEXT NOT NULL,
    findings    TEXT DEFAULT '',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    """Initialize the database schema and migrate from JSON if needed."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_db() as conn:
        conn.executescript(_SCHEMA_SQL)
        logger.info(f"Database schema initialized at {DB_PATH}")

        # Check if base_vehicles is empty — seed from JSON if so
        count = conn.execute("SELECT COUNT(*) FROM base_vehicles").fetchone()[0]
        if count == 0:
            _migrate_from_json(conn)


def _migrate_from_json(conn: sqlite3.Connection):
    """Seed base_vehicles from the legacy vehicle_registry.json."""
    json_path = os.environ.get(
        "VEHICLE_REGISTRY_PATH",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "vehicle_registry.json")
    )
    if not os.path.exists(json_path):
        logger.warning(f"No vehicle_registry.json found at {json_path} — starting fresh")
        return

    with open(json_path) as f:
        registry = json.load(f)

    vehicles = registry.get("vehicles", [])
    for v in vehicles:
        try:
            conn.execute(
                """INSERT OR IGNORE INTO base_vehicles 
                   (id, year, make, model, collection, identity, ledger_file, pdf_subdir)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    v["id"], v["year"], v["make"], v["model"],
                    v["collection"], v["identity"],
                    v.get("ledger_filename", f"MASTER_LEDGER_{v['id']}.md"),
                    v.get("pdf_subdir", v["id"]),
                )
            )
        except Exception as e:
            logger.error(f"Failed to migrate vehicle {v.get('id')}: {e}")

    logger.info(f"Migrated {len(vehicles)} vehicles from {json_path}")


# ──────────────────────────────────────────────────────────────────────────────
# BASE VEHICLE CRUD
# ──────────────────────────────────────────────────────────────────────────────

def get_all_base_vehicles() -> list[dict]:
    """Return all base vehicles as dicts."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM base_vehicles ORDER BY make, model, year"
        ).fetchall()
        return [_row_to_vehicle(r) for r in rows]


def get_base_vehicle(vehicle_id: str) -> dict | None:
    """Look up a base vehicle by ID."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM base_vehicles WHERE id = ?", (vehicle_id,)
        ).fetchone()
        return _row_to_vehicle(row) if row else None


def add_base_vehicle(vehicle_id: str, year: int, make: str, model: str,
                     collection: str, identity: str, ledger_file: str,
                     pdf_subdir: str) -> dict:
    """Add a new base vehicle. Returns the created vehicle dict."""
    with get_db() as conn:
        conn.execute(
            """INSERT INTO base_vehicles 
               (id, year, make, model, collection, identity, ledger_file, pdf_subdir)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (vehicle_id, year, make, model, collection, identity, ledger_file, pdf_subdir)
        )
    return get_base_vehicle(vehicle_id)


def delete_base_vehicle(vehicle_id: str) -> bool:
    """Delete a base vehicle and all linked customer vehicles (CASCADE)."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM base_vehicles WHERE id = ?", (vehicle_id,))
        return cursor.rowcount > 0


def _row_to_vehicle(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a vehicle dict matching the legacy format."""
    return {
        "id": row["id"],
        "year": row["year"],
        "make": row["make"],
        "model": row["model"],
        "collection": row["collection"],
        "identity": row["identity"],
        "ledger_filename": row["ledger_file"],
        "pdf_subdir": row["pdf_subdir"],
    }


# ──────────────────────────────────────────────────────────────────────────────
# CUSTOMER VEHICLE CRUD
# ──────────────────────────────────────────────────────────────────────────────

def get_all_customers() -> list[dict]:
    """Return all customer vehicles with their base vehicle info."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT c.vin, c.customer_name, c.notes, c.created_at,
                   b.id as base_id, b.year, b.make, b.model, b.collection, b.identity,
                   b.ledger_file, b.pdf_subdir
            FROM customer_vehicles c
            JOIN base_vehicles b ON c.base_vehicle_id = b.id
            ORDER BY c.customer_name
        """).fetchall()
        return [_row_to_customer(r) for r in rows]


def get_customer(vin: str) -> dict | None:
    """Look up a customer vehicle by VIN."""
    with get_db() as conn:
        row = conn.execute("""
            SELECT c.vin, c.customer_name, c.notes, c.created_at,
                   b.id as base_id, b.year, b.make, b.model, b.collection, b.identity,
                   b.ledger_file, b.pdf_subdir
            FROM customer_vehicles c
            JOIN base_vehicles b ON c.base_vehicle_id = b.id
            WHERE c.vin = ?
        """, (vin,)).fetchone()
        return _row_to_customer(row) if row else None


def add_customer(vin: str, base_vehicle_id: str, customer_name: str,
                 notes: str = "") -> dict:
    """Add a customer vehicle linked to a base vehicle."""
    with get_db() as conn:
        conn.execute(
            """INSERT INTO customer_vehicles (vin, base_vehicle_id, customer_name, notes)
               VALUES (?, ?, ?, ?)""",
            (vin, base_vehicle_id, customer_name, notes)
        )
    return get_customer(vin)


def delete_customer(vin: str) -> bool:
    """Delete a customer vehicle (CASCADE deletes mods + service history)."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM customer_vehicles WHERE vin = ?", (vin,))
        return cursor.rowcount > 0


def _row_to_customer(row: sqlite3.Row) -> dict:
    """Convert a joined customer row to a dict."""
    return {
        "vin": row["vin"],
        "customer_name": row["customer_name"],
        "notes": row["notes"],
        "created_at": row["created_at"],
        "base_vehicle": {
            "id": row["base_id"],
            "year": row["year"],
            "make": row["make"],
            "model": row["model"],
            "collection": row["collection"],
            "identity": row["identity"],
            "ledger_filename": row["ledger_file"],
            "pdf_subdir": row["pdf_subdir"],
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
# MODIFICATION CRUD
# ──────────────────────────────────────────────────────────────────────────────

def get_modifications(vin: str) -> list[dict]:
    """Return all modifications for a VIN."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM modifications WHERE vin = ? ORDER BY created_at DESC",
            (vin,)
        ).fetchall()
        return [dict(r) for r in rows]


def add_modification(vin: str, system: str, component: str, mod_type: str,
                     oem_spec: str = "", actual_spec: str = "",
                     date_applied: str = "", tech_name: str = "") -> dict:
    """Add a structured modification to a customer vehicle."""
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO modifications 
               (vin, system, component, mod_type, oem_spec, actual_spec, date_applied, tech_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (vin, system, component, mod_type, oem_spec, actual_spec, date_applied, tech_name)
        )
        mod_id = cursor.lastrowid
    return get_modification(mod_id)


def get_modification(mod_id: int) -> dict | None:
    """Get a single modification by ID."""
    with get_db() as conn:
        row = conn.execute("SELECT * FROM modifications WHERE id = ?", (mod_id,)).fetchone()
        return dict(row) if row else None


def delete_modification(mod_id: int) -> bool:
    """Delete a single modification."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM modifications WHERE id = ?", (mod_id,))
        return cursor.rowcount > 0


def format_modifications_context(vin: str) -> str:
    """Format all modifications for a VIN as LLM-readable context text.
    
    This is injected into the chat prompt alongside RAG context so Gus
    knows about custom work on the specific vehicle.
    """
    mods = get_modifications(vin)
    if not mods:
        return ""

    lines = [f"VEHICLE-SPECIFIC MODIFICATIONS FOR VIN {vin}:"]
    lines.append("These modifications override factory specifications where applicable.\n")

    for m in mods:
        entry = f"- [{m['system']}] {m['component']} — {m['mod_type']}"
        if m.get("oem_spec"):
            entry += f"\n  OEM: {m['oem_spec']}"
        if m.get("actual_spec"):
            entry += f"\n  ACTUAL: {m['actual_spec']}"
        if m.get("date_applied"):
            entry += f"\n  Applied: {m['date_applied']}"
        if m.get("tech_name"):
            entry += f"\n  Tech: {m['tech_name']}"
        lines.append(entry)

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# SERVICE HISTORY CRUD
# ──────────────────────────────────────────────────────────────────────────────

def get_service_history(vin: str) -> list[dict]:
    """Return service history for a VIN."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM service_history WHERE vin = ? ORDER BY date DESC",
            (vin,)
        ).fetchall()
        return [dict(r) for r in rows]


def add_service_entry(vin: str, date: str, description: str,
                      tech_name: str = "", findings: str = "") -> dict:
    """Add a service history entry."""
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO service_history (vin, date, tech_name, description, findings)
               VALUES (?, ?, ?, ?, ?)""",
            (vin, date, tech_name, description, findings)
        )
        entry_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM service_history WHERE id = ?", (entry_id,)).fetchone()
        return dict(row) if row else {}
