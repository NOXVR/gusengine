#!/bin/bash
set -e

# Always work from /app
cd /app

# Restore Qdrant backup on first boot if collection doesn't exist
echo "Checking Qdrant status..."
for i in {1..30}; do
    if curl -sf http://qdrant:6333/healthz > /dev/null 2>&1; then
        echo "Qdrant is healthy"

        # V11 HARDENING: Check ALL registered vehicle collections and warn loudly
        REGISTRY="/app/config/vehicle_registry.json"
        if [ -f "$REGISTRY" ]; then
            COLLECTIONS=$(python3 -c "import json; r=json.load(open('$REGISTRY')); print(' '.join(v['collection'] for v in r.get('vehicles',[])))" 2>/dev/null || echo "fsm_corpus")
            VEHICLE_COUNT=$(python3 -c "import json; r=json.load(open('$REGISTRY')); print(len(r.get('vehicles',[])))" 2>/dev/null || echo "0")
        else
            COLLECTIONS="fsm_corpus"
            VEHICLE_COUNT="1"
            echo "WARNING: vehicle_registry.json not found, using fallback"
        fi

        HEALTHY=0
        UNHEALTHY=0
        MISSING_LIST=""
        EMPTY_LIST=""
        ALL_EXIST=true

        for COLL in $COLLECTIONS; do
            COLL_STATUS=$(curl -sf "http://qdrant:6333/collections/$COLL" 2>/dev/null || echo "NOT_FOUND")
            if echo "$COLL_STATUS" | grep -q '"status":"ok"'; then
                POINTS=$(echo "$COLL_STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('points_count',0))" 2>/dev/null || echo "0")
                if [ "$POINTS" -gt 0 ] 2>/dev/null; then
                    echo "[OK] Collection $COLL: $POINTS points"
                    HEALTHY=$((HEALTHY + 1))
                else
                    echo "[WARN] Collection $COLL exists but has 0 points!"
                    EMPTY_LIST="$EMPTY_LIST $COLL"
                    UNHEALTHY=$((UNHEALTHY + 1))
                fi
            else
                echo "[MISS] Collection $COLL does not exist (will be created by backend)"
                MISSING_LIST="$MISSING_LIST $COLL"
                ALL_EXIST=false
                UNHEALTHY=$((UNHEALTHY + 1))
            fi
        done

        echo ""
        echo "=== DEPLOYMENT INTEGRITY CHECK ==="
        echo "  Registered vehicles: $VEHICLE_COUNT"
        echo "  Collections healthy: $HEALTHY"
        echo "  Collections issues:  $UNHEALTHY"
        if [ -n "$MISSING_LIST" ]; then
            echo "  MISSING:$MISSING_LIST"
        fi
        if [ -n "$EMPTY_LIST" ]; then
            echo "  EMPTY:$EMPTY_LIST"
        fi
        if [ "$UNHEALTHY" -gt 0 ]; then
            echo "  >>> WARNING: $UNHEALTHY collection(s) need attention! <<<"
        else
            echo "  >>> ALL COLLECTIONS VERIFIED <<<"
        fi
        echo "==================================="
        echo ""

        # Restore from backup if we have one and any collection is missing data
        if [ "$ALL_EXIST" = false ] && [ -f /app/storage/backups/qdrant_backup.tar.gz ]; then
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
