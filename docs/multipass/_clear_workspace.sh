#!/bin/bash
# Delete ALL existing documents from the AnythingLLM workspace
# so we can re-ingest watermarked versions
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"

echo "=== Step 1: Get list of all documents in workspace ==="
DOC_LIST=$(curl -s "$BASE/workspace/$SLUG" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get('documents', [])
print(len(docs))
for d in docs:
    print(d.get('docpath', d.get('name', 'unknown')))
")
DOC_COUNT=$(echo "$DOC_LIST" | head -1)
echo "Found $DOC_COUNT documents"

if [ "$DOC_COUNT" -eq 0 ]; then
    echo "No documents to delete. Workspace is already clean."
    exit 0
fi

echo ""
echo "=== Step 2: Delete all documents from workspace ==="
# AnythingLLM API: POST /workspace/{slug}/update-embeddings with deletes array
# First get the document names/paths
DOCPATHS=$(echo "$DOC_LIST" | tail -n +2)

# Build the deletes JSON array
DELETES_JSON=$(echo "$DOCPATHS" | python3 -c "
import sys, json
paths = [line.strip() for line in sys.stdin if line.strip()]
print(json.dumps(paths))
")
echo "Deleting $DOC_COUNT documents..."

RESULT=$(curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"adds\": [], \"deletes\": $DELETES_JSON}")
echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"

echo ""
echo "=== Step 3: Verify workspace is empty ==="
REMAINING=$(curl -s "$BASE/workspace/$SLUG" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get('documents', [])
print(len(docs))
")
echo "Documents remaining: $REMAINING"

if [ "$REMAINING" -eq 0 ]; then
    echo "SUCCESS: Workspace is clean. Ready for re-ingestion."
else
    echo "WARNING: $REMAINING documents still in workspace."
fi
