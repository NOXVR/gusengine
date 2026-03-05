#!/bin/bash
# Full reset: purge stale chunks, clear workspace, re-ingest v2 watermarked PDFs
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"
DOC_STORE="/home/ubuntu/diagnostic_engine/storage/documents/custom-documents"

echo "=== Step 1: Delete ALL workspace embeddings ==="
CURRENT=$(curl -s "$BASE/workspace/$SLUG" -H "Authorization: Bearer $API_KEY" | \
  python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list): ws = ws[0]
docs = ws.get('documents', [])
paths = [d.get('docpath','') for d in docs if d.get('docpath')]
json.dump(paths, open('/tmp/del_all.json','w'))
print(len(paths))
")
echo "Deleting $CURRENT documents from workspace..."

if [ "$CURRENT" -gt 0 ]; then
    DELETES=$(cat /tmp/del_all.json)
    curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"adds\": [], \"deletes\": $DELETES}" > /dev/null
fi

echo ""
echo "=== Step 2: Purge ALL cached document chunks ==="
BEFORE=$(ls "$DOC_STORE" 2>/dev/null | wc -l)
rm -f "$DOC_STORE"/*.json
AFTER=$(ls "$DOC_STORE" 2>/dev/null | wc -l)
echo "Deleted $BEFORE chunk files, remaining: $AFTER"

echo ""
echo "=== Step 3: Verify workspace is empty ==="
sleep 2
REMAINING=$(curl -s "$BASE/workspace/$SLUG" -H "Authorization: Bearer $API_KEY" | \
  python3 -c "
import sys, json
raw = json.load(sys.stdin)
ws = raw.get('workspace', raw)
if isinstance(ws, list): ws = ws[0]
print(len(ws.get('documents', [])))
")
echo "Workspace documents: $REMAINING"

echo ""
echo "=== Step 4: Launch re-ingestion of v2 watermarked PDFs ==="
# Update sync_ingest to use watermarked_manuals
sed 's|extracted_manuals|watermarked_manuals|' /home/ubuntu/diagnostic_engine/sync_ingest.py > /home/ubuntu/diagnostic_engine/sync_ingest_v3.py

nohup /home/ubuntu/diagnostic_engine/venv/bin/python3 -u /home/ubuntu/diagnostic_engine/sync_ingest_v3.py > /home/ubuntu/diagnostic_engine/ingestion_v3.log 2>&1 &
echo "Re-ingestion started as PID: $!"
echo "Monitor: tail -f ~/diagnostic_engine/ingestion_v3.log"
echo "Count: grep -c EMBEDDED ~/diagnostic_engine/ingestion_v3.log"
