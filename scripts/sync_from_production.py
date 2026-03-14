#!/usr/bin/env python3
"""Pull production database state to local vehicle_registry.json.

Usage:
    python scripts/sync_from_production.py [--url http://5.78.132.233:8888]

This is the "key" — without running this, your local config may be stale.
The check_sync.py pre-push hook will warn you if you forget.
"""
import argparse
import json
import sys
import os

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

DEFAULT_API = "http://5.78.132.233:8888"
REGISTRY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config", "vehicle_registry.json"
)


def main():
    parser = argparse.ArgumentParser(description="Sync production DB to local vehicle_registry.json")
    parser.add_argument("--url", default=DEFAULT_API, help="Production API URL")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing")
    args = parser.parse_args()

    # Pull production snapshot
    print(f"Pulling from {args.url}/api/sync/export ...")
    try:
        r = requests.get(f"{args.url}/api/sync/export", timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"ERROR: Could not reach production API: {e}")
        sys.exit(1)

    data = r.json()
    prod_vehicles = data["snapshot"]["base_vehicles"]
    prod_hash = data["hash"]
    print(f"Production: {len(prod_vehicles)} vehicles, hash={prod_hash[:12]}")

    # Load local registry
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            local_reg = json.load(f)
        local_vehicles = local_reg.get("vehicles", [])
    else:
        local_reg = {"vehicles": [], "default_vehicle_id": ""}
        local_vehicles = []

    local_ids = {v["id"] for v in local_vehicles}
    prod_ids = {v["id"] for v in prod_vehicles}

    new_ids = prod_ids - local_ids
    removed_ids = local_ids - prod_ids

    # Report diff
    if new_ids:
        print(f"\n  NEW in production ({len(new_ids)}):")
        for vid in sorted(new_ids):
            v = next(pv for pv in prod_vehicles if pv["id"] == vid)
            print(f"    + {v['year']} {v['make']} {v['model']} ({vid})")

    if removed_ids:
        print(f"\n  REMOVED from production ({len(removed_ids)}):")
        for vid in sorted(removed_ids):
            print(f"    - {vid}")

    if not new_ids and not removed_ids:
        print("\n  ✅ Local registry matches production — no changes needed.")
        return

    if args.dry_run:
        print("\n  (dry-run — no changes written)")
        return

    # Build updated registry from production data
    # Convert prod format to registry format
    updated_vehicles = []
    for pv in prod_vehicles:
        updated_vehicles.append({
            "id": pv["id"],
            "make": pv["make"],
            "model": pv["model"],
            "year": pv["year"],
            "collection": pv["collection"],
            "identity": pv["identity"],
            "ledger_filename": pv.get("ledger_filename", f"MASTER_LEDGER_{pv['id']}.md"),
            "pdf_subdir": pv.get("pdf_subdir", pv["id"]),
        })

    updated_reg = {
        "vehicles": updated_vehicles,
        "default_vehicle_id": local_reg.get("default_vehicle_id", updated_vehicles[0]["id"] if updated_vehicles else ""),
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(updated_reg, f, indent=4)

    print(f"\n  ✅ Updated {REGISTRY_PATH}")
    print(f"     {len(updated_vehicles)} vehicles synced from production.")
    print(f"     Remember to commit this change!")


if __name__ == "__main__":
    main()
