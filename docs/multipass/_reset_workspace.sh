#!/bin/bash
# Full workspace reset: remove ALL docs, then add ONLY watermarked ones
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"

echo "=== Step 1: Get all current workspace documents ==="
CURRENT_DOCS=$(curl -s "$BASE/workspace/$SLUG" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get('documents', [])
paths = [d.get('docpath','') for d in docs if d.get('docpath')]
print(len(paths))
import json as j
j.dump(paths, open('/tmp/current_docs.json','w'))
")
echo "Current workspace docs: $CURRENT_DOCS"

echo ""
echo "=== Step 2: Delete ALL from workspace ==="
DELETES=$(cat /tmp/current_docs.json)
RESULT=$(curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"adds\": [], \"deletes\": $DELETES}")
echo "Delete result docs remaining: $(echo $RESULT | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', {})
print(len(ws.get('documents', [])))
" 2>/dev/null || echo 'unknown')"

echo ""
echo "=== Step 3: Wait for vector DB to settle ==="
sleep 5

echo ""
echo "=== Step 4: Add ONLY watermarked documents ==="
ADDS=$(cat /tmp/embed_adds.json)
ADD_COUNT=$(echo "$ADDS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
echo "Adding $ADD_COUNT watermarked documents..."
RESULT=$(curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"adds\": $ADDS, \"deletes\": []}")
FINAL_COUNT=$(echo "$RESULT" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', {})
print(len(ws.get('documents', [])))
" 2>/dev/null || echo 'unknown')
echo "Final workspace document count: $FINAL_COUNT"

echo ""
echo "=== Step 5: Quick sanity check ==="
sleep 3
curl -s "$BASE/workspace/$SLUG" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get('documents', [])
print(f'Workspace docs: {len(docs)}')
print(f'Vector token count: {ws.get(\"currentContextTokenCount\", \"?\")}')
"
