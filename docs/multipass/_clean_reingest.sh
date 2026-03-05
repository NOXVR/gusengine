#!/bin/bash
# Clean workspace and start fresh ingestion with original un-watermarked PDFs
set -euo pipefail

echo "=== Killing any background ingestion ==="
pkill -f sync_ingest 2>/dev/null || true
sleep 2

echo "=== Purging corrupted chunk files ==="
BEFORE=$(ls ~/diagnostic_engine/storage/documents/custom-documents/*.json 2>/dev/null | wc -l)
rm -f ~/diagnostic_engine/storage/documents/custom-documents/*.json
echo "Deleted $BEFORE chunk files"

echo "=== Deleting LanceDB vector table ==="
rm -rf ~/diagnostic_engine/storage/lancedb/1975-mercedes-benz-450sl.lance
echo "Done"

echo "=== Restarting container ==="
docker restart diagnostic_rag_engine
sleep 15
docker ps --format '{{.Names}} {{.Status}}'

echo ""
echo "=== Checking workspace ==="
DOCS=$(curl -s 'http://127.0.0.1:3001/api/v1/workspace/1975-mercedes-benz-450sl' \
  -H 'Authorization: Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ' | \
  python3 -c 'import sys,json; r=json.load(sys.stdin); ws=r.get("workspace",r); ws=ws[0] if isinstance(ws,list) else ws; print(len(ws.get("documents",[])))')
echo "Workspace docs: $DOCS"

echo ""
echo "=== Launching clean re-ingestion from extracted_manuals/ ==="
# Use sync_ingest.py pointing to ORIGINAL un-watermarked extracted_manuals
sed 's|watermarked_manuals|extracted_manuals|' ~/diagnostic_engine/sync_ingest.py > ~/diagnostic_engine/sync_ingest_clean.py 2>/dev/null || \
  cp ~/diagnostic_engine/sync_ingest.py ~/diagnostic_engine/sync_ingest_clean.py

# Verify it points to extracted_manuals
grep "CHUNKS_DIR\|extracted_manuals\|watermarked_manuals" ~/diagnostic_engine/sync_ingest_clean.py || echo "(no grep match)"

nohup ~/diagnostic_engine/venv/bin/python3 -u ~/diagnostic_engine/sync_ingest_clean.py > ~/diagnostic_engine/ingestion_clean.log 2>&1 &
echo "Clean re-ingestion started as PID: $!"
echo "Monitor: tail -f ~/diagnostic_engine/ingestion_clean.log"
echo "Count: grep -c EMBEDDED ~/diagnostic_engine/ingestion_clean.log"
