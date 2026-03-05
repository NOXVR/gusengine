#!/bin/bash
pkill -f sync_ingest 2>/dev/null || true
pkill -f python3 2>/dev/null || true
sleep 1
REMAINING=$(ps aux | grep -E 'sync_ingest|python3.*ingest' | grep -v grep | wc -l)
CHUNKS=$(ls ~/diagnostic_engine/storage/documents/custom-documents/*.json 2>/dev/null | wc -l)
echo "Ingestion processes: $REMAINING"
echo "Remaining chunk files: $CHUNKS"
echo "LanceDB exists: $(test -d ~/diagnostic_engine/storage/lancedb/1975-mercedes-benz-450sl.lance && echo YES || echo NO)"
echo ""
echo "System is clean. Ready for rethink."
