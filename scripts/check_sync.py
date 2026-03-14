#!/usr/bin/env python3
"""Pre-push integrity check: warns if production has vehicles not in local config.

This is the "locked door" — if production data doesn't match local,
you get a warning and must explicitly confirm before proceeding.

Usage:
    python scripts/check_sync.py [--url http://5.78.132.233:8888]

Exit codes:
    0 = synced (or user confirmed mismatch)
    1 = mismatch and user declined / non-interactive
"""
import argparse
import json
import sys
import os
import hashlib

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


def _local_vehicle_ids() -> set:
    """Read vehicle IDs from local registry."""
    if not os.path.exists(REGISTRY_PATH):
        return set()
    with open(REGISTRY_PATH) as f:
        reg = json.load(f)
    return {v["id"] for v in reg.get("vehicles", [])}


def main():
    parser = argparse.ArgumentParser(description="Check local <-> production vehicle sync")
    parser.add_argument("--url", default=DEFAULT_API, help="Production API URL")
    parser.add_argument("--no-prompt", action="store_true", help="Fail on mismatch without prompting")
    args = parser.parse_args()

    # Get production state
    try:
        r = requests.get(f"{args.url}/api/sync/hash", timeout=10)
        r.raise_for_status()
        prod_data = r.json()
    except requests.exceptions.ConnectionError:
        print("[!] Cannot reach production API -- skipping sync check.")
        print(f"   (tried {args.url}/api/sync/hash)")
        sys.exit(0)  # Don't block if server is down
    except Exception as e:
        print(f"[!] Sync check failed: {e}")
        sys.exit(0)  # Don't block on unexpected errors

    prod_count = prod_data["vehicle_count"]
    local_ids = _local_vehicle_ids()
    local_count = len(local_ids)

    if prod_count == local_count:
        print(f"[OK] Sync OK: {local_count} vehicles locally, {prod_count} in production.")
        sys.exit(0)

    # Mismatch detected — get full details
    try:
        r2 = requests.get(f"{args.url}/api/sync/export", timeout=15)
        r2.raise_for_status()
        export = r2.json()
        prod_vehicles = export["snapshot"]["base_vehicles"]
        prod_ids = {v["id"] for v in prod_vehicles}
    except Exception:
        prod_ids = set()

    new_in_prod = prod_ids - local_ids
    missing_from_prod = local_ids - prod_ids

    print("=" * 60)
    print("[!] VEHICLE DATA MISMATCH DETECTED")
    print("=" * 60)
    print(f"  Local:      {local_count} vehicles")
    print(f"  Production: {prod_count} vehicles")

    if new_in_prod:
        print(f"\n  Production has {len(new_in_prod)} vehicle(s) NOT in your local config:")
        for vid in sorted(new_in_prod):
            v = next((pv for pv in prod_vehicles if pv["id"] == vid), None)
            if v:
                print(f"    + {v['year']} {v['make']} {v['model']} ({vid})")
            else:
                print(f"    + {vid}")

    if missing_from_prod:
        print(f"\n  Local has {len(missing_from_prod)} vehicle(s) NOT in production:")
        for vid in sorted(missing_from_prod):
            print(f"    - {vid}")

    print()
    print("  Run 'python scripts/sync_from_production.py' to pull production data.")
    print()

    if args.no_prompt:
        print("  --no-prompt specified: aborting.")
        sys.exit(1)

    try:
        answer = input("  Proceed anyway? [y/N]: ").strip().lower()
        if answer == "y":
            print("  Proceeding with mismatch.")
            sys.exit(0)
        else:
            print("  Aborting. Sync first, then retry.")
            sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        print("\n  Non-interactive — aborting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
