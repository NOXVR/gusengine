#!/bin/bash
# =============================================================================
# GusEngine V10 — Service Startup Script
# Run after pod resume: bash /workspace/GusEngine/start_all.sh
#
# This script handles pre-flight setup, then delegates ALL process management
# to supervisord. Individual services should NEVER be started manually.
# =============================================================================
set -e

WORKSPACE="/workspace/GusEngine"
LOG_DIR="/workspace"

# --- 0a. Sync code from GitHub ---
echo "[sync] Pulling latest code from GitHub..."
cd "$WORKSPACE"
if [ -d ".git" ]; then
    git pull --ff-only origin main 2>&1 || echo "  -> Git pull failed (offline?), using existing code"
else
    echo "  -> No git repo found, skipping sync"
fi

# --- 0b. Load secrets from .env ---
if [ -f "$WORKSPACE/.env" ]; then
    set -a
    source "$WORKSPACE/.env"
    set +a
    echo "  -> Secrets loaded from .env"
else
    echo "  !! ERROR: No .env found. Copy .env.template to .env and set LLM_API_KEY."
    echo "  !! Run: cp $WORKSPACE/.env.template $WORKSPACE/.env && nano $WORKSPACE/.env"
    exit 1
fi

# Validate required secrets
if [ -z "$LLM_API_KEY" ]; then
    echo "  !! ERROR: LLM_API_KEY is empty. Set it in $WORKSPACE/.env"
    exit 1
fi

echo "=========================================="
echo "  GusEngine V10 — Starting All Services"
echo "=========================================="

# --- 1. System tuning ---
echo "[tuning] Applying system settings..."
ulimit -n 65535
pkill -f jupyter 2>/dev/null || true
echo "  -> ulimit -n set to 65535"

# --- 2. Install supervisord if missing ---
if ! command -v supervisord &> /dev/null; then
    echo "[install] Installing supervisord..."
    pip install supervisor 2>&1 | tail -1
    echo "  -> supervisord installed"
else
    echo "  -> supervisord found"
fi

# --- 3. Stop any existing supervisord/services ---
if [ -f /workspace/supervisord.pid ]; then
    echo "[cleanup] Stopping existing supervisord..."
    supervisorctl -c "$WORKSPACE/supervisord.conf" shutdown 2>/dev/null || true
    sleep 2
fi
# Kill any orphaned processes from manual restarts
pkill -f "uvicorn backend.main" 2>/dev/null || true
pkill -f "bge_m3_server" 2>/dev/null || true
# Don't kill Qdrant here — supervisord will manage it

# --- 4. Start supervisord (manages ALL services) ---
echo "[supervisord] Starting process manager..."
supervisord -c "$WORKSPACE/supervisord.conf"
echo "  -> supervisord started"

# --- 5. Wait for services to become healthy ---
echo ""
echo "Waiting for all services to become healthy..."

# Wait for Qdrant (up to 30s)
echo -n "  Qdrant: "
for i in $(seq 1 30); do
    if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
        echo "OK"
        break
    fi
    sleep 1
done
if ! curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo "WAITING (check: supervisorctl -c $WORKSPACE/supervisord.conf status)"
fi

# Wait for Embedding server (up to 60s — model takes ~30s to load)
echo -n "  Embedding: "
for i in $(seq 1 60); do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "OK"
        break
    fi
    sleep 1
done
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "LOADING (BGE-M3 model takes ~30s, check: tail -f /workspace/tei.log)"
fi

# Wait for Backend (up to 30s)
echo -n "  Backend: "
for i in $(seq 1 30); do
    if curl -s http://localhost:8888/api/health > /dev/null 2>&1; then
        echo "OK"
        break
    fi
    sleep 1
done
if ! curl -s http://localhost:8888/api/health > /dev/null 2>&1; then
    echo "WAITING (check: tail -f /workspace/backend.log)"
fi

# --- 6. Status summary ---
echo ""
echo "=========================================="

PASS=0
for svc in "http://localhost:6333/healthz Qdrant" "http://localhost:8080/health Embedding" "http://localhost:8888/api/health Backend"; do
    url=$(echo $svc | awk '{print $1}')
    name=$(echo $svc | awk '{print $2}')
    if curl -s "$url" > /dev/null 2>&1; then
        PASS=$((PASS+1))
    fi
done

echo "  $PASS/3 services healthy"
echo "  LLM: Gemini 2.5 Flash (API)"
echo "  Process Manager: supervisord"
echo ""
echo "  Manage services:"
echo "    supervisorctl -c $WORKSPACE/supervisord.conf status"
echo "    supervisorctl -c $WORKSPACE/supervisord.conf restart backend"
echo "    supervisorctl -c $WORKSPACE/supervisord.conf tail -f backend"
echo ""
echo "  Logs:"
echo "    tail -f /workspace/{qdrant,tei,backend}.log"
echo "  Backend API: http://localhost:8888"
echo "=========================================="

# --- 7. Qdrant Backup (all vehicle collections) ---
# V10 FIREWALL: Back up all registered vehicle collections, not just fsm_corpus.
if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo ""
    # Read collection names from vehicle registry
    REGISTRY_PATH="$WORKSPACE/config/vehicle_registry.json"
    if [ -f "$REGISTRY_PATH" ]; then
        COLLECTIONS=$(python3 -c "import json; r=json.load(open('$REGISTRY_PATH')); print(' '.join(v['collection'] for v in r.get('vehicles',[])))" 2>/dev/null || echo "fsm_corpus")
    else
        COLLECTIONS="fsm_corpus"
    fi
    for COLL in $COLLECTIONS; do
        POINTS=$(curl -s "http://localhost:6333/collections/$COLL" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('points_count',0))" 2>/dev/null || echo "0")
        if [ "$POINTS" -gt "0" ] 2>/dev/null; then
            echo "[backup] $COLL has $POINTS points — creating snapshot..."
            curl -s -X POST "http://localhost:6333/collections/$COLL/snapshots" > /dev/null 2>&1
        else
            echo "[backup] $COLL has 0 points — skipping"
        fi
    done
    # Full Qdrant storage backup
    cd "$WORKSPACE/storage" && tar czf /workspace/qdrant_backup.tar.gz qdrant/ 2>/dev/null
    BACKUP_SIZE=$(ls -lh /workspace/qdrant_backup.tar.gz 2>/dev/null | awk '{print $5}')
    echo "  -> Full backup saved: /workspace/qdrant_backup.tar.gz ($BACKUP_SIZE)"
fi
