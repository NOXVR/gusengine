"""Snapshot ALL Qdrant collections on Hetzner and download locally."""
import requests, json, os, hashlib, time

API = "http://5.78.132.233:8888"
SNAPSHOT_DIR = r"j:\GusEngine\storage\snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# 1. List all vehicles/collections
print("=== Checking registered vehicles on Hetzner ===")
r = requests.get(f"{API}/api/vehicles", timeout=10)
vehicles = r.json()["vehicles"]
print(f"Total vehicles: {len(vehicles)}")
for v in vehicles:
    vid = v["id"]
    collection = v.get("collection", f"fsm_corpus_{vid}")
    print(f"  - {vid}: {collection} ({v.get('make','')} {v.get('model','')})")

# 2. Check stats for each
print("\n=== Collection stats ===")
collections = {}
for v in vehicles:
    vid = v["id"]
    try:
        sr = requests.get(f"{API}/api/stats/{vid}", timeout=10)
        stats = sr.json()
        points = stats.get("total_points", stats.get("vectors", "?"))
        sources = stats.get("total_sources", stats.get("sources", "?"))
        collection = v.get("collection", f"fsm_corpus_{vid}")
        collections[vid] = {
            "collection": collection,
            "points": points,
            "sources": sources,
            "make": v.get("make", ""),
            "model": v.get("model", ""),
        }
        print(f"  {vid}: {points} points / {sources} sources")
    except Exception as e:
        print(f"  {vid}: ERROR - {e}")

# 3. Check which snapshots we already have locally
print("\n=== Local snapshots ===")
existing = set()
for f in os.listdir(SNAPSHOT_DIR):
    if f.endswith(".snapshot"):
        size_mb = os.path.getsize(os.path.join(SNAPSHOT_DIR, f)) / (1024*1024)
        print(f"  EXISTS: {f} ({size_mb:.1f} MB)")
        existing.add(f)

# 4. Report what needs to be done
print("\n=== Snapshot plan ===")
for vid, info in collections.items():
    local_name = f"{info['collection']}.snapshot"
    if local_name in existing:
        print(f"  SKIP {vid}: already backed up as {local_name}")
    else:
        print(f"  NEED {vid}: {info['collection']} ({info['points']} points)")

print("\n=== Summary ===")
print(f"Total collections: {len(collections)}")
backed = sum(1 for v in collections.values() if v["collection"] + ".snapshot" in existing)
needed = sum(1 for v in collections.values() if v["collection"] + ".snapshot" not in existing)
print(f"Already backed up: {backed}")
print(f"Need backup: {needed}")
