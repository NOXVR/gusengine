"""
Backup MerCruiser Qdrant vectors from Hetzner/Coolify.

Strategy:
1. Use the GusEngine /api/stats endpoint to confirm collection exists
2. Trigger Qdrant snapshot via direct API or backend proxy
3. Download the snapshot file locally
"""
import requests, json, sys, os

# Hetzner GusEngine API
API = "http://5.78.132.233:8888"
COLLECTION = "fsm_corpus_2000_mercury_mercruiser_marine"
LOCAL_SNAPSHOT_DIR = r"j:\GusEngine\storage\snapshots"
os.makedirs(LOCAL_SNAPSHOT_DIR, exist_ok=True)

# Step 1: Check collection via GusEngine stats
print("=" * 60)
print("Step 1: Checking collection via GusEngine API...")
print("=" * 60)

for vid in ["2000_mercury_mercruiser_marine"]:
    try:
        r = requests.get(f"{API}/api/stats/{vid}", timeout=30)
        print(f"  /api/stats/{vid} -> {r.status_code}")
        if r.status_code == 200:
            print(f"  {json.dumps(r.json(), indent=2)}")
    except Exception as e:
        print(f"  Error: {e}")

# Step 2: Try direct Qdrant
print("\n" + "=" * 60)
print("Step 2: Trying direct Qdrant access...")
print("=" * 60)
for port in [6333]:
    try:
        r = requests.get(f"http://5.78.132.233:{port}/collections", timeout=10)
        print(f"  Port {port} -> {r.status_code}")
        if r.status_code == 200:
            cols = r.json()
            print(f"  Collections: {json.dumps(cols, indent=2)}")
    except Exception as e:
        print(f"  Port {port} -> {e}")

# Step 3: Health check
print("\n" + "=" * 60)
print("Step 3: Checking available endpoints...")
print("=" * 60)
for ep in ["/api/health", "/api/vehicles", "/api/stats"]:
    try:
        r = requests.get(f"{API}{ep}", timeout=10)
        print(f"  {ep} -> {r.status_code}: {r.text[:300]}")
    except Exception as e:
        print(f"  {ep} -> {e}")
