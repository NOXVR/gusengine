#!/bin/bash
set -e

# Always work from /app
cd /app

# Restore Qdrant backup on first boot if collection doesn't exist
echo "Checking Qdrant status..."
for i in {1..30}; do
    if curl -sf http://qdrant:6333/healthz > /dev/null 2>&1; then
        echo "Qdrant is healthy"
        # Check if collection exists
        COLLECTION_STATUS=$(curl -sf http://qdrant:6333/collections/fsm_corpus 2>/dev/null || echo "NOT_FOUND")
        if echo "$COLLECTION_STATUS" | grep -q '"status":"ok"'; then
            POINTS=$(echo "$COLLECTION_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('points_count',0))" 2>/dev/null || echo "0")
            echo "Collection fsm_corpus exists with $POINTS points"
            if [ "$POINTS" -gt "0" ]; then
                echo "Data already loaded, skipping restore"
                break
            fi
        fi
        
        # Restore from backup if we have one
        if [ -f /app/storage/backups/qdrant_backup.tar.gz ]; then
            echo "Restoring Qdrant data from backup..."
            SNAP_DIR="/tmp/qdrant_restore"
            mkdir -p "$SNAP_DIR"
            tar xzf /app/storage/backups/qdrant_backup.tar.gz -C "$SNAP_DIR"
            
            # Find and upload snapshot files
            if ls "$SNAP_DIR"/*.snapshot 1>/dev/null 2>&1; then
                for snap in "$SNAP_DIR"/*.snapshot; do
                    COLLECTION=$(basename "$snap" | sed 's/-.*//')
                    echo "Restoring collection: $COLLECTION from $snap"
                    curl -sf -X POST "http://qdrant:6333/collections/$COLLECTION/snapshots/upload" \
                        -H "Content-Type: multipart/form-data" \
                        -F "snapshot=@$snap" || echo "Snapshot restore failed, will try direct copy"
                done
            else
                echo "No snapshot files found in backup, data may need manual restore"
            fi
            rm -rf "$SNAP_DIR"
        fi
        break
    fi
    echo "Waiting for Qdrant... ($i/30)"
    sleep 2
done

echo "Starting GusEngine backend..."
exec python -m uvicorn backend.main:app --host 0.0.0.0 --port 8888
