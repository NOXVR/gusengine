"""
Restore Qdrant snapshots to Hetzner by uploading via the admin API.

Qdrant's snapshot restore API: PUT /collections/{name}/snapshots/upload
The Qdrant port is not exposed externally on Hetzner, so we need to 
go through the backend's admin endpoint or use an SSH tunnel.

This script uses the Qdrant API directly — requires Qdrant port to be
accessible. If running against Hetzner, you need an SSH tunnel:
  ssh -L 6333:localhost:6333 root@5.78.132.233
Then run:
  python restore_snapshots.py --qdrant http://localhost:6333
"""

import requests
import os
import sys
import argparse

SNAPSHOT_DIR = r"j:\GusEngine\storage\snapshots"

COLLECTIONS_TO_RESTORE = {
    "fsm_corpus_1975_cessna_172_skyhawk_aviation": "fsm_corpus_1975_cessna_172_skyhawk_aviation.snapshot",
    "fsm_corpus_2000_mercury_mercruiser_marine": "fsm_corpus_2000_mercury_mercruiser_marine.snapshot",
}


def restore_snapshot(qdrant_url: str, collection: str, snapshot_file: str):
    filepath = os.path.join(SNAPSHOT_DIR, snapshot_file)
    if not os.path.exists(filepath):
        print(f"  ERROR: Snapshot not found: {filepath}")
        return False

    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  Uploading {snapshot_file} ({size_mb:.1f} MB)...")

    url = f"{qdrant_url}/collections/{collection}/snapshots/upload"
    with open(filepath, "rb") as f:
        r = requests.post(
            url,
            files={"snapshot": (snapshot_file, f, "application/octet-stream")},
            timeout=600,
        )

    if r.status_code == 200:
        print(f"  SUCCESS: {collection} restored")
        return True
    else:
        print(f"  ERROR: {r.status_code} - {r.text[:500]}")
        return False


def check_collections(qdrant_url: str):
    """List all collections and their point counts."""
    r = requests.get(f"{qdrant_url}/collections", timeout=30)
    r.raise_for_status()
    collections = r.json()["result"]["collections"]
    print("Current collections:")
    for c in collections:
        name = c["name"]
        # Get point count
        info = requests.get(f"{qdrant_url}/collections/{name}", timeout=30).json()
        points = info["result"]["points_count"]
        print(f"  {name}: {points} points")
    return {c["name"] for c in collections}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qdrant", default="http://localhost:6333", help="Qdrant URL")
    parser.add_argument("--all", action="store_true", help="Restore all snapshots")
    args = parser.parse_args()

    print(f"Qdrant URL: {args.qdrant}")
    print()

    # Check current state
    try:
        existing = check_collections(args.qdrant)
    except Exception as e:
        print(f"ERROR: Cannot reach Qdrant at {args.qdrant}: {e}")
        print("If targeting Hetzner, start an SSH tunnel first:")
        print("  ssh -L 6333:localhost:6333 root@5.78.132.233")
        sys.exit(1)

    print()

    # Determine what to restore
    if args.all:
        to_restore = {
            name: f for f in os.listdir(SNAPSHOT_DIR) 
            if f.endswith(".snapshot")
            for name in [f.replace(".snapshot", "")]
        }
    else:
        to_restore = COLLECTIONS_TO_RESTORE

    for collection, snapshot_file in to_restore.items():
        print(f"\n=== Restoring {collection} ===")
        if collection in existing:
            # Get point count
            info = requests.get(f"{args.qdrant}/collections/{collection}", timeout=30).json()
            points = info["result"]["points_count"]
            if points > 0:
                print(f"  Collection already exists with {points} points — skipping")
                continue
            else:
                print(f"  Collection exists but is EMPTY — restoring")

        success = restore_snapshot(args.qdrant, collection, snapshot_file)
        if not success:
            print(f"  FAILED to restore {collection}")

    print("\n=== Final state ===")
    check_collections(args.qdrant)


if __name__ == "__main__":
    main()
