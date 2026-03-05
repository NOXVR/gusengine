#!/bin/bash
# Nuclear option: delete vector DB table, then re-add all docs
# This forces AnythingLLM to re-chunk and re-vectorize from the 
# modified (densified) pageContent files
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"
STORAGE="/home/ubuntu/diagnostic_engine/storage"

echo "=== Step 1: Remove all docs from workspace ==="
python3 << 'PYEOF'
import json, urllib.request
api_key = "S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
base = "http://127.0.0.1:3001/api/v1"
slug = "1975-mercedes-benz-450sl"

req = urllib.request.Request(f"{base}/workspace/{slug}",
    headers={"Authorization": f"Bearer {api_key}"})
resp = json.loads(urllib.request.urlopen(req).read())
ws = resp.get("workspace", resp)
if isinstance(ws, list): ws = ws[0]
docs = ws.get("documents", [])
paths = [d.get("docpath","") for d in docs if d.get("docpath")]
print(f"Removing {len(paths)} docs from workspace...")
if paths:
    data = json.dumps({"adds": [], "deletes": paths}).encode()
    req2 = urllib.request.Request(f"{base}/workspace/{slug}/update-embeddings",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    resp2 = json.loads(urllib.request.urlopen(req2).read())
    print(f"Remaining: {len(resp2.get('workspace',{}).get('documents',[]))}")
PYEOF

echo ""
echo "=== Step 2: Delete vector DB table ==="
rm -rf "$STORAGE/lancedb/1975-mercedes-benz-450sl.lance"
echo "LanceDB table deleted"
ls "$STORAGE/lancedb/"

echo ""
echo "=== Step 3: Restart container to clear caches ==="
docker restart diagnostic_rag_engine
echo "Waiting 15s for container..."
sleep 15
docker ps --format '{{.Names}} {{.Status}}'

echo ""
echo "=== Step 4: Re-add all densified documents ==="
python3 << 'PYEOF'
import json, urllib.request, os, time
api_key = "S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
base = "http://127.0.0.1:3001/api/v1"
slug = "1975-mercedes-benz-450sl"
doc_dir = os.path.expanduser("~/diagnostic_engine/storage/documents/custom-documents")

files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".json")])
adds = [f"custom-documents/{f}" for f in files]
print(f"Re-adding {len(adds)} densified documents...")

# Add in batches of 50 (smaller batches for more reliable vectorization)
for i in range(0, len(adds), 50):
    batch = adds[i:i+50]
    data = json.dumps({"adds": batch, "deletes": []}).encode()
    try:
        req = urllib.request.Request(f"{base}/workspace/{slug}/update-embeddings",
            data=data,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req).read())
        count = len(resp.get("workspace", {}).get("documents", []))
        print(f"  Batch {i//50+1}: added {len(batch)}, workspace total: {count}")
    except Exception as e:
        print(f"  Batch {i//50+1}: ERROR: {e}")
        time.sleep(5)

# Final count
time.sleep(3)
req = urllib.request.Request(f"{base}/workspace/{slug}",
    headers={"Authorization": f"Bearer {api_key}"})
resp = json.loads(urllib.request.urlopen(req).read())
ws = resp.get("workspace", resp)
if isinstance(ws, list): ws = ws[0]
final = len(ws.get("documents", []))
print(f"\nFinal workspace docs: {final}")
PYEOF
