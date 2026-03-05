#!/bin/bash
# =============================================================================
# GusEngine V10 — Full Service Startup Script
# Run after pod resume: bash /workspace/GusEngine/start_all.sh
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
    export $(grep -v '^#' "$WORKSPACE/.env" | xargs)
    echo "  -> Secrets loaded from .env"
else
    echo "  -> WARNING: No .env found, LLM_API_KEY must be set manually"
fi


echo "=========================================="
echo "  GusEngine V10 — Starting All Services"
echo "=========================================="

# --- 0. System tuning ---
echo "[0/3] Applying system tuning..."
ulimit -n 65535
# Kill Jupyter if it's hogging port 8888
pkill -f jupyter 2>/dev/null || true
echo "  -> ulimit -n set to 65535"

# --- 1. Qdrant (vector store) ---
echo "[1/3] Starting Qdrant..."
if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo "  -> Qdrant already running"
else
    nohup /workspace/qdrant > "$LOG_DIR/qdrant.log" 2>&1 &
    echo "  -> Waiting for Qdrant..."
    for i in $(seq 1 30); do
        if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
            echo "  -> Qdrant ready"
            break
        fi
        sleep 1
    done
    if ! curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
        echo "  X Qdrant failed to start -- check $LOG_DIR/qdrant.log"
        exit 1
    fi
fi

# --- 2. BGE-M3 Embedding Server (Python, persistent in /workspace) ---
echo "[2/3] Starting BGE-M3 embedding server..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "  -> Embedding server already running"
else
    cd "$WORKSPACE" && nohup /workspace/venvs/embed/bin/python3 \
        bge_m3_server.py \
        > "$LOG_DIR/tei.log" 2>&1 &
    echo "  -> BGE-M3 loading model (~30 sec)..."
fi

# --- 3. Backend API (FastAPI/uvicorn) ---
# NOTE: LLM inference uses Gemini 2.5 Flash via API — no local vLLM needed.
echo "[3/3] Starting backend (Gemini 2.5 Flash)..."
echo "  -> Waiting for embedding server..."
for i in $(seq 1 60); do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "  -> Embedding server ready"
        break
    fi
    sleep 1
done

cd "$WORKSPACE" && \
    TOKENIZER_MODEL_PATH="$WORKSPACE/storage/models/Qwen2.5-32B-Instruct-AWQ" \
    VLLM_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai" \
    TEI_BASE_URL="http://localhost:8080" \
    QDRANT_URL="http://localhost:6333" \
    VLLM_MODEL="gemini-2.5-flash" \
    LLM_API_KEY="${LLM_API_KEY:?ERROR: LLM_API_KEY not set. Create .env file.}" \
    EASYOCR_MODULE_PATH="$WORKSPACE/storage/easyocr_models" \
    SYSTEM_PROMPT_PATH="$WORKSPACE/config/system_prompt.txt" \
    ALLOWED_PDF_DIR="$WORKSPACE/storage/pdfs" \
    FAILURE_MANIFEST_PATH="$WORKSPACE/storage/extracted/.ingest_failures.log" \
    LEDGER_PATH="$WORKSPACE/config/MASTER_LEDGER.md" \
    DOCLING_MODELS_PATH="$WORKSPACE/storage/models/docling-models" \
    SYSTEM_PROMPT_TOKENS=1800 \
    MAX_CONTEXT_TOKENS=32768 \
    RESPONSE_BUDGET_TOKENS=8192 \
    LEDGER_MAX_TOKENS=2550 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    nohup /workspace/venvs/backend/bin/python3 \
        -m uvicorn backend.main:app \
        --host 0.0.0.0 --port 8888 \
        > "$LOG_DIR/backend.log" 2>&1 &

# --- Final health checks ---
echo ""
echo "Waiting for all services to become healthy..."
sleep 10

PASS=0
FAIL=0

for svc in "http://localhost:6333/healthz Qdrant" "http://localhost:8080/health Embedding" "http://localhost:8888/api/health Backend"; do
    url=$(echo $svc | awk '{print $1}')
    name=$(echo $svc | awk '{print $2}')
    if curl -s "$url" > /dev/null 2>&1; then
        echo "  OK $name"
        PASS=$((PASS+1))
    else
        echo "  X $name NOT READY (may still be loading)"
        FAIL=$((FAIL+1))
    fi
done

echo ""
echo "=========================================="
echo "  $PASS/3 services started"
echo "  LLM: Gemini 2.5 Flash (API — no local vLLM)"
if [ $FAIL -gt 0 ]; then
    echo "  $FAIL service(s) may still be loading."
    echo "  Check logs: tail -f $LOG_DIR/{qdrant,tei,backend}.log"
fi
echo "  Backend API: http://localhost:8888"
echo "=========================================="
