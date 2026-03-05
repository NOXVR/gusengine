#!/bin/bash
# Re-embed densified documents and test citations
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"

echo "=== Step 1: Remove all current workspace docs ==="
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
print(f"Current docs: {len(paths)}")

if paths:
    data = json.dumps({"adds": [], "deletes": paths}).encode()
    req2 = urllib.request.Request(f"{base}/workspace/{slug}/update-embeddings",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    resp2 = json.loads(urllib.request.urlopen(req2).read())
    remaining = len(resp2.get("workspace", {}).get("documents", []))
    print(f"After delete: {remaining}")
PYEOF

echo ""
echo "=== Step 2: Add all densified docs ==="
python3 << 'PYEOF'
import json, urllib.request, os

api_key = "S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
base = "http://127.0.0.1:3001/api/v1"
slug = "1975-mercedes-benz-450sl"
doc_dir = os.path.expanduser("~/diagnostic_engine/storage/documents/custom-documents")

files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".json")])
adds = [f"custom-documents/{f}" for f in files]
print(f"Adding {len(adds)} documents...")

# Add in batches of 100
for i in range(0, len(adds), 100):
    batch = adds[i:i+100]
    data = json.dumps({"adds": batch, "deletes": []}).encode()
    req = urllib.request.Request(f"{base}/workspace/{slug}/update-embeddings",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    count = len(resp.get("workspace", {}).get("documents", []))
    print(f"  Batch {i//100+1}: added {len(batch)}, workspace total: {count}")

# Final count
req = urllib.request.Request(f"{base}/workspace/{slug}",
    headers={"Authorization": f"Bearer {api_key}"})
resp = json.loads(urllib.request.urlopen(req).read())
ws = resp.get("workspace", resp)
if isinstance(ws, list): ws = ws[0]
print(f"\nFinal workspace docs: {len(ws.get('documents', []))}")
PYEOF

echo ""
echo "=== Step 3: Citation test ==="
sleep 3
# Create fresh thread and test
python3 << 'PYEOF'
import json, urllib.request, re, time

api_key = "S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
base = "http://127.0.0.1:3001/api/v1"
slug = "1975-mercedes-benz-450sl"

# New thread
data = json.dumps({}).encode()
req = urllib.request.Request(f"{base}/workspace/{slug}/thread/new",
    data=data,
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
resp = json.loads(urllib.request.urlopen(req).read())
thread = resp["thread"]["slug"]
print(f"Thread: {thread}")

# Send query
msg = "K-Jetronic fuel pressure test procedure for 1975 Mercedes 450SL"
data = json.dumps({"message": msg, "mode": "chat"}).encode()
req = urllib.request.Request(f"{base}/workspace/{slug}/thread/{thread}/chat",
    data=data,
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
print(f"Sending: {msg}")
resp = json.loads(urllib.request.urlopen(req).read())

text = resp.get("textResponse", "")
sources = resp.get("sources", [])
print(f"\nResponse: {len(text)} chars, {len(sources)} sources")

# Check sources for watermarks
print("\n=== SOURCE CHUNK WATERMARK CHECK ===")
for i, s in enumerate(sources):
    content = s.get("text", "")
    tags = re.findall(r'\[\[ABSOLUTE_PAGE: \d+\]\]', content)
    title = s.get("title", "?")
    print(f"  [{i+1}] {title[:60]}")
    print(f"      Tags in chunk: {tags[:3]}{'...' if len(tags)>3 else ''}")
    print(f"      Has watermark: {'YES' if tags else 'NO'}")

# Parse Gus JSON
print("\n=== GUS CITATIONS ===")
try:
    start = text.index("{")
    end = text.rindex("}") + 1
    parsed = json.loads(text[start:end])
    citations = parsed.get("source_citations", [])
    for c in citations:
        page = c.get("page", "MISSING")
        source = c.get("source", "?")
        print(f"  page: {page} | source: {source[:60]}")
    
    has_real = any(c.get("page") not in ["unknown", "MISSING", None] for c in citations)
    if has_real:
        print("\nCITATION TEST: PASS — page numbers are real")
    else:
        print("\nCITATION TEST: FAIL — pages still unknown")
except Exception as e:
    print(f"Parse error: {e}")
    print(f"Response: {text[:500]}")
PYEOF
