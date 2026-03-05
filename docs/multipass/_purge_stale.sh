#!/bin/bash
# Purge ALL old (un-watermarked) document chunks and reset vector DB
# Then re-embed only the watermarked documents
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"
STORAGE="/home/ubuntu/diagnostic_engine/storage"

echo "=== Step 1: Stop and backup ==="
echo "Doc store before: $(ls $STORAGE/documents/custom-documents/ | wc -l) chunk files"

echo ""
echo "=== Step 2: Identify and delete un-watermarked chunk files ==="
python3 << 'PYEOF'
import os, json, re

doc_dir = "/home/ubuntu/diagnostic_engine/storage/documents/custom-documents"
files = [f for f in os.listdir(doc_dir) if f.endswith(".json")]
print(f"Total files before: {len(files)}")

deleted = 0
kept = 0
for fname in files:
    path = os.path.join(doc_dir, fname)
    try:
        with open(path) as f:
            data = json.load(f)
        content = data.get("pageContent", "")
        if "[[ABSOLUTE_PAGE:" not in content:
            os.remove(path)
            deleted += 1
        else:
            kept += 1
    except Exception as e:
        print(f"Error processing {fname}: {e}")
        os.remove(path)
        deleted += 1

print(f"Deleted (un-watermarked): {deleted}")
print(f"Kept (watermarked): {kept}")
PYEOF

echo ""
echo "Doc store after: $(ls $STORAGE/documents/custom-documents/ | wc -l) chunk files"

echo ""
echo "=== Step 3: Reset workspace vectors ==="
# Delete the LanceDB table to force re-indexing
RESULT=$(curl -s -X DELETE "$BASE/workspace/$SLUG/reset-vector-db" \
  -H "$AUTH" \
  -H "Content-Type: application/json" 2>/dev/null || echo "reset endpoint not available")
echo "Vector reset result: $RESULT"

echo ""
echo "=== Step 4: Get list of watermarked documents ==="
# List the remaining (watermarked) document files and re-embed them
python3 << 'PYEOF'
import os, json

doc_dir = "/home/ubuntu/diagnostic_engine/storage/documents/custom-documents"
files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".json")])
print(f"Watermarked documents to re-embed: {len(files)}")

# Build the adds array for the workspace update-embeddings endpoint
# The docpath format is: custom-documents/filename.json
adds = [f"custom-documents/{f}" for f in files]

with open("/tmp/embed_adds.json", "w") as f:
    json.dump(adds, f)
print(f"Saved adds list to /tmp/embed_adds.json")
print(f"First 3: {adds[:3]}")
PYEOF

echo ""
echo "=== Step 5: Re-embed all watermarked documents into workspace ==="
ADDS_JSON=$(cat /tmp/embed_adds.json)
echo "Adding $(echo $ADDS_JSON | python3 -c 'import sys,json; print(len(json.load(sys.stdin)))') documents to workspace..."

RESULT=$(curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"adds\": $ADDS_JSON, \"deletes\": []}")
echo "$RESULT" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', {})
docs = ws.get('documents', [])
print(f'Workspace now has {len(docs)} documents')
" 2>/dev/null || echo "$RESULT" | head -3

echo ""
echo "=== Step 6: Verify watermarks in workspace ==="
# Wait a moment for indexing
sleep 5
curl -s "$BASE/workspace/$SLUG" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get('documents', [])
print(f'Documents in workspace: {len(docs)}')
"
