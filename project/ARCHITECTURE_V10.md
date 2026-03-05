# ARCHITECTURE_V10.md

**SYSTEM:** Closed-Loop Automotive Diagnostic RAG Engine
**VERSION:** V10 (Full Pipeline Redesign — Local-First, Air-Gapped, GPU-Feasible Prototype)
**CLASSIFICATION:** ZERO-TOLERANCE / LIFE-SAFETY ADJACENT
**HARDWARE TARGET:** Dual NVIDIA RTX 4090 (2 × 24 GB = 48 GB VRAM)
**DATE:** 2026-02-24
**PREDECESSOR:** `ARCHITECTURE_FINAL_V9_FROZEN.md` (2107 lines, 49 verified audit findings)

**STATUS:** DRAFT — PENDING TRIAD VALIDATION

---

### CRITICAL ARCHITECTURAL PREFACE

This document supersedes all V9 pipeline components (Phases 4, 5, 7, 8 RAG parameters) while preserving validated V9 infrastructure, state machine logic, and operational tooling. The V9.3 Deprecation Notice identified 7 critical gaps vs. NotebookLM benchmark. V10 resolves all 7 by replacing the entire RAG pipeline with a local-first, GPU-feasible stack.

**V10 Design Principles:**

1. **Prototype-First:** Accept model fallibility for proof-of-concept. Cloud scale-up is a future MVP consideration.
2. **Air-Gap Mandatory:** Zero external API calls at inference time. All models run locally on dual RTX 4090s.
3. **NotebookLM is the Floor:** Match or exceed NotebookLM's structural chunking, cross-document retrieval, and citation granularity.
4. **V9 Heritage Preserved:** Infrastructure (Phases 1-3), DAG state machine, `parseGusResponse()`, `buildUserMessage()`, VMDK/OVA extraction, TOCTOU locking, three-tier quarantine, tribal knowledge — all carried forward.
5. **Triple-Validated:** Every component choice confirmed by ≥2 of 3 independent auditors (Gemini Deep Think, Claude Opus, Gemini Deep Research).

**V10 Changelog (from V9.3 Frozen):**
- LLM replaced: Claude 3.5 Sonnet (API) → Qwen2.5-32B-Instruct-AWQ (local, vLLM)
- Inference server added: vLLM with tensor parallelism across 2× RTX 4090
- Parser replaced: PyMuPDF flat text → Docling (IBM) with EasyOCR for scanned PDFs
- Embedding replaced: Voyage AI (API) → BGE-M3 via HuggingFace TEI (local)
- Vector store replaced: LanceDB (embedded) → Qdrant ≥ v1.15.2 (containerized)
- Reranker removed: Cohere API dropped; RRF fusion + dynamic threshold sufficient for prototype
- Token counting replaced: tiktoken cl100k_base → AutoTokenizer (native Qwen2.5 tokenizer)
- Chunking replaced: 5-page physical + 400-char RecursiveTextSplitter → Docling HybridChunker (structural)
- Context budget expanded: 4K total → 32K total (~25K usable RAG budget, 6× improvement)
- Frontend replaced: AnythingLLM Web UI → Custom React with PDF.js citation rendering (self-hosted)
- Orchestration replaced: AnythingLLM (all-in-one) → Custom FastAPI backend
- Deployment replaced: Single Docker container + systemd → Docker Compose (multi-container, GPU passthrough)
- Search upgraded: Vector-only → Hybrid dense + sparse + RRF fusion (Qdrant native)
- Relevance threshold: Fixed 0.50 → Dynamic 70% of top RRF score

---

## COMPONENT MAP

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HOST MACHINE (Ubuntu)                        │
│                     Dual RTX 4090 (48 GB VRAM)                      │
│                                                                     │
│  ┌──────────────────────────── Docker Compose ────────────────────┐ │
│  │                                                                │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │ │
│  │  │   vLLM        │  │  TEI          │  │  Qdrant              │ │ │
│  │  │  Qwen2.5-32B  │  │  BGE-M3       │  │  v1.15.2+            │ │ │
│  │  │  AWQ 4-bit    │  │  Embedding    │  │  Hybrid Search       │ │ │
│  │  │  TP=2 (both   │  │  Server       │  │  Dense + Sparse      │ │ │
│  │  │  GPUs)        │  │  (GPU 0)      │  │  (CPU + Disk)        │ │ │
│  │  │  Port: 8000   │  │  Port: 8080   │  │  Port: 6333          │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │ │
│  │                                                                │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │                   GusEngine (FastAPI)                     │  │ │
│  │  │  • /api/chat  — RAG orchestration + DAG enforcement      │  │ │
│  │  │  • /api/ingest — Docling parsing + Qdrant indexing       │  │ │
│  │  │  • /api/health — Service readiness probe                 │  │ │
│  │  │  Port: 8888                                              │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  │                                                                │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │                React Frontend (Nginx)                    │  │ │
│  │  │  • PDF.js viewer (self-hosted, NO CDN)                   │  │ │
│  │  │  • Citation bbox overlays                                │  │ │
│  │  │  • DAG button rendering                                  │  │ │
│  │  │  Port: 443 (TLS)                                        │  │ │
│  │  └──────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─────────── Host Services (systemd) ───────────┐                  │
│  │  manual-ingest.service (V9 VMDK/OVA daemon)   │                  │
│  │  → Feeds extracted PDFs to /api/ingest         │                  │
│  └────────────────────────────────────────────────┘                  │
│                                                                     │
│  ┌─────────── Volumes ───────────────────────────┐                  │
│  │  ./storage/qdrant    — Qdrant persistence     │                  │
│  │  ./storage/models    — Qwen2.5 + BGE-M3       │                  │
│  │  ./storage/pdfs      — Original PDFs (display) │                  │
│  │  ./storage/extracted — Docling output cache    │                  │
│  └────────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## GPU MEMORY BUDGET

> [!CAUTION]
> **ALL THREE AUDITORS UNANIMOUSLY CONFIRM:** Llama 3.1 70B + 128K context is physically impossible on 48 GB VRAM. The math below proves Qwen2.5-32B-AWQ @ 32K context is feasible with headroom.

### VRAM Allocation (Dual RTX 4090, 48 GB total)

| Component | VRAM (GB) | Location | Notes |
|:----------|:---------:|:---------|:------|
| Qwen2.5-32B-Instruct-AWQ weights | ~18 | GPU 0 + GPU 1 (TP=2) | 4-bit AWQ quantization, ~9 GB per GPU |
| KV Cache @ 32K context | ~8 | GPU 0 + GPU 1 (TP=2) | 64 layers × 8 KV heads × 128 dim × 32K × 2 bytes × 2 (K+V) |
| vLLM overhead (CUDA kernels, buffers) | ~2 | GPU 0 + GPU 1 | PagedAttention, scheduler |
| **Subtotal: LLM** | **~28** | | **58% of 48 GB** |
| BGE-M3 embedding model | ~2 | GPU 0 | 568M params, FP16 |
| TEI runtime overhead | ~0.5 | GPU 0 | |
| **Subtotal: Embedding** | **~2.5** | | |
| **TOTAL** | **~30.5** | | **64% of 48 GB** |
| **Headroom** | **~17.5** | | OS, CUDA context, burst batches |

> [!IMPORTANT]
> **KV Cache Math (independent verification):**
> Qwen2.5-32B has 64 layers, 8 KV heads per layer (GQA), head dimension 128.
> KV cache per token = 64 × 8 × 128 × 2 (K+V) × 2 bytes (FP16) = 262,144 bytes = 0.25 MB
> At 32K tokens: 0.25 MB × 32,768 = 8,192 MB = **8 GB** ✅
> At 64K tokens: 0.25 MB × 65,536 = 16,384 MB = **16 GB** (tight but possible, ~46 GB total)
> At 128K tokens: 0.25 MB × 131,072 = 32,768 MB = **32 GB** ❌ (62.5 GB total, exceeds 48 GB)

### Future Scale-Up Path

| Target | Context | Hardware Required | Strategy |
|:-------|:-------:|:-----------------|:---------|
| **Prototype (THIS DOC)** | 32K | 2× RTX 4090 (48 GB) | AWQ-4bit, TP=2 |
| **Extended Prototype** | 64K | 2× RTX 4090 (48 GB) | AWQ-4bit, TP=2, tight budget |
| **MVP Cloud** | 128K | 1× A100-80GB or 2× A6000-48GB | FP16 or AWQ, single/dual GPU |
| **Production** | 128K+ | 2× A100-80GB (160 GB) | Full precision, maximum context |

---

## DOCKER COMPOSE SPECIFICATION

> [!CAUTION]
> **AIR-GAP ENFORCEMENT:** No container makes outbound internet requests at runtime. All model weights must be pre-downloaded to `./storage/models/` before first launch. The Docker network is **`internal: true` — containers cannot initiate outbound internet connections. Published ports (both `127.0.0.1`-bound backend services and `0.0.0.0`-bound frontend 443/80) still accept connections via iptables DNAT.**

```yaml
# docker-compose.yml — GusEngine V10
# Pre-requisite: Download models to ./storage/models/ before first launch
# Pre-requisite: NVIDIA Container Toolkit installed on host

# AUDIT FIX (P10-19): Removed deprecated 'version: "3.8"' — Docker Compose V2 ignores it
# and emits a noisy deprecation warning on every deploy.

services:
  # ─── LLM Inference (vLLM) ───
  vllm:
    # AUDIT FIX (P9-07): Pin to tested version — :latest makes builds non-reproducible.
    # vLLM releases frequently break AWQ Marlin support, healthcheck format, and chat
    # completion schema. A fresh deploy or docker compose pull could pull a breaking update.
    image: vllm/vllm-openai:v0.7.2
    container_name: gus_vllm
    restart: always
    ports:
      - "127.0.0.1:8000:8000"
    volumes:
      - ./storage/models:/models:ro
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
    command: >
      --model /models/Qwen2.5-32B-Instruct-AWQ
      --quantization awq_marlin
      --dtype float16
      --tensor-parallel-size 2
      --max-model-len 32768
      --gpu-memory-utilization 0.75  # AUDIT FIX: 0.85→0.80→0.75; GPU 0 needs room for TEI (2.5GB) + CUDA (1.5GB)
      --port 8000
      --served-model-name Qwen2.5-32B-Instruct-AWQ  # AUDIT FIX: without this, vLLM API model ID = file path, causing 404s
      --trust-remote-code
      --disable-log-requests
    networks:
      - gus_internal
    healthcheck:
      # AUDIT FIX (GP7-10): Changed from /health to /v1/models.
      # /health only checks the API HTTP listener — it returns 200 even when
      # the PagedAttention KV cache is exhausted or GPU workers are deadlocked.
      # /v1/models forces the scheduler to enumerate loaded models, confirming
      # the engine is actually functional, not just the HTTP front-end.
      test: ["CMD-SHELL", "curl -sf http://localhost:8000/v1/models || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 120s  # vLLM needs time to load 32B model
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

  # ─── Embedding Server (TEI) ───
  tei:
    # AUDIT FIX (P9-07): Pin to tested version — matches vLLM pinning rationale.
    image: ghcr.io/huggingface/text-embeddings-inference:1.5.0
    container_name: gus_tei
    restart: always
    ports:
      - "127.0.0.1:8080:80"
    volumes:
      - ./storage/models/bge-m3:/model:ro
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
    command: --model-id /model --port 80
    networks:
      - gus_internal
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:80/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

  # ─── Vector Store (Qdrant) ───
  qdrant:
    image: qdrant/qdrant:v1.15.2
    container_name: gus_qdrant
    restart: always
    ports:
      - "127.0.0.1:6333:6333"
    volumes:
      - ./storage/qdrant:/qdrant/storage
      - ./storage/snapshots:/qdrant/snapshots  # AUDIT FIX (DT-P9-04): persist snapshots across container recreates
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    networks:
      - gus_internal
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:6333/healthz || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 15s
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

  # ─── GusEngine Backend (FastAPI) ───
  gusengine:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: gus_backend
    restart: always
    ports:
      - "127.0.0.1:8888:8888"
    volumes:
      - ./storage/pdfs:/app/pdfs:ro
      - ./storage/extracted:/app/extracted
      - ./config:/app/config:ro
      - ./storage/models:/app/models:ro
      - ./storage/easyocr_models:/app/.EasyOCR/model:ro
    environment:
      - VLLM_BASE_URL=http://vllm:8000/v1
      - TEI_BASE_URL=http://tei:80
      - QDRANT_URL=http://qdrant:6333
      - EASYOCR_MODULE_PATH=/app/.EasyOCR
      - VLLM_MODEL=Qwen2.5-32B-Instruct-AWQ
      - MAX_CONTEXT_TOKENS=32768
      - SYSTEM_PROMPT_TOKENS=900
      - RESPONSE_BUDGET_TOKENS=2000
      - LEDGER_MAX_TOKENS=2550
      - HF_HUB_OFFLINE=1
      - TRANSFORMERS_OFFLINE=1
    depends_on:
      vllm:
        condition: service_healthy
      tei:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    networks:
      - gus_internal
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"
    # AUDIT FIX (P9-06): gusengine was missing a Docker healthcheck despite having /api/health.
    # During the 303s ensure_qdrant_collection() retry loop after OOM-kill restart,
    # Nginx proxies to gusengine:8888 → connection refused → HTTP 502 "Bad Gateway"
    # instead of a graceful Gus PHASE_ERROR. Healthcheck enables depends_on: condition.
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8888/api/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 5  # AUDIT FIX (OP-P11-03): was 3
      # AUDIT FIX (OP-P11-03): was 60s — doesn't cover ~303s max startup retry loop.
      # With 60s start_period, Docker marks unhealthy at ~105s while ensure_qdrant_collection()
      # retries for up to 303s. Frontend blocked for ~153s unnecessarily.
      start_period: 360s

  # ─── Frontend (React + Nginx) ───
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: gus_frontend
    restart: always
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./storage/pdfs:/usr/share/nginx/pdfs:ro
      - ./certs:/etc/nginx/ssl:ro
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      gusengine:
        condition: service_healthy  # AUDIT FIX (P9-06): was bare depends_on
    networks:
      - gus_internal
    # AUDIT FIX (P10-28): Frontend healthcheck — only service without health monitoring.
    # If Nginx master stays alive but workers crash (known failure mode under memory
    # pressure), Docker sees container as healthy. Port 80 returns 301 (P10-06 redirect).
    healthcheck:
      # AUDIT FIX (P11-12): Check for 301 status code directly instead of following
      # redirect. With self-signed certs, curl follows 301→https and fails TLS
      # verification (exit 60), causing a restart loop.
      test: ["CMD-SHELL", "curl -sfo /dev/null -w '%{http_code}' http://localhost:80/ | grep -q 301 || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

networks:
  gus_internal:
    driver: bridge
    internal: true   # TRIAD FIX (OP-1): Air-gap enforcement — blocks container egress. 127.0.0.1 port bindings still work via iptables DNAT.

```

### Model Pre-Download Commands

> [!CAUTION]
> These commands require internet access. Run them ONCE before first deployment. After download, the system operates fully air-gapped.

```bash
# Create model storage
mkdir -p ./storage/models

# Download Qwen2.5-32B-Instruct-AWQ (HuggingFace)
pip install huggingface_hub
huggingface-cli download Qwen/Qwen2.5-32B-Instruct-AWQ \
  --local-dir ./storage/models/Qwen2.5-32B-Instruct-AWQ

# Download BGE-M3 embedding model
huggingface-cli download BAAI/bge-m3 \
  --local-dir ./storage/models/bge-m3

# Pre-download EasyOCR model weights (air-gap requirement)
# TRIAD FIX (OP-5, DT-3): EasyOCR downloads ~100MB at first use, violating air-gap.
# Pre-cache the English recognition model to ./storage/easyocr_models/
python3 -c "
import easyocr
import shutil, os
reader = easyocr.Reader(['en'], gpu=False)  # downloads model on first init
src = os.path.expanduser('~/.EasyOCR/model')
dst = './storage/easyocr_models'
os.makedirs(dst, exist_ok=True)
for f in os.listdir(src):
    shutil.copy2(os.path.join(src, f), dst)
print(f'EasyOCR models cached to {dst}: {os.listdir(dst)}')
"

# AUDIT FIX (DT-P11-02): Pre-download Docling layout models (air-gap requirement).
# IBM Docling's TableFormer requires ds4sd/docling-models for table structure
# extraction. Without pre-download, HF_HUB_OFFLINE=1 blocks the fetch and
# parse_and_chunk() crashes on the first PDF with OfflineModeIsEnabled.
huggingface-cli download ds4sd/docling-models \
  --local-dir ./storage/models/docling-models

# Download PDF.js for self-hosted frontend (NO CDN)
# V10 FIX: Opus and Gemini DT both flagged R3's unpkg.com CDN dependency
# as an air-gap violation. PDF.js worker MUST be self-hosted.
# TRIAD FIX (OP-13): Use official npm registry, not third-party GitHub fork.
cd ./frontend && npm pack pdfjs-dist@4.0.379 && \
  tar xzf pdfjs-dist-4.0.379.tgz && \
  mkdir -p public/pdfjs && \
  cp package/build/* public/pdfjs/ && \
  rm -rf package pdfjs-dist-4.0.379.tgz && cd ..

# AUDIT FIX (DT-P11-04): Removed npm install dompurify — dead dependency.
# DOMPurify was mandated by DT-P3-06 but P4-04 switched all innerHTML to
# textContent, making DOMPurify unused. XSS defense is now inherent.

```

---

## INGESTION PIPELINE

### Overview

The V10 ingestion pipeline replaces V9's flat PyMuPDF text extraction with IBM Docling's structural document parser. This achieves NotebookLM-aligned structural chunking while preserving original PDFs for citation display.

```
PDF File → Docling Parser → Structural Chunks → BGE-M3 Embedding → Qdrant Index
                ↓                                                        ↑
          OCR (if scanned)                                    Dense + Sparse vectors
                ↓
        Layout Model → Tables, Headings, Figures detected
                ↓
        HybridChunker → Chunks respect document structure
```

### Docling Configuration

> [!IMPORTANT]
> **AUDIT FIX (Opus + Gemini DR):** R1's PyMuPDF extracts ZERO text from scanned PDFs. R3's Docling config was missing `do_ocr=True`. The configuration below explicitly enables OCR for all documents.

```python
# backend/ingestion/parser.py
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    EasyOcrOptions,
    TableFormerMode,
    TableStructureOptions,
)
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer  # AUDIT FIX (DT-7)
from backend.shared.tokenizer import TOKENIZER, _TOKENIZER_LOCK, count_tokens  # AUDIT FIX (P3-13 + P11-14)
import os

def create_converter():
    """Create Docling converter with OCR enabled for scanned PDFs."""
    pipeline_options = PdfPipelineOptions(
        # AUDIT FIX (DT-P11-02): Explicit offline artifacts path for TableFormer.
        # Without this, Docling attempts HF Hub download blocked by HF_HUB_OFFLINE=1.
        artifacts_path="/app/models/docling-models",
        do_ocr=True,  # CRITICAL: Must be True for scanned FSM PDFs
        ocr_options=EasyOcrOptions(
            lang=["en"],
            use_gpu=False,  # OCR on CPU to preserve GPU VRAM for LLM
            # Air-gap: runtime downloads blocked by EASYOCR_MODULE_PATH env var,
            # pre-cached models volume mount, and internal:true Docker network.
        ),
        do_table_structure=True,
        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
    )
    return DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

class IngestionError(Exception):
    """Raised when a PDF fails to parse or chunk. Caller should quarantine."""
    pass

def parse_and_chunk(pdf_path: str, max_tokens: int = 512) -> list[dict]:
    """Parse a PDF with Docling and chunk using HybridChunker.
    
    Returns list of chunks with metadata:
    - text: chunk text content
    - source: relative path under /app/pdfs/ (e.g. "brakes/manual.pdf", not just "manual.pdf")
    - page_numbers: list of page numbers this chunk spans
    - headings: hierarchical heading path
    - token_count: exact token count via native tokenizer
    
    Raises:
        IngestionError: If parsing fails after logging. Caller should
        quarantine the file and continue with the next PDF.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        converter = create_converter()
        result = converter.convert(pdf_path)
    except Exception as e:
        logger.error(f"DOCLING PARSE FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Failed to parse {pdf_path}: {e}") from e
    
    doc = result.document
    if doc is None:
        logger.error(f"DOCLING EMPTY RESULT: {pdf_path} — converter returned None document")
        raise IngestionError(f"Docling returned empty document for {pdf_path}")
    
    # AUDIT FIX (P7-01): Wrap TOKENIZER for Docling with lock protection.
    # Docling's HybridChunker calls tokenizer.encode() internally on its own
    # thread during parse_and_chunk (dispatched via asyncio.to_thread). Without
    # the lock, concurrent chat handler tokenization can corrupt the
    # trust_remote_code Python state in Qwen2.5's tokenizer.
    # AUDIT FIX (P11-14): Removed redundant function-level TOKENIZER import (now at module scope)
    # _TOKENIZER_LOCK and count_tokens also imported at module scope.
    class LockedTokenizer:
        def __init__(self, tok): self.tok = tok
        def encode(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.encode(text, **kwargs)
        # AUDIT FIX (P9-11): Add decode() with lock + __getattr__ for forward compat.
        # Only encode() is currently called by Docling's HybridChunker, but a Docling
        # upgrade could call decode(), vocab_size, __len__(), etc. Without delegation,
        # those calls raise AttributeError and crash ingestion silently.
        def decode(self, ids, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.decode(ids, **kwargs)
        # AUDIT FIX (P10-07): __getattr__ must also acquire the lock. The Qwen2.5
        # tokenizer has stateful Python code behind trust_remote_code=True — property
        # access is NOT guaranteed read-only. Without the lock, concurrent attribute
        # access from chat (count_tokens) and ingestion (Docling) can corrupt state.
        def __getattr__(self, name):
            with _TOKENIZER_LOCK: return getattr(self.tok, name)
        # AUDIT FIX (DT-P10-05): Explicit wrappers for methods Docling calls through
        # HuggingFaceTokenizer. __getattr__ locks the attribute access but not the
        # subsequent method call — these wrappers lock the entire call.
        def tokenize(self, text, **kwargs):
            with _TOKENIZER_LOCK: return self.tok.tokenize(text, **kwargs)
        def __call__(self, *args, **kwargs):
            with _TOKENIZER_LOCK: return self.tok(*args, **kwargs)
    
    chunker = HybridChunker(
        # AUDIT FIX (DT-7): Docling requires its own BaseTokenizer protocol.
        # Raw HuggingFace AutoTokenizer throws TypeError/AttributeError.
        # AUDIT FIX (P7-01): LockedTokenizer wraps TOKENIZER for thread safety.
        tokenizer=HuggingFaceTokenizer(tokenizer=LockedTokenizer(TOKENIZER)),
        max_tokens=max_tokens,
        merge_peers=True,  # Merge adjacent same-level sections
    )
    
    # AUDIT FIX (DT-P10-06): chunker.chunk(doc) returns a lazy generator.
    # Docling parsing errors fire during iteration, NOT creation. The try/except
    # must wrap the iteration loop to route errors to IngestionError quarantine.
    try:
        chunk_iter = chunker.chunk(doc)  # AUDIT FIX: lazy generator, not list() — avoids OOM on large PDFs
        chunks = []
        for chunk in chunk_iter:
            text = chunk.text
            if not text or not text.strip():
                continue  # Skip empty chunks (OCR failures on blank pages)
            token_count = count_tokens(text)  # AUDIT FIX (P7-01): was len(TOKENIZER.encode(text))
            
            # Extract page numbers from chunk metadata
            page_numbers = sorted(set(
                item.prov[0].page_no
                for item in chunk.meta.doc_items
                if item.prov
            )) if chunk.meta.doc_items else []
            
            # Extract heading hierarchy
            headings = []
            for item in (chunk.meta.headings or []):
                headings.append(item)
            
            chunks.append({
                "text": text,
                # AUDIT FIX (DT-P9-03): Preserve relative path, not just basename.
                # os.path.basename strips folder structure, causing cross-source collision
                # when identically-named files exist in different subdirectories.
                # e.g., brakes/manual.pdf and engine/manual.pdf both became "manual.pdf",
                # so /api/cleanup on "manual.pdf" would wipe BOTH manuals.
                "source": pdf_path.split("/app/pdfs/", 1)[-1] if "/app/pdfs/" in pdf_path else os.path.basename(pdf_path),
                "page_numbers": page_numbers,
                "headings": headings,
                "token_count": token_count,
            })
    except Exception as e:
        logger.error(f"CHUNKER FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Chunking failed for {pdf_path}: {e}") from e
    
    return chunks
```

### V9 Heritage: VMDK/OVA Extraction Daemon

> [!NOTE]
> The `vmdk_extractor.py` daemon from V9 Phase 4 is **PRESERVED WITH TARGETED MODIFICATIONS** for extracting PDFs from VMDK/OVA files. Core logic is unchanged: `wait_for_stable()` TOCTOU locking, three-tier quarantine defense, and manifest-based deduplication remain exactly as documented in V9 (49 verified audit findings). Three changes:
> 1. **Output path:** `./storage/pdfs/` replaces `~/diagnostic_engine/extracted_manuals/`
> 2. **`chunk_pdf()` removed:** Docling handles all chunking (see Ingestion Pipeline)
> 3. **Webhook added:** After dedup, triggers `POST /api/ingest` on localhost:8888

The daemon's `chunk_pdf()` function is **NO LONGER CALLED** — Docling handles all chunking. The daemon's role is now purely extraction and deduplication:

1. Monitor `./storage/downloads/` for VMDK/OVA/PDF files
2. Extract PDFs from VMDK/OVA containers via `guestmount`
3. SHA-256 dedup via atomic manifest
4. Copy extracted PDFs to `./storage/pdfs/` (original, unchunked)
5. Trigger `/api/ingest` webhook on the FastAPI backend

---

## EMBEDDING & INDEXING

### BGE-M3 Embedding Model

| Property | Value |
|:---------|:------|
| Model | BAAI/bge-m3 |
| Parameters | 568M |
| Dimensions | 1024 (dense) |
| Max Tokens | 8192 |
| VRAM | ~2 GB (FP16) |
| Capabilities | Dense + Sparse + ColBERT (multi-vector) |
| Server | HuggingFace TEI (GPU-accelerated) |

> [!NOTE]
> **Why BGE-M3 over bge-small-en-v1.5:** Gemini DR argued for the smaller model to save VRAM. However, BGE-M3 costs only ~2 GB VRAM and provides: (1) 1024d vs 384d vectors for better semantic separation, (2) native sparse vector output for hybrid search, (3) 8192 token input window vs 512 for bge-small. The 2 GB cost is justified by the 17.5 GB headroom available.

### Qdrant Collection Schema

```python
# backend/indexing/qdrant_setup.py
from qdrant_client import QdrantClient, models  # AUDIT FIX (DT-P9-02): models needed for PointStruct
from qdrant_client.models import (
    VectorParams, SparseVectorParams, Distance,
    SparseIndexParams,
)

def create_collection(client: QdrantClient, collection_name: str = "fsm_corpus"):
    """Create Qdrant collection with hybrid dense + sparse vectors."""
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": VectorParams(
                size=1024,           # BGE-M3 dense dimension
                distance=Distance.COSINE,
                on_disk=False,       # Keep in RAM for speed
            )
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(
                index=SparseIndexParams(on_disk=False),
                modifier=None,  # BGE-M3 sparse output is pre-weighted (SPLADE-like); no additional IDF needed
            )
        },
    )

def index_chunk(client: QdrantClient, chunk: dict, chunk_id: str,  # AUDIT FIX (P2-08): was int, now str (UUID)
                dense_vector: list[float], sparse_vector: dict):
    """Index a single chunk with both dense and sparse vectors."""
    # AUDIT FIX (DT-P8-06): Conditionally construct vector dict.
    # DT-8 fixed empty SparseVector in the SEARCH path, but the INGESTION path
    # was missed. When TEI degrades, sparse_vector is None or {"indices":[], "values":[]}.
    # Qdrant's Rust backend rejects empty SparseVector arrays with HTTP 400,
    # crashing the entire ingestion pipeline via the circuit breaker.
    vector_data = {"dense": dense_vector}
    if sparse_vector and sparse_vector.get("indices"):
        vector_data["sparse"] = {
            "indices": sparse_vector["indices"],
            "values": sparse_vector["values"],
        }
    # AUDIT FIX (DT-P9-02): Use models.PointStruct instead of raw dict.
    # qdrant-client >= 1.7.0 (system runs v1.15.2) enforces Pydantic validation.
    # Raw dicts crash with ValidationError or AttributeError, halting ingestion.
    client.upsert(
        collection_name="fsm_corpus",
        points=[models.PointStruct(
            id=chunk_id,
            vector=vector_data,
            payload={
                "text": chunk["text"],
                "source": chunk["source"],
                "page_numbers": chunk["page_numbers"],
                "headings": chunk["headings"],
                "token_count": chunk["token_count"],
            }
        )]
    )
```

### Shared Client Singletons

> [!IMPORTANT]
> **AUDIT FIX (P2-04):** Both `chat.py` and `ingest.py` reference `qdrant_client` but neither
> defines it. This module provides a single shared instance imported by all routes.

```python
# backend/shared/clients.py
import os
from qdrant_client import QdrantClient

# AUDIT FIX (P10-16): Separate QdrantClient instances for search and ingest.
# httpx.Client (used internally by synchronous QdrantClient) is NOT thread-safe.
# Chat dispatches hybrid_search via _SEARCH_POOL (ThreadPoolExecutor) and ingestion
# dispatches index_chunk via asyncio.to_thread() — both use different OS threads.
# A single shared instance risks corrupted HTTP connection state.
qdrant_search_client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://qdrant:6333"))
qdrant_ingest_client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://qdrant:6333"))
# Legacy alias retained for backward compatibility in routes that import by old name
qdrant_client = qdrant_search_client
# AUDIT FIX (P11-15): Client separation documentation.
# IMPORTANT: qdrant_search_client is for read-only operations (hybrid_search).
# qdrant_ingest_client is for write operations (index_chunk, create_collection, delete).
# Never swap them — httpx.Client is not thread-safe across pool boundaries.
```

> [!NOTE]
> **AUDIT FIX (P3-13): Shared tokenizer singleton.** Both `parser.py` and `context_builder.py`
> previously instantiated their own `AutoTokenizer.from_pretrained()` — loading ~50-100MB of
> vocabulary data each. Now both import from a single module:

```python
# backend/shared/tokenizer.py
import os
import threading  # AUDIT FIX (P6-06)
from transformers import AutoTokenizer

# AUDIT FIX (P4-11 + DT-P5-06): Pre-check model directory with clear error message.
# Without this, a missing volume mount produces a confusing ImportError
# traceback deep in the transformers library. Matches P2-12 pattern.
# DT-P5-06: SystemExit inherits from BaseException — bypasses except ImportError
# in validate_ledger.py's host-side fallback. RuntimeError is properly catchable.
_MODEL_PATH = "/app/models/Qwen2.5-32B-Instruct-AWQ"
if not os.path.isdir(_MODEL_PATH):
    raise RuntimeError(
        f"Fatal: tokenizer model directory not found at {_MODEL_PATH}. "
        f"Ensure model weights are pre-downloaded to ./storage/models/."
    )

TOKENIZER = AutoTokenizer.from_pretrained(
    _MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True,
)

# AUDIT FIX (P6-06): Thread-safe token counting wrapper.
# TOKENIZER.encode() is called from multiple async contexts that may run on
# different threads via asyncio.to_thread(): chat handler, build_context(),
# parse_and_chunk(), and eviction loop. HuggingFace provides NO thread-safety
# guarantee for trust_remote_code tokenizers (Qwen2.5 loads custom Python code).
# A threading.Lock prevents potential state corruption in the custom tokenization.
_TOKENIZER_LOCK = threading.Lock()

def count_tokens(text: str) -> int:
    """Thread-safe token counting."""
    with _TOKENIZER_LOCK:
        return len(TOKENIZER.encode(text))
```

> [!IMPORTANT]
> **AUDIT FIX (P3-03): Collection auto-creation at startup.** Without this, a fresh deployment
> receiving a `/api/chat` request before any PDF is ingested hits a Qdrant 404 on the
> non-existent `fsm_corpus` collection. The error handler returns PHASE_ERROR but with a
> misleading "search system temporarily unavailable" message.

```python
# backend/main.py (startup hook)
# AUDIT FIX (P11-02): Use qdrant_ingest_client for startup probe (management operation).
from backend.shared.clients import qdrant_ingest_client
from backend.indexing.qdrant_setup import create_collection
# AUDIT FIX (P11-04): Removed unused UnexpectedResponse import (bare except Exception used)
import asyncio
import logging  # AUDIT FIX (P11-03)
logger = logging.getLogger(__name__)  # AUDIT FIX (P11-03)

@app.on_event("startup")
async def ensure_qdrant_collection():
    """Create collection if it doesn't exist. Retry on transient failure."""
    # AUDIT FIX (P3-03 + P4-07 + P5-08): Idempotent collection creation with retry.
    # P3-03: Fresh deployment hits 404 without this.
    # P4-07: If Qdrant is still loading persistence, create_collection() fails.
    # P5-08: Extended from 5→10 attempts with 60s cap to outlast large persistence loads.
    # Total max wait: 1+2+4+8+16+32+60+60+60+60 = ~303s (~5 minutes)
    for attempt in range(10):
        try:
            # AUDIT FIX (P11-02): Use ingest client for read probe too.
            qdrant_ingest_client.get_collection("fsm_corpus")
            logger.info("Qdrant collection 'fsm_corpus' verified.")
            return
        except Exception:
            try:
                # AUDIT FIX (P10-29): Use ingest client for write operations,
                # matching P10-16 semantic separation (search vs write).
                from backend.shared.clients import qdrant_ingest_client
                create_collection(qdrant_ingest_client)
                logger.info("Qdrant collection 'fsm_corpus' created.")
                return
            except Exception as e:
                wait = min(2 ** attempt, 60)  # Cap at 60 seconds per wait
                logger.warning(f"Qdrant not ready (attempt {attempt+1}/10): {e}")
                await asyncio.sleep(wait)
    logger.critical("FATAL: Could not verify/create Qdrant collection after 10 attempts (~5 min).")
    raise SystemExit("Qdrant collection setup failed — aborting startup.")
```

```python
# AUDIT FIX (P5-05): Graceful shutdown — close persistent httpx connections.
from backend.embedding.client import close_embed_client
from backend.inference.llm import _flush_llm_client  # AUDIT FIX (P9-03)

@app.on_event("shutdown")
async def cleanup_clients():
    """Close persistent httpx clients and thread pools to prevent leaks."""
    await close_embed_client()
    # AUDIT FIX (P9-03): Close LLM httpx client on shutdown. Without this,
    # _llm_client's connection pool to vLLM:8000 is abandoned without aclose(),
    # leaking TCP sockets into TIME_WAIT during rapid restart cycles.
    await _flush_llm_client()
    # AUDIT FIX (P9-09): Shut down search thread pool. Non-blocking (wait=False)
    # so blocked Qdrant HTTP calls don't delay container exit past Docker's
    # 10s SIGTERM grace period, which would trigger SIGKILL.
    from backend.routes.chat import _SEARCH_POOL
    _SEARCH_POOL.shutdown(wait=False)
    # AUDIT FIX (P10-30): Close Qdrant clients to prevent TCP socket leak.
    # QdrantClient uses synchronous httpx.Client — wrap in to_thread to avoid
    # blocking the event loop. Same class of leak as P9-03 and P5-05.
    from backend.shared.clients import qdrant_search_client, qdrant_ingest_client
    await asyncio.to_thread(qdrant_search_client.close)
    await asyncio.to_thread(qdrant_ingest_client.close)
    logger.info("All httpx clients, thread pools, and Qdrant clients closed.")
```

### TEI Embedding Client

> [!IMPORTANT]
> **TRIAD FIX (OP-2, OP-6):** The original V10 draft showed how to store and search embeddings but was missing the code that actually GENERATES them via TEI. This section fills that gap. It also validates that TEI exposes sparse vector support for BGE-M3.

```python
# backend/embedding/client.py
import asyncio  # AUDIT FIX (P7-13): Required for _client_lock
import os       # AUDIT FIX (P10-23): Required by P10-17's os.environ.get("TEI_BASE_URL")
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# AUDIT FIX (P10-17): Read TEI_BASE_URL from env var — operator can point to
# external TEI server without editing backend code. Docker Compose sets the default.
TEI_BASE_URL = os.environ.get("TEI_BASE_URL", "http://tei:80")

# AUDIT FIX (P3-05): Persistent httpx client instead of per-call instantiation.
# During bulk ingestion (100K+ chunks), creating/destroying an HTTP client per
# embed call exhausts ephemeral ports and accumulates TIME_WAIT sockets.
_http_client: httpx.AsyncClient | None = None

# AUDIT FIX (P7-13 + DT-P9-01): Asyncio lock for pool flush serialization.
# P7-13: Without a lock, concurrent coroutines can double-close the httpx client.
# DT-P9-01: Deferred initialization — asyncio.Lock() at module scope crashes on
# Python 3.10+ because no event loop exists during import. Lazy init on first use.
_client_lock: asyncio.Lock | None = None
# AUDIT FIX (P10-04): Thread-safe double-checked locking for lazy asyncio.Lock init.
# Without this, a TOCTOU race could create two asyncio.Lock instances if refactoring
# introduces an await between the None check and assignment.
import threading
_client_lock_init = threading.Lock()

async def _get_client_lock() -> asyncio.Lock:
    global _client_lock
    if _client_lock is None:
        with _client_lock_init:
            if _client_lock is None:
                _client_lock = asyncio.Lock()
    return _client_lock

async def _flush_embed_client():
    """AUDIT FIX (P7-13): Serialized pool flush for concurrent failure safety."""
    lock = await _get_client_lock()  # AUDIT FIX (DT-P9-01)
    async with lock:
        global _http_client
        if _http_client is not None and not _http_client.is_closed:
            await _http_client.aclose()
            _http_client = None

async def _get_client() -> httpx.AsyncClient:
    # AUDIT FIX (P10-02): Lock-protect client initialization. Without the lock,
    # _flush_embed_client() can close a client between the caller's _get_client()
    # return and their subsequent client.post() — causing use-after-close errors
    # during TEI crash recovery when concurrent embed requests are in-flight.
    lock = await _get_client_lock()
    async with lock:
        global _http_client
        if _http_client is None or _http_client.is_closed:
            # AUDIT FIX (P5-05): Explicit pool limits prevent unbounded connection growth
            # during bulk ingestion. 100 max connections is generous for single-TEI setups;
            # 20 max keepalive prevents idle socket accumulation.
            # AUDIT FIX (P6-08): Reduced timeout from 30s to 10s (connect: 5s) — fail-fast
            # on stale keep-alive connections after TEI container restart.
            _http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        return _http_client

async def close_embed_client():
    """AUDIT FIX (P5-05 + P8-06): Graceful shutdown — close persistent httpx client.
    P8-06: Route through _client_lock to prevent race with _flush_embed_client()
    during concurrent shutdown + TEI failure."""
    lock = await _get_client_lock()  # AUDIT FIX (DT-P9-01)
    async with lock:
        global _http_client
        if _http_client is not None and not _http_client.is_closed:
            await _http_client.aclose()
            _http_client = None

async def embed_text(
    text: str,
    base_url: str = TEI_BASE_URL,
) -> tuple[list[float], Optional[dict]]:
    """Generate dense and sparse embeddings via TEI.
    
    TEI's BGE-M3 model exposes:
      - POST /embed         → dense vectors (1024-dim)
      - POST /embed_sparse  → sparse vectors (token_id: weight pairs)
    
    IMPORTANT: TEI must be started with a model that supports sparse output.
    BGE-M3 supports this natively. Verify with:
      curl -s http://127.0.0.1:8080/info | python3 -c "import sys,json; print(json.load(sys.stdin))"
    The response should include "sparse" in the model's capabilities.
    
    Returns:
        (dense_vector, sparse_vector) where sparse_vector may be None
        if TEI version doesn't support /embed_sparse.
    """
    # AUDIT FIX (GP7-05): Wrap all TEI calls in connection-aware error handler.
    # After a TEI crash, httpx keeps dead TCP sockets in the connection pool.
    # Without flushing, each subsequent request hangs for 10s (P6-08 timeout),
    # fails, and the next request picks another dead socket — cycling through
    # the entire pool before recovery. Flushing forces fresh connections.
    # AUDIT FIX (P11-08): _get_client() moved inside try — constructor failure
    # now triggers pool flush instead of leaving corrupt state.
    try:
        client = await _get_client()  # AUDIT FIX (P3-05)
        # Dense embedding
        dense_response = await client.post(
            f"{base_url}/embed",
            json={"inputs": text},
        )
        dense_response.raise_for_status()
        dense_vector = dense_response.json()[0]  # List[float], 1024-dim
        
        # Sparse embedding
        sparse_vector = None
        try:
            sparse_response = await client.post(
                f"{base_url}/embed_sparse",
                json={"inputs": text},
            )
            sparse_response.raise_for_status()
            sparse_data = sparse_response.json()[0]  # List[{index, value}]
            sparse_vector = {
                "indices": [entry["index"] for entry in sparse_data],
                "values": [entry["value"] for entry in sparse_data],
            }
        except (httpx.HTTPStatusError, KeyError) as e:
            # TEI version may not support sparse; degrade to dense-only
            logger.warning(f"TEI /embed_sparse failed ({e}) — falling back to dense-only search")
        
        return dense_vector, sparse_vector
    except (httpx.ConnectError, httpx.ReadTimeout, RuntimeError) as e:
        # AUDIT FIX (GP7-05 + P7-13): TEI is down — flush dead sockets via
        # lock-protected helper to prevent race condition under concurrent failures.
        logger.warning(f"TEI connection failure ({type(e).__name__}) — flushing httpx pool")
        await _flush_embed_client()
        raise
```

### Ingestion Orchestration

```python
# backend/ingestion/pipeline.py
import asyncio
import os       # AUDIT FIX (P7-09): Required by P7-07's os.path.basename()
import threading  # AUDIT FIX (P10-24): Required by P10-20's _manifest_lock = threading.Lock()
import uuid
from backend.ingestion.parser import parse_and_chunk, IngestionError
from backend.embedding.client import embed_text
from backend.indexing.qdrant_setup import index_chunk
from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)

# AUDIT FIX (DT-P2-04): Limit concurrent ingestion workers to prevent OOM.
# The V9 daemon fires 500+ POST /api/ingest requests in seconds (HTTP 202 returns instantly).
# Without a semaphore, asyncio.to_thread spawns ~32 concurrent Docling/EasyOCR workers,
# each consuming ~2GB RAM. On a 64GB host, this instantly triggers the Linux OOM Killer.
# Limit to 2 concurrent jobs — each Docling+EasyOCR process needs ~2GB for PDF parsing + OCR.
# AUDIT FIX (DT-P10-01): Deferred initialization — asyncio.Semaphore() at module scope
# crashes Python 3.10+ (same as DT-P9-01 for asyncio.Lock). Lazy init on first use.
_INGEST_SEMAPHORE: asyncio.Semaphore | None = None

async def _get_ingest_semaphore() -> asyncio.Semaphore:
    global _INGEST_SEMAPHORE
    if _INGEST_SEMAPHORE is None:
        _INGEST_SEMAPHORE = asyncio.Semaphore(2)
    return _INGEST_SEMAPHORE

# AUDIT FIX (P3-04): Rate-limit concurrent TEI embedding requests.
# The INGEST_SEMAPHORE gates parse_and_chunk (CPU-bound) but the embed loop runs
# outside it. With 500+ PDFs queued, dozens enter the embed phase simultaneously,
# flooding TEI with concurrent HTTP requests and causing httpx timeouts.
# AUDIT FIX (DT-P10-01): Deferred initialization, matching ingest semaphore pattern.
_EMBED_SEMAPHORE: asyncio.Semaphore | None = None

async def _get_embed_semaphore() -> asyncio.Semaphore:
    global _EMBED_SEMAPHORE
    if _EMBED_SEMAPHORE is None:
        _EMBED_SEMAPHORE = asyncio.Semaphore(8)  # TEI handles ~8 concurrent requests efficiently
    return _EMBED_SEMAPHORE

async def ingest_pdf(pdf_path: str, client: QdrantClient) -> int:
    """Full ingestion pipeline: parse → embed → index.
    
    Returns number of chunks indexed.
    Raises IngestionError if parsing fails (caller should quarantine).
    
    AUDIT FIX (DT-3): Uses deterministic UUID5 based on (pdf_path, chunk_index)
    so that re-ingesting the same PDF produces the same IDs (idempotent upsert),
    but different PDFs never collide. Previous sequential IDs (start_id + i)
    caused every PDF to overwrite chunks 0, 1, 2... destroying the entire DB.
    """
    # AUDIT FIX: parse_and_chunk is synchronous and CPU-bound (20-60 hours for
    # degraded scans). Must dispatch to threadpool to avoid deadlocking the
    # asyncio event loop and killing FastAPI health checks.
    # AUDIT FIX (DT-P2-04): Acquire semaphore to limit concurrent OCR workers.
    # Only the CPU-bound parse_and_chunk is gated — embed/index are I/O-bound.
    async with (await _get_ingest_semaphore()):  # AUDIT FIX (DT-P10-01): lazy getter
        chunks = await asyncio.to_thread(parse_and_chunk, pdf_path)
    
    if not chunks:
        # AUDIT FIX (DT-5b): Zero extractable text = silent failure.
        # Raise IngestionError so the V9 quarantine logic activates.
        raise IngestionError(f"No chunks extracted from {pdf_path} — likely blank/corrupt PDF")
    
    # AUDIT FIX (P5-01): Track actual indexed vs failed counts. Previously reported
    # len(chunks) which is the PARSED count, not the indexed count. Silent partial
    # ingestion: TEI down → 0 indexed, 200 reported → entire FSM corpus missing.
    indexed_count = 0
    failed_count = 0
    
    # AUDIT FIX (P7-14): Removed P7-07's pre-delete-before-reindex.
    # P7-07 deleted all existing chunks for a PDF before re-inserting new ones.
    # Problem: for a 200-chunk PDF, the delete completes in milliseconds but
    # re-embedding takes ~100s. During this window, a mechanic querying that
    # PDF's content gets RETRIEVAL_FAILURE — a safety issue for brake/fuel procedures.
    # UUID5 deterministic upsert handles matching chunks (same content = same ID).
    # Ghost chunks from shrunk PDFs (v2 has fewer chunks than v1) are a data
    # quality issue, not a safety issue. Use /api/cleanup to purge stale chunks
    # offline when the system is not actively serving queries.
    # AUDIT FIX (P7-04): Circuit breaker for consecutive failures.
    # When TEI/Qdrant dies, ConnectError returns instantly (~1ms). Without a
    # circuit breaker, the for-loop burns through all remaining chunks at CPU
    # speed — discarding hours of parsed OCR data in milliseconds. After 5
    # consecutive failures, abort and let the background wrapper write to the
    # failure manifest for operator retry.
    consecutive_failures = 0
    for i, chunk in enumerate(chunks):
        # AUDIT FIX (DT-3): Deterministic UUID from (path, index).
        # AUDIT FIX (P2-08): Use str() not .hex — Qdrant needs hyphenated UUID format.
        chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{pdf_path}_{i}"))
        
        # AUDIT FIX (P4-08): Per-chunk error handling for embed+index.
        # Without this, a single TEI crash (ConnectError) during bulk ingestion
        # kills the entire PDF — all remaining chunks are skipped. Now each
        # chunk failure is logged and skipped; the rest of the PDF proceeds.
        try:
            # AUDIT FIX (P3-04): Rate-limit TEI requests to prevent timeout cascade
            async with (await _get_embed_semaphore()):  # AUDIT FIX (DT-P10-01): lazy getter
                dense, sparse = await embed_text(chunk["text"])
            sparse_dict = sparse or {"indices": [], "values": []}
            
            # AUDIT FIX: index_chunk() uses synchronous client.upsert() — dispatch
            # to threadpool to avoid blocking the event loop during bulk ingestion.
            await asyncio.to_thread(
                index_chunk,
                client=client,
                chunk=chunk,
                chunk_id=chunk_id,
                dense_vector=dense,
                sparse_vector=sparse_dict,
            )
            indexed_count += 1  # AUDIT FIX (P5-01)
            consecutive_failures = 0  # AUDIT FIX (P7-04): reset on success
        except Exception as e:
            failed_count += 1  # AUDIT FIX (P5-01)
            consecutive_failures += 1  # AUDIT FIX (P7-04)
            logger.warning(f"Chunk {i}/{len(chunks)} failed for {pdf_path}: {e} — skipping")
            # AUDIT FIX (P7-04): Circuit breaker — 5 consecutive failures means
            # the downstream service (TEI/Qdrant) is dead, not flaky. Abort to
            # preserve remaining chunks for retry instead of burning through them.
            if consecutive_failures >= 5:
                raise IngestionError(
                    f"Circuit breaker: {consecutive_failures} consecutive failures at "
                    f"chunk {i}/{len(chunks)} for {pdf_path}. TEI or Qdrant likely down."
                )
            continue
    
    # AUDIT FIX (P5-01): Report actual indexed count, not len(chunks)
    logger.info(
        f"Indexed {indexed_count}/{len(chunks)} chunks from {pdf_path}"
        f"{f' ({failed_count} failed)' if failed_count else ''}"
    )
    # AUDIT FIX (P6-03): Only write PARTIAL manifest entry when some chunks succeeded.
    # When ALL chunks fail (indexed_count == 0), DT-P5-04 raises IngestionError which
    # the background wrapper catches and writes to the manifest — don't double-write.
    if failed_count > 0 and indexed_count > 0:
        logger.warning(
            f"PARTIAL INGESTION: {pdf_path} — {failed_count}/{len(chunks)} chunks failed. "
            f"Re-ingest after resolving TEI/Qdrant issues."
        )
        # Write partial failure to manifest so operator can identify and re-ingest
        # AUDIT FIX (P10-26): Acquire _manifest_lock — P10-20 only wrapped the
        # background wrapper paths, missing this partial-failure path in ingest_pdf().
        with _manifest_lock:
            with open(FAILURE_MANIFEST_PATH, "a") as f:
                f.write(f"{pdf_path}\tPARTIAL: {indexed_count}/{len(chunks)} indexed, {failed_count} failed\n")
    # AUDIT FIX (DT-P5-04): If EVERY chunk failed, raise IngestionError so the
    # P2-06 background wrapper logs it and writes to the failure manifest.
    # No silent errors — a 100% failure rate is never "success".
    if indexed_count == 0 and len(chunks) > 0:
        raise IngestionError(
            f"All {len(chunks)} chunks failed to index for {pdf_path} — "
            f"TEI or Qdrant may be down."
        )
    return indexed_count  # AUDIT FIX (P5-01): was len(chunks)

# AUDIT FIX (P2-06): Background task wrapper with error handling.
# When called via FastAPI BackgroundTasks, exceptions are silently swallowed.
# This wrapper catches IngestionError, logs it, and writes to a failure manifest
# so the V9 daemon (or operator) can identify failed ingestions.
# AUDIT FIX (P5-10): Path constant — was "/app/storage/extracted/" which doesn't
# match the Docker volume mount (./storage/extracted:/app/extracted). Failures
# were written to an unmounted path and lost on container restart.
FAILURE_MANIFEST_PATH = "/app/extracted/.ingest_failures.log"
# AUDIT FIX (P10-20): Thread-safe manifest writes. With INGEST_SEMAPHORE=2,
# two concurrent ingestion failures can race on append. threading.Lock prevents
# interleaved writes (especially on non-ext4 filesystems like overlayfs).
_manifest_lock = threading.Lock()

async def ingest_pdf_background(pdf_path: str, client: QdrantClient):
    """Wrapper for BackgroundTask execution with error handling."""
    try:
        count = await ingest_pdf(pdf_path, client)
        logger.info(f"Background ingestion complete: {pdf_path} ({count} chunks)")
    except IngestionError as e:
        logger.error(f"INGESTION FAILED (quarantine candidate): {pdf_path} — {e}")
        # Write to failure manifest for operator/daemon re-check
        with _manifest_lock:  # AUDIT FIX (P10-20)
            with open(FAILURE_MANIFEST_PATH, "a") as f:  # AUDIT FIX (P5-10)
                f.write(f"{pdf_path}\t{e}\n")
    except Exception as e:
        logger.error(f"UNEXPECTED INGESTION ERROR: {pdf_path} — {e}", exc_info=True)
        # AUDIT FIX (P3-09): Also log unexpected errors to failure manifest
        # (previously only IngestionError was written — operator would miss these)
        with _manifest_lock:  # AUDIT FIX (P10-20)
            with open(FAILURE_MANIFEST_PATH, "a") as f:  # AUDIT FIX (P5-10)
                f.write(f"{pdf_path}\tUNEXPECTED: {e}\n")
```

> [!IMPORTANT]
> **AUDIT FIX (DT-5): Ingestion endpoint MUST use FastAPI BackgroundTasks.**
> Docling+EasyOCR processes 1-3 minutes per page (20-60 hours for full corpus).
> If the HTTP request stays open, Nginx's 60s timeout drops the connection.
> The V9 daemon interprets this as failure and retries, spawning infinite
> concurrent OCR threads until the host CPU locks up.
>
> ```python
> # backend/routes/ingest.py
> import asyncio  # AUDIT FIX (P10-09): Required by P9-04's asyncio.to_thread() in /api/cleanup
> import os
> from fastapi import APIRouter, BackgroundTasks, Request
> from qdrant_client import models  # AUDIT FIX (P10-10): consolidated from cleanup block
> from backend.shared.clients import qdrant_ingest_client  # AUDIT FIX (P2-04 + P10-25 + P11-10)
> from backend.ingestion.pipeline import ingest_pdf_background  # AUDIT FIX (P11-01)
> 
> router = APIRouter()
> ALLOWED_PDF_DIR = "/app/pdfs"  # AUDIT FIX (P2-11): path traversal prevention
> 
> @router.post("/api/ingest", status_code=202)
> async def ingest(request: Request, background_tasks: BackgroundTasks):
>     body = await request.json()
>     # AUDIT FIX (DT-P4-04 + DT-P5-05): The host daemon sends absolute HOST paths
>     # (e.g. /home/user/storage/pdfs/engine/manual.pdf). The container volume mount
>     # maps that directory to /app/pdfs. Extract the relative path AFTER "pdfs/"
>     # to preserve subdirectory structure. Fallback to basename if "pdfs/" not found.
>     # DT-P5-05: basename() flattens subdirs — /app/pdfs/engine/manual.pdf becomes
>     # /app/pdfs/manual.pdf which doesn't exist.
>     raw_path = body["pdf_path"]
>     # AUDIT FIX (P6-07): Null bytes in paths cause os.path.realpath() to raise
>     # ValueError("embedded null character") — unhandled, producing HTTP 500 with
>     # traceback. Reject early with a clean response.
>     if "\x00" in raw_path:
>         return {"status": "rejected", "message": "Invalid path"}
>     rel_path = raw_path.split("pdfs/", 1)[-1] if "pdfs/" in raw_path else os.path.basename(raw_path)
>     pdf_path = os.path.realpath(os.path.join(ALLOWED_PDF_DIR, rel_path))
>     # AUDIT FIX (P2-11 + DT-P3-04): Validate path is within allowed directory.
>     # DT-P3-04: Trailing slash prevents sibling dir bypass ("/app/pdfs_keys/...")
>     if not pdf_path.startswith(ALLOWED_PDF_DIR + "/"):
>         return {"status": "rejected", "message": "Path outside allowed directory"}
>     if not pdf_path.endswith(".pdf"):
>         return {"status": "rejected", "message": "Not a PDF file"}
>     # AUDIT FIX (P10-25): Use qdrant_ingest_client for write operations,
>     # matching P10-16 thread-safety separation (search vs write clients).
>     background_tasks.add_task(ingest_pdf_background, pdf_path, qdrant_ingest_client)
>     return {"status": "accepted", "message": f"Ingestion queued for {pdf_path}"}
> ```
>
> ```python
> # AUDIT FIX (DT-P8-05): Ghost chunk cleanup endpoint.
> # P7-14 removed pre-ingestion database wipe (to prevent mid-ingest gaps) and
> # deferred ghost chunk removal to an offline /api/cleanup endpoint — but the
> # endpoint was never implemented. Without it, re-ingesting a shorter PDF
> # (e.g., manufacturer removing a recalled procedure) leaves stale chunks from
> # the old version permanently searchable. This is a life-safety hazard:
> # recalled/dangerous instructions remain in RAG context indefinitely.
> #
> # Usage: POST /api/cleanup {"source": "brakes/manual.pdf"}
> # AUDIT FIX (DT-P9-03): source is now a relative path (not basename) to prevent
> # cross-source collision when files in different subdirectories share the same name.
> # Atomically deletes all chunks where payload.source matches the given value.
> # AUDIT FIX (DT-P10-03): Run BEFORE re-ingestion, not after. UUID5 deterministic IDs
> # mean post-ingestion cleanup deletes BOTH ghost chunks AND freshly ingested chunks
> # (they share the same source payload), causing total retrieval blackout.
> # Protocol: (1) POST /api/cleanup, (2) POST /api/ingest. Brief offline gap is acceptable.
> # models import moved to top of file — AUDIT FIX (P10-10)
> 
> @router.post("/api/cleanup", status_code=200)
> async def cleanup_document(request: Request):
>     body = await request.json()
>     source = body.get("source")
>     if not source or not isinstance(source, str):
>         return {"status": "rejected", "message": "Missing or invalid 'source' field"}
>     # AUDIT FIX (P9-04): Wrap synchronous Qdrant delete in asyncio.to_thread().
>     # Same class of defect as P3-08 (search) and H06 (index_chunk). Without this,
>     # the synchronous HTTP call blocks the event loop for 500ms-2s on large source
>     # files, causing concurrent healthchecks to timeout and Docker to restart.
>     # AUDIT FIX (P10-25): Use qdrant_ingest_client for delete operations.
>     await asyncio.to_thread(
>         qdrant_ingest_client.delete,
>         collection_name="fsm_corpus",
>         points_selector=models.FilterSelector(
>             filter=models.Filter(
>                 must=[models.FieldCondition(
>                     key="source",
>                     match=models.MatchValue(value=source),
>                 )]
>             )
>         ),
>     )
>     return {"status": "success", "message": f"All chunks with source='{source}' deleted"}
> ```

> [!NOTE]
> **Chat Handler (Complete Assembly):** The chat route is the single orchestration point
> where ALL components converge. The ledger, RAG context, chat history, and system prompt
> are assembled here in a specific order.

```python
# backend/routes/chat.py
import asyncio  # AUDIT FIX (P4-01): Required by P3-08's asyncio.to_thread() search dispatch
import json
import os
from concurrent.futures import ThreadPoolExecutor  # AUDIT FIX (P6-05)
import logging
from fastapi import APIRouter, Request
from backend.embedding.client import embed_text
from backend.retrieval.search import hybrid_search  # AUDIT FIX (P8-11): was backend.search
from backend.retrieval.context_builder import build_context  # AUDIT FIX (P8-11): was backend.inference.context
from backend.shared.tokenizer import TOKENIZER, count_tokens, _TOKENIZER_LOCK  # AUDIT FIX (P8-11, P2-03, P7-01, DT-P8-03)
from backend.inference.llm import generate_response
from backend.shared.clients import qdrant_client  # AUDIT FIX (P2-04)

logger = logging.getLogger(__name__)

# AUDIT FIX (P6-05): Dedicated thread pool for chat-path search.
# The default ThreadPoolExecutor is shared with ingestion's index_chunk() calls.
# During bulk ingestion (200+ chunks × 2 concurrent PDFs), index_chunk to_thread()
# dispatches can saturate the default pool, queuing chat search requests behind them.
# This dedicated pool guarantees chat search always has threads available.
_SEARCH_POOL = ThreadPoolExecutor(max_workers=4, thread_name_prefix="chat-search")

# AUDIT FIX (P9-02): Read budget env vars. Docker Compose defines MAX_CONTEXT_TOKENS,
# SYSTEM_PROMPT_TOKENS, and RESPONSE_BUDGET_TOKENS but build_context() was called with
# hardcoded defaults, ignoring operator configuration. Deploying on a 16K model with
# MAX_CONTEXT_TOKENS=16384 had ZERO effect — build_context() still computed with 32768.
_MAX_CONTEXT_TOKENS = int(os.environ.get("MAX_CONTEXT_TOKENS", "32768"))
_SYSTEM_PROMPT_TOKENS = int(os.environ.get("SYSTEM_PROMPT_TOKENS", "900"))
_RESPONSE_BUDGET_TOKENS = int(os.environ.get("RESPONSE_BUDGET_TOKENS", "2000"))

router = APIRouter()

# AUDIT FIX (P2-12): Explicit startup failure instead of confusing ImportError
_PROMPT_PATH = "/app/config/system_prompt.txt"
if os.path.exists(_PROMPT_PATH):
    # AUDIT FIX (P9-12): Use context manager — bare open().read() leaks the FD
    # for the server's lifetime. All other file opens (load_ledger, ingest) use `with`.
    with open(_PROMPT_PATH) as f:
        SYSTEM_PROMPT = f.read()
else:
    logger.critical(f"SYSTEM PROMPT NOT FOUND: {_PROMPT_PATH}")
    raise SystemExit(f"Fatal: system prompt missing at {_PROMPT_PATH}")

# AUDIT FIX (P8-09): Verify system prompt token count at startup.
# SYSTEM_PROMPT_TOKENS=900 is used as a parameter default in build_context().
# If the operator edits system_prompt.txt (common customization), the actual
# count may exceed 900. The budget would under-deduct, allowing RAG context to
# over-fill, and the final prompt sent to vLLM would exceed max_model_len.
_actual_prompt_tokens = count_tokens(SYSTEM_PROMPT)
_configured_prompt_tokens = int(os.environ.get("SYSTEM_PROMPT_TOKENS", "900"))
if _actual_prompt_tokens > _configured_prompt_tokens:
    logger.critical(
        f"System prompt ({_actual_prompt_tokens} tokens) exceeds configured budget "
        f"({_configured_prompt_tokens}). Update SYSTEM_PROMPT_TOKENS env var."
    )
    raise SystemExit(f"System prompt exceeds token budget: {_actual_prompt_tokens} > {_configured_prompt_tokens}")

@router.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_query = body["message"]
    
    # AUDIT FIX (P7-15): Validate chat_history schema before processing.
    # Frontend sends chat_history as a list of {role, content} dicts. Without
    # validation, a malformed entry (missing "content", null value, wrong type,
    # stale cache, XSS injection) crashes count_tokens() with KeyError/TypeError
    # → unhandled HTTP 500 with Python traceback (information disclosure).
    raw_history = body.get("chat_history", [])
    if not isinstance(raw_history, list):
        raw_history = []
    chat_history = []
    for m in raw_history:
        if (isinstance(m, dict)
            and isinstance(m.get("content"), str)
            and m.get("content").strip()            # AUDIT FIX (P8-07): reject empty/whitespace-only
            and m.get("role") in ("user", "assistant")):
            chat_history.append(m)
        else:
            logger.warning(f"Malformed chat_history entry dropped: {type(m)}")
    
    # Step 1: Load ledger (may be empty if file missing — degrades gracefully)
    ledger_text = load_ledger()
    ledger_tokens = count_tokens(ledger_text) if ledger_text else 0  # AUDIT FIX (P7-01)
    
    # AUDIT FIX (P7-11): Runtime ledger cap enforcement.
    # validate_ledger.py checks size at deploy time, but the operator may edit
    # MASTER_LEDGER.md post-deployment without re-running the validator.
    # Unbounded growth → available budget shrinks → PHASE_ERROR for every request.
    # Truncate to cap and warn — forces re-validation while keeping the system alive.
    LEDGER_MAX_TOKENS = int(os.environ.get("LEDGER_MAX_TOKENS", "2550"))
    if ledger_tokens > LEDGER_MAX_TOKENS:
        logger.warning(
            f"Ledger ({ledger_tokens} tokens) exceeds cap ({LEDGER_MAX_TOKENS}). "
            f"Truncating to cap. Run validate_ledger.py to resize."
        )
        # AUDIT FIX (DT-P8-03): Wrap raw TOKENIZER.encode()/decode() in _TOKENIZER_LOCK.
        # Qwen2.5's custom HuggingFace tokenizer is not thread-safe. Without the lock,
        # concurrent ingestion (asyncio.to_thread) can corrupt internal tokenizer state.
        # count_tokens() uses the lock internally, but these raw calls did not.
        with _TOKENIZER_LOCK:
            ledger_text = TOKENIZER.decode(TOKENIZER.encode(ledger_text)[:LEDGER_MAX_TOKENS])
        # AUDIT FIX (P8-04): Re-count after decode — encode→decode round-trip can
        # change token count due to subword boundary effects. Hardcoding LEDGER_MAX_TOKENS
        # without re-counting could cause a budget lie (actual > budgeted).
        ledger_tokens = count_tokens(ledger_text)
        if ledger_tokens > LEDGER_MAX_TOKENS:
            # Slice tighter to guarantee fit
            with _TOKENIZER_LOCK:
                ledger_text = TOKENIZER.decode(TOKENIZER.encode(ledger_text)[:LEDGER_MAX_TOKENS - 10])
            ledger_tokens = count_tokens(ledger_text)
    
    # Step 2: Compute chat history token cost
    chat_history_tokens = sum(
        count_tokens(m["content"]) for m in chat_history  # AUDIT FIX (P7-01)
    )
    
    # AUDIT FIX (P2-02): Physically truncate chat_history array to match budget cap.
    # Without this, build_context() caps the budget MATH at 8000 tokens but
    # generate_response() still sends ALL messages to vLLM, overshooting 32K.
    # Evict oldest messages first (preserve recent diagnostic context).
    MAX_CHAT_HISTORY_TOKENS = 8000
    # AUDIT FIX (P8-03): Cap message count to prevent framing token overflow.
    # FRAMEWORK_OVERHEAD is now dynamic: (message_count + 2) * 5 tokens.
    # Without a count cap, 1000 short messages (4000 content tokens, under 8000
    # cap) generate 5000 framing tokens — overflowing the context window.
    # 40 messages × 5 framing = 200 tokens — safe within any budget scenario.
    MAX_CHAT_HISTORY_MESSAGES = 40
    if len(chat_history) > MAX_CHAT_HISTORY_MESSAGES:
        chat_history = chat_history[-MAX_CHAT_HISTORY_MESSAGES:]
        chat_history_tokens = sum(count_tokens(m["content"]) for m in chat_history)
    # AUDIT FIX (DT-P10-04): Strip leading orphan assistant messages GLOBALLY,
    # not just inside the token eviction block. Message-count truncation (above)
    # can drop the oldest user message, leaving an assistant message at index 0.
    # If token budget is under 8000, the token block is skipped entirely and the
    # orphan strip inside it never executes — poisoning Qwen2.5's ChatML context.
    while chat_history and chat_history[0]["role"] == "assistant":
        removed = count_tokens(chat_history[0]["content"])
        chat_history.pop(0)
        chat_history_tokens -= removed
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        truncated = []
        running = 0
        for msg in reversed(chat_history):
            msg_tokens = count_tokens(msg["content"])  # AUDIT FIX (P7-01)
            if running + msg_tokens > MAX_CHAT_HISTORY_TOKENS and truncated:
                break  # AUDIT FIX (DT-P5-01): Reverted from continue to preserve contiguous role alternation
            truncated.insert(0, msg)
            running += msg_tokens
        # AUDIT FIX (DT-P3-07 + DT-P5-07 + P6-02): Eviction may split a user/assistant pair,
        # leaving a dangling assistant message first. Qwen2.5 chat template expects
        # user-first after system prompt — strip ALL leading orphan assistants.
        # DT-P5-07: Removed P4-03 len>1 guard. An empty history (DAG reset) is always
        # safer than injecting a broken assistant message that poisons LLM context.
        # P6-02: Changed if→while to handle consecutive assistant messages (malformed
        # frontend payload — stale cache, bug, or manipulation).
        while truncated and truncated[0]["role"] == "assistant":
            chat_history_tokens_removed = count_tokens(truncated[0]["content"])  # AUDIT FIX (P7-01)
            truncated.pop(0)
            running -= chat_history_tokens_removed
        chat_history = truncated
        chat_history_tokens = running
    
    # AUDIT FIX (P6-01, CRITICAL): Hard budget enforcement after eviction.
    # When P3-02 guard preserves a single oversized message (>8000 tokens),
    # build_context() only clamps the MATH to 8000 but generate_response()
    # still sends the actual (oversized) message to vLLM. The prompt can
    # exceed --max-model-len 32768, causing HTTP 400 from vLLM.
    # Option (b): Reject with PHASE_ERROR — safer for a life-safety system
    # than silently truncating potentially critical diagnostic context.
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "Your conversation history is too large. Please start a new diagnostic session.",
            "diagnostic_reasoning": f"Chat history ({chat_history_tokens} tokens) exceeds {MAX_CHAT_HISTORY_TOKENS}-token limit after eviction.",
            "requires_input": False,
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    # AUDIT FIX (DT-P6-02): Query length validation moved ABOVE embed call.
    # TEI has an absolute 8192-token input limit. The previous placement at
    # Step 5 (after embedding) meant a 9500-token query would crash the TEI
    # request with HTTP 400 before reaching the length validator, producing a
    # misleading "search system unavailable" error instead of "message too long."
    # Cap reduced from 10000 → 8000 to align with TEI's hardware limit.
    user_query_tokens = count_tokens(user_query)  # AUDIT FIX (P7-01)
    MAX_USER_QUERY_TOKENS = 8000
    if user_query_tokens > MAX_USER_QUERY_TOKENS:
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "Your message is too long for me to process. Please shorten your question or paste smaller sections of diagnostic data.",
            "diagnostic_reasoning": f"User query ({user_query_tokens} tokens) exceeds {MAX_USER_QUERY_TOKENS}-token safety limit.",
            "requires_input": False,
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    # AUDIT FIX (H09/H10/H13): Comprehensive error handling for the entire
    # embed → search → generate pipeline. Without this, TEI crash, Qdrant 404,
    # or vLLM OOM all produce raw HTTP 500 with Python tracebacks visible to
    # the mechanic. Each failure now returns structured JSON with PHASE_ERROR.
    try:
        # Step 3: Embed user query for retrieval
        # AUDIT FIX (P4-05): Acquire EMBED_SEMAPHORE so chat competes fairly
        # with ingestion. Without this, during bulk ingestion all 8 permits are
        # held and chat sends an unthrottled 9th request → TEI overload.
        # AUDIT FIX (P7-05): Acquire with 5s timeout. During bulk ingestion with
        # TEI degradation, 8 permits hang for 10s each (P6-08 timeout). Without
        # a timeout, chat blocks for 250s+ — exceeding Nginx's 60s proxy limit
        # and producing a 504 instead of Gus's graceful PHASE_ERROR.
        from backend.ingestion.pipeline import _get_embed_semaphore
        _embed_sem = await _get_embed_semaphore()  # AUDIT FIX (DT-P10-01): lazy getter
        try:
            await asyncio.wait_for(_embed_sem.acquire(), timeout=5.0)
        except asyncio.TimeoutError:
            raise RuntimeError("Embedding service at capacity — all permits held by ingestion")
        try:
            query_dense, query_sparse = await embed_text(user_query)
        finally:
            _embed_sem.release()
    except Exception as e:
        logger.error(f"Embedding failed: {e}", exc_info=True)
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "The search system is temporarily unavailable. Please try again in a moment.",
            "diagnostic_reasoning": f"Embedding service error: {type(e).__name__}",
            "requires_input": False,  # AUDIT FIX (P2-10)
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    try:
        # Step 4: Hybrid search (dense + sparse with RRF fusion)
        # AUDIT FIX (P3-08 + P6-05): hybrid_search() uses synchronous QdrantClient —
        # dispatch to dedicated search pool to avoid blocking event loop.
        # P6-05: Uses _SEARCH_POOL instead of default to_thread() pool to prevent
        # ingestion index_chunk() calls from starving chat search.
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            _SEARCH_POOL,
            hybrid_search, qdrant_client, query_dense, query_sparse,
            60,  # AUDIT FIX (DT-P9-05): top_k=60 — default 20 starves the ~26K RAG budget
        )
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "The document search system is temporarily unavailable. Please try again in a moment.",
            "diagnostic_reasoning": f"Search error: {type(e).__name__}",
            "requires_input": False,  # AUDIT FIX (P2-10)
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    # Step 5: Build RAG context within token budget
    # AUDIT FIX (P2-01): user_query_tokens already computed above (DT-P6-02 moved it before embed)
    # AUDIT FIX (P3-01): build_context() returns tuple[str, list[dict]].
    # Destructure the return value — without this, `context` is the raw tuple
    # and f-string formatting injects Python tuple repr into the LLM prompt.
    # AUDIT FIX (P7-03): build_context() now raises ValueError if the budget is
    # exhausted below MIN_RAG_FLOOR. Catch it and return a graceful PHASE_ERROR
    # instead of an unhandled HTTP 500.
    try:
        context, used_chunks = build_context(
            results,
            max_context_tokens=_MAX_CONTEXT_TOKENS,       # AUDIT FIX (P9-02)
            system_prompt_tokens=_SYSTEM_PROMPT_TOKENS,    # AUDIT FIX (P9-02)
            response_budget=_RESPONSE_BUDGET_TOKENS,       # AUDIT FIX (P9-02)
            ledger_tokens=ledger_tokens,
            chat_history_tokens=chat_history_tokens,
            user_query_tokens=user_query_tokens,
            chat_history_message_count=len(chat_history),  # AUDIT FIX (P8-03)
        )
    except ValueError as e:
        logger.warning(f"Context budget exhausted: {e}")
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "Your conversation history is too large for me to include enough reference material. Please start a new diagnostic session.",
            "diagnostic_reasoning": str(e),
            "requires_input": False,
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    # Step 6: Assemble system prompt WITH ledger (injection point)
    # Ledger goes INSIDE the system prompt, before RAG context
    system_prompt = SYSTEM_PROMPT
    if ledger_text:
        system_prompt += f"\n\nMASTER_LEDGER.md:\n{ledger_text}"
    
    try:
        # Step 7: Generate LLM response (context appended in generate_response)
        # AUDIT FIX (P6-09): chat_history may be empty after orphan strip
        # (e.g., single-assistant history). This produces valid [system, user]
        # ChatML for Qwen2.5 — this is intentional, not a bug.
        response = await generate_response(
            system_prompt=system_prompt,
            context=context,
            user_message=user_query,
            chat_history=chat_history,
            max_tokens=_RESPONSE_BUDGET_TOKENS,  # AUDIT FIX (P10-14): sync with budget reservation
        )
    except Exception as e:
        logger.error(f"LLM generation failed: {e}", exc_info=True)
        return {"response": json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "The AI engine is temporarily unavailable. Please try again in a moment.",
            "diagnostic_reasoning": f"LLM error: {type(e).__name__}",
            "requires_input": False,  # AUDIT FIX (P2-10)
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })}
    
    # AUDIT FIX (P3-12 + P4-10 + DT-P4-06): Validate LLM output is valid JSON with required schema.
    # P3-12: Qwen2.5 may ignore JSON instruction and return prose.
    # P4-10: Even valid JSON may have wrong schema (e.g. {"answer":"yes"}).
    # DT-P4-06: LLMs frequently wrap valid JSON in ```json ... ``` fences.
    # Strip fences first so the validation doesn't reject salvageable output.
    import re
    stripped = re.sub(r'^```(?:json)?\s*\n?', '', response.strip())
    stripped = re.sub(r'\n?```\s*$', '', stripped)
    try:
        parsed = json.loads(stripped)
        if not isinstance(parsed, dict) or "current_state" not in parsed:
            raise ValueError("Missing required 'current_state' field")
        response = stripped  # Use the fence-stripped version
    except (json.JSONDecodeError, ValueError):
        # AUDIT FIX (P5-03): Secondary extraction — find first { to last } in case
        # the LLM prepended prose before the JSON fence (e.g., "Here is the response:\n```json\n{...}\n```").
        # Replicates the frontend's parseGusResponse() brace-scanning server-side.
        recovered = False
        brace_start = stripped.find('{')
        brace_end = stripped.rfind('}')
        if brace_start != -1 and brace_end > brace_start:
            candidate = stripped[brace_start:brace_end + 1]
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict) and "current_state" in parsed:
                    response = candidate
                    recovered = True
                    logger.info("Recovered JSON via brace extraction after fence-strip failure (P5-03)")
                else:
                    raise ValueError("Missing current_state in extracted JSON")
            except (json.JSONDecodeError, ValueError):
                pass  # Fall through to PHASE_ERROR below

        if not recovered:
            logger.warning(f"LLM returned invalid/malformed response: {response[:200]}")
            response = json.dumps({
                "current_state": "PHASE_ERROR",
                "mechanic_instructions": "The AI produced an unexpected response format. Please rephrase your question.",
                "diagnostic_reasoning": "LLM output failed schema validation — may indicate prompt compliance failure.",
                "requires_input": False,
                "answer_path_prompts": [],
                "source_citations": [],
                "intersecting_subsystems": [],
            })
    
    return {"response": response}
```

### Ingestion Time Estimate

> [!WARNING]
> **Gemini DT and Gemini DR both flag this:** Docling with OCR on 250K+ pages will take significant time. Estimated 2-5 pages/minute with OCR enabled on CPU for clean documents. **For prototype with 514 PDFs (~2,442 pages) of degraded 1960s-era scans, estimated time is 20-60 hours** (1-3 minutes/page with EasyOCR on CPU for faded/handwritten content). This is a one-time cost. Pre-compute and cache Docling output in `./storage/extracted/`.

---

## RETRIEVAL PIPELINE

### Hybrid Search with RRF Fusion

The retrieval pipeline implements Reciprocal Rank Fusion (RRF) to combine dense semantic search with sparse keyword search, achieving NotebookLM-aligned multi-signal retrieval.

```python
# backend/retrieval/search.py
import logging  # AUDIT FIX (P2-07)
from qdrant_client import QdrantClient
from qdrant_client.models import (
    SparseVector, FusionQuery, Fusion, Prefetch,
)

logger = logging.getLogger(__name__)  # AUDIT FIX (P2-07)

def hybrid_search(
    client: QdrantClient,
    query_dense: list[float],
    query_sparse: dict | None,  # AUDIT FIX (OP-P11-06): None when TEI sparse degrades
    top_k: int = 60,  # AUDIT FIX (P10-15): was 20, starves RAG budget (DT-P9-05)
    min_score_ratio: float = 0.70,
    min_absolute_score: float = 0.013,  # AUDIT FIX (P2-14): raised from 0.005 (dead code — RRF min is 0.0125)
) -> list[dict]:
    """Execute hybrid dense + sparse search with RRF fusion.
    
    Args:
        query_dense: Dense embedding vector from BGE-M3
        query_sparse: Sparse vector from BGE-M3 (indices + values)
        top_k: Number of candidates from each signal before fusion
        min_score_ratio: Keep chunks scoring >= this fraction of top RRF score
        min_absolute_score: Absolute RRF score floor — discard ALL results if
            top score is below this value (handles off-topic queries)
    
    Returns:
        List of chunks sorted by RRF score, filtered by dynamic threshold
    """
    # Qdrant native RRF fusion via query API
    # AUDIT FIX (DT-8): Build prefetch list conditionally. Qdrant's Rust backend
    # rejects empty SparseVector arrays ({indices:[], values:[]}) with HTTP 400.
    # When TEI degrades and sparse vector is None, omit the sparse prefetch
    # entirely and fall back to dense-only search.
    prefetch_list = [
        Prefetch(
            query=query_dense,
            using="dense",
            limit=top_k,
        ),
    ]
    
    if query_sparse and query_sparse.get("indices"):
        prefetch_list.append(
            Prefetch(
                query=SparseVector(
                    indices=query_sparse["indices"],
                    values=query_sparse["values"],
                ),
                using="sparse",
                limit=top_k,
            )
        )
    else:
        logger.warning("Sparse vector unavailable — falling back to dense-only search")
    
    # AUDIT FIX (DT-P4-02): Qdrant requires ≥2 prefetch queries for RRF fusion.
    # When TEI sparse degrades and the sparse prefetch is dropped, a single-signal
    # FusionQuery crashes with HTTP 400. Conditionally use direct query for fallback.
    if len(prefetch_list) >= 2:
        results = client.query_points(
            collection_name="fsm_corpus",
            prefetch=prefetch_list,
            query=FusionQuery(fusion=Fusion.RRF),
            limit=top_k,
        )
    else:
        # Dense-only fallback — no fusion needed
        results = client.query_points(
            collection_name="fsm_corpus",
            query=prefetch_list[0].query,
            using="dense",
            limit=top_k,
        )
    
    if not results.points:
        return []
    
    # AUDIT FIX (P5-04 + P6-04): Mode-adaptive absolute score floor.
    # RRF scores cluster in [0.0125, 0.0164] — 0.013 catches off-topic queries.
    # Dense cosine scores range [0, 1] — for BGE-M3 1024-dim L2-normalized vectors,
    # random-pair cosine similarity clusters at 0.25–0.45. P6-04 raised from 0.35
    # (inside noise band) to 0.50 (above noise, below relevant-pair minimum ~0.60).
    effective_min_absolute = min_absolute_score if len(prefetch_list) >= 2 else 0.50
    top_score = results.points[0].score
    if top_score < effective_min_absolute:
        logger.warning(
            f"Top score {top_score:.4f} below absolute floor {effective_min_absolute} "
            f"({'RRF' if len(prefetch_list) >= 2 else 'dense-only'} mode) — discarding all results"
        )
        return []
    
    # Dynamic threshold: keep chunks within a fraction of top score.
    # AUDIT FIX (DT-P8-07): Multiplicative ratios are DISABLED for BOTH modes.
    #
    # RRF mode: Scores are additive — dual-match ≈ 0.0328, single-match ≈ 0.0164.
    # A 0.70 ratio on 0.0328 = threshold 0.0229 — this discards ALL single-signal
    # matches (0.0164 < 0.0229), turning hybrid search (a union) into a strict
    # intersection. Rely on min_absolute_score (0.013) and top_k for filtering.
    #
    # Dense-only mode: (DT-P6-05) Cosine scores range widely (0.3–1.0). A 0.70
    # ratio on 0.90 = 0.63, brutally discarding chunks at 0.60 that are still
    # highly relevant. Rely on absolute floor (0.50) and top_k.
    effective_ratio = 0.0  # AUDIT FIX (DT-P8-07): ratios break additive RRF arrays
    threshold = top_score * effective_ratio
    
    filtered = []
    for point in results.points:
        # AUDIT FIX (DT-P8-04): Apply absolute floor to EVERY chunk, not just top score.
        # Without this, dense-only fallback (threshold=0.0) lets all 20 chunks through
        # including noise at cosine 0.25. The absolute floor (0.50 dense / 0.013 RRF)
        # now filters symmetrically across all results.
        if point.score >= threshold and point.score >= effective_min_absolute:
            filtered.append({
                "text": point.payload["text"],
                "source": point.payload["source"],
                "page_numbers": point.payload["page_numbers"],
                "headings": point.payload["headings"],
                "token_count": point.payload["token_count"],
                "score": point.score,
            })
    
    # AUDIT FIX (GP7-11): Telemetry for threshold calibration.
    # If search returned results but ALL were filtered by the dynamic ratio,
    # the operator has zero visibility into why context is empty. Log the top
    # rejected score so operators can calibrate the 0.50 floor to their corpus.
    if not filtered and results.points:
        top_rejected = results.points[0].score
        logger.warning(
            f"SEARCH FILTER SUPPRESSION: {len(results.points)} chunks found but "
            f"all below threshold {threshold:.4f}. Top rejected score: {top_rejected:.4f}. "
            f"Consider adjusting min_absolute_score if this recurs."
        )
    
    return filtered
```

### Greedy Token-Capped Context Injection

> [!IMPORTANT]
> **NotebookLM Parity:** NotebookLM injects "raw, sequential plain-text strings divided into numerical excerpts" — NOT a fixed number of chunks. V10 replicates this by greedily filling the context window with the highest-scoring chunks until the token budget is exhausted.

```python
# backend/retrieval/context_builder.py
import logging  # AUDIT FIX (P3-06)
from backend.shared.tokenizer import TOKENIZER, count_tokens  # AUDIT FIX (P3-13, P7-01)

logger = logging.getLogger(__name__)  # AUDIT FIX (P3-06)

# AUDIT FIX (H11): Runtime RAG budget floor — prevents long conversations from
# silently pushing RAG context to zero or negative. The ledger validator uses
# MIN_RAG_BUDGET=20000, but at runtime we use a lower floor to allow some
# degradation before hard-cutting chat history.
MIN_RAG_FLOOR = 5000  # Minimum tokens reserved for RAG context at runtime
MAX_CHAT_HISTORY_TOKENS = 8000  # AUDIT FIX (H12): Hard cap on chat history
# AUDIT FIX (P8-03): Dynamic ChatML framing computation replaces static FRAMEWORK_OVERHEAD.
# vLLM wraps each message with <|im_start|>role\n...<|im_end|>\n (~5 tokens each).
# Static FRAMEWORK_OVERHEAD=250 budgeted for ~50 messages, but message count was
# unbounded — 1000 short messages × 5 = 5000 framing tokens vs 250 budgeted = overflow.
# Now computed dynamically from actual message count passed by chat handler.
TOKENS_PER_MESSAGE_FRAME = 5  # Conservative: <|im_start|>, role, \n, <|im_end|>, \n
# AUDIT FIX (P11-13): Moved to module scope to avoid per-request _TOKENIZER_LOCK acquisition.
SEPARATOR = "\n\n---\n\n"
SEPARATOR_TOKENS = count_tokens(SEPARATOR)  # AUDIT FIX (P7-01)

def build_context(
    chunks: list[dict],
    max_context_tokens: int = 32768,
    system_prompt_tokens: int = 900,
    ledger_tokens: int = 0,
    response_budget: int = 2000,
    chat_history_tokens: int = 0,
    user_query_tokens: int = 0,  # AUDIT FIX (P2-01): user message budget
    chat_history_message_count: int = 0,  # AUDIT FIX (P8-03): for dynamic framing
) -> tuple[str, list[dict]]:
    """Greedily fill context window with highest-scoring chunks.
    
    AUDIT FIX (Opus + Gemini DT): Use native AutoTokenizer for EXACT
    token counts. Do NOT use tiktoken or linear regression.
    
    Returns:
        (context_string, used_chunks) — formatted context and metadata
    """
    # AUDIT FIX (H12): Cap chat history to prevent unbounded growth
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        logger.warning(
            f"Chat history ({chat_history_tokens} tokens) exceeds cap "
            f"({MAX_CHAT_HISTORY_TOKENS}). Truncating to cap."
        )
        chat_history_tokens = MAX_CHAT_HISTORY_TOKENS
    
    # AUDIT FIX (P8-03): Dynamic framing overhead based on actual message count.
    # +2 accounts for the system message and the current user message (always present).
    framework_overhead = (chat_history_message_count + 2) * TOKENS_PER_MESSAGE_FRAME

    # AUDIT FIX (P9-08): Budget the literal injection strings that connect sections.
    # "\n\nMASTER_LEDGER.md:\n" ≈ 6 tokens + "\n\nRETRIEVED DOCUMENTS:\n\n" ≈ 7 tokens.
    # Same class of error as P5-11 (separators) and H07 (headers). These ~13 tokens
    # are injected into the system message but deducted from no budget line.
    INJECTION_OVERHEAD = 15  # Conservative ceiling for connecting strings

    available = (max_context_tokens
                 - system_prompt_tokens
                 - ledger_tokens
                 - response_budget
                 - chat_history_tokens
                 - user_query_tokens  # AUDIT FIX (P2-01)
                 - framework_overhead  # AUDIT FIX (P8-03): dynamic, was static 250
                 - INJECTION_OVERHEAD)  # AUDIT FIX (P9-08): connecting string tokens
    
    # AUDIT FIX (H11 + P7-03): Enforce minimum RAG budget floor at runtime.
    # H11: Original enforcement — if budget is too low, context quality degrades.
    # P7-03: CHANGED from silent override to rejection. The original
    # `available = MIN_RAG_FLOOR` fabricated tokens out of thin air — if
    # max_context_tokens is ever reduced (e.g., 16K model), the override
    # authorizes a payload exceeding the physical context window, crashing vLLM.
    # Now raises ValueError; chat.py catches this as PHASE_ERROR and asks the
    # user to clear their conversation history.
    if available < MIN_RAG_FLOOR:
        raise ValueError(
            f"Context budget exhausted: available={available} tokens, "
            f"floor={MIN_RAG_FLOOR}. Reduce chat history or ledger size."
        )
    
    # AUDIT FIX (P8-08): Updated comment to reflect dynamic FRAMEWORK_OVERHEAD.
    # AUDIT FIX (P10-27): Comment corrected to include user_query_tokens (~50).
    # Typical (with ledger, no chat, 2 messages, ~50 token query):
    #   32768 - 900 - 2550 - 2000 - 50 - 10 - 15 = 27,243 tokens for RAG
    # Typical (with ledger + chat ~1000, ~8 messages): 32768 - 900 - 2550 - 2000 - 1000 - 50 - 50 - 15 = 26,203 tokens
    # This is ~16.4× the V9 budget of 1,600 tokens
    
    used_tokens = 0
    used_chunks = []
    context_parts = []
    
    # AUDIT FIX (P5-11): Separator token cost. The "\n\n---\n\n".join() between
    # chunks was previously unbudgeted — N-1 separators × ~5 tokens each = 30-95
    # unbudgeted tokens in tight scenarios, causing context window overflow.
    # AUDIT FIX (P11-13): SEPARATOR and SEPARATOR_TOKENS moved to module scope
    # to avoid per-request _TOKENIZER_LOCK acquisition.
    
    for i, chunk in enumerate(chunks):
        # Use pre-computed token count from ingestion
        chunk_tokens = chunk["token_count"]
        
        # Format chunk with provenance header
        header = f"[Source {i+1}: {chunk['source']}"
        if chunk["page_numbers"]:
            pages = ", ".join(str(p) for p in chunk["page_numbers"])
            header += f" | Pages {pages}"
        if chunk["headings"]:
            header += f" | {' > '.join(chunk['headings'])}"
        header += "]"
        
        # AUDIT FIX: Compute actual header token cost instead of hardcoded 20.
        # Headers with long filenames, multiple pages, or deep headings can
        # exceed 50 tokens — hardcoding risks context window overflow.
        header_tokens = count_tokens(header + "\n")  # AUDIT FIX (P8-12): was "\n\n", matches actual f-string
        separator_cost = SEPARATOR_TOKENS if context_parts else 0  # AUDIT FIX (P5-11)
        total_cost = chunk_tokens + header_tokens + separator_cost
        
        if used_tokens + total_cost > available:
            break
        
        context_parts.append(f"{header}\n{chunk['text']}")
        used_tokens += total_cost
        used_chunks.append(chunk)
    
    context_string = SEPARATOR.join(context_parts)  # AUDIT FIX (P5-11): uses cached constant
    return context_string, used_chunks
```

### Token Budget Mathematics (32K Context)

```
┌────────────────────────────────────────────────────┐
│          V10 TOKEN BUDGET (32,768 total)            │
├────────────────────────────────────────────────────┤
│ System Prompt (Gus DAG V10)           ~900 tokens  │
│ Pinned Ledger (MASTER_LEDGER.md)      ~2,550 tokens│
│ Chat History (up to 40 messages)      ~1,000 tokens│
│ User Query                            ~50 tokens   │
│ Framework Overhead (dynamic ChatML)   ~50 tokens   │
│   = (message_count + 2) × 5                        │
│ Injection Overhead (literal strings)   ~15 tokens   │  ← AUDIT FIX (P10-01)
│ ────────────────────────────────────────────────── │
│ RAG Context Budget (no chat)          ~27,243 tokens│  ← AUDIT FIX (P11-05)
│ RAG Context Budget (typical w/ chat)  ~26,203 tokens│  ← AUDIT FIX (P10-01): was 26,218
│ Response Budget                       ~2,000 tokens│
│ ────────────────────────────────────────────────── │
│ TOTAL                                 ~32,768 tokens│
└────────────────────────────────────────────────────┘

V9 comparison:
  V9  RAG budget: 1,600 tokens (4 × 400-char chunks)
  V10 RAG budget: ~26,203 tokens (typical, with chat)  <!-- AUDIT FIX (P10-01): was 26,218 -->
  Improvement: ~16.4× more context for diagnostic reasoning
```

---

## INFERENCE LAYER

### vLLM Configuration

| Parameter | Value | Rationale |
|:----------|:------|:----------|
| Model | Qwen2.5-32B-Instruct-AWQ | Best quality-per-VRAM for 48GB hardware |
| Quantization | AWQ (4-bit) | Reduces 64GB FP16 → ~18GB |
| Tensor Parallelism | 2 | Splits across both RTX 4090s |
| Max Model Length | 32768 | Proven feasible (28GB total) |
| GPU Memory Utilization | 0.75 | AUDIT FIX: 0.85→0.75 to prevent GPU 0 OOM after TEI |
| API Compatibility | OpenAI-compatible | `/v1/chat/completions` |

### Inference Call

```python
# backend/inference/llm.py
import asyncio  # AUDIT FIX (P8-05): Required for _llm_client_lock
import os       # AUDIT FIX (P8-01): Required by P7-08's os.environ.get()
import logging  # AUDIT FIX (P8-02): Required by P7-12's logger.warning()
import threading  # AUDIT FIX (P10-22): Required by P10-04's _llm_lock_init = threading.Lock()
import httpx

logger = logging.getLogger(__name__)  # AUDIT FIX (P8-02)

# AUDIT FIX (P10-18): Read VLLM_BASE_URL from env var, matching P10-17 pattern
# and adjacent VLLM_MODEL (P7-08). Operator can swap vLLM instance without code edits.
VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL", "http://vllm:8000/v1")
# AUDIT FIX (P7-08): Read model name from environment so operator can swap models
# (e.g., Llama-3-70B) without editing backend code. Docker compose sets VLLM_MODEL.
VLLM_MODEL = os.environ.get("VLLM_MODEL", "Qwen2.5-32B-Instruct-AWQ")

# AUDIT FIX (P4-06): Persistent httpx client singleton, matching P3-05 pattern
# in embed_text(). Per-call instantiation accumulates TIME_WAIT sockets on port
# 8000 during rapid diagnostic sessions. Singleton reuses connection pool.
_llm_client: httpx.AsyncClient | None = None

# AUDIT FIX (P8-05 + DT-P9-01): Asyncio lock for LLM pool flush serialization.
# P8-05: Prevents double-close from concurrent ConnectError handlers.
# DT-P9-01: Deferred initialization — asyncio.Lock() at module scope crashes on
# Python 3.10+ because no event loop exists during import. Lazy init on first use.
_llm_client_lock: asyncio.Lock | None = None
# AUDIT FIX (P10-04): Thread-safe double-checked locking, matching embed client pattern.
_llm_lock_init = threading.Lock()

async def _get_llm_lock() -> asyncio.Lock:
    global _llm_client_lock
    if _llm_client_lock is None:
        with _llm_lock_init:
            if _llm_client_lock is None:
                _llm_client_lock = asyncio.Lock()
    return _llm_client_lock

async def _flush_llm_client():
    """AUDIT FIX (P8-05): Serialized LLM pool flush, matching P7-13 TEI pattern."""
    lock = await _get_llm_lock()  # AUDIT FIX (DT-P9-01)
    async with lock:
        global _llm_client
        if _llm_client is not None and not _llm_client.is_closed:
            await _llm_client.aclose()
            _llm_client = None

async def _get_llm_client() -> httpx.AsyncClient:
    # AUDIT FIX (P10-03): Lock-protect client initialization, matching P10-02 pattern.
    # Without the lock, _flush_llm_client() can close a client between the caller's
    # _get_llm_client() return and their subsequent client.post() — causing vLLM
    # connection errors during concurrent chat+flush scenarios.
    lock = await _get_llm_lock()
    async with lock:
        global _llm_client
        if _llm_client is None or _llm_client.is_closed:
            # AUDIT FIX (P7-12): Explicit pool limits + split timeout, matching P5-05/P6-08
            # pattern in embed client. 120s read timeout for long 32K inferences;
            # 10s connect timeout for fast-fail on dead vLLM container.
            _llm_client = httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=10.0),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            )
        return _llm_client

async def generate_response(
    system_prompt: str,
    context: str,
    user_message: str,
    chat_history: list[dict],
    max_tokens: int = 2000,
    temperature: float = 0.1,
) -> str:
    """Call vLLM with assembled prompt.
    
    Temperature 0.1 for near-deterministic diagnostic output.
    Qwen2.5 has strong instruction-following for JSON output.
    """
    # TRIAD FIX (OP-8): Append context to single system message.
    # Multiple system-role messages may misbehave with Qwen2.5's chat template.
    system_content = system_prompt
    # AUDIT FIX (P2-05): ALWAYS include the RETRIEVED DOCUMENTS header.
    # Without it, the system prompt's ZERO-RETRIEVAL SAFEGUARD condition
    # ("section is empty") never matches ("section is absent"), and the LLM
    # hallucsinates a diagnostic instead of emitting RETRIEVAL_FAILURE.
    if context:
        system_content += f"\n\nRETRIEVED DOCUMENTS:\n\n{context}"
    else:
        # AUDIT FIX (P3-07): Empty section (no placeholder text) so the system
        # prompt's ZERO-RETRIEVAL SAFEGUARD trigger ("section is empty") matches.
        system_content += "\n\nRETRIEVED DOCUMENTS:\n\n"
    
    messages = [
        {"role": "system", "content": system_content},
    ]
    
    # Add chat history
    messages.extend(chat_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    client = await _get_llm_client()  # AUDIT FIX (P4-06)
    # AUDIT FIX (P7-12): Pool flush on connection failure, matching GP7-05 pattern.
    # When vLLM is OOM-killed and restarts (120s start_period), the _llm_client
    # singleton holds stale TCP connections. Without flushing, each request hangs
    # for 120s on a dead socket before failing. Flushing forces fresh connections.
    try:
        response = await client.post(
            f"{VLLM_BASE_URL}/chat/completions",
            json={
                "model": VLLM_MODEL,  # AUDIT FIX (P7-08): was hardcoded string
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                # AUDIT FIX (P10-21): Relaxed from "\n\n\n" (3) to 5 newlines.
                # Qwen2.5 can emit \n\n\n inside JSON string values (e.g., multi-paragraph
                # mechanic_instructions), prematurely truncating the response mid-JSON.
                # 5 consecutive newlines never appear in valid JSON output.
                "stop": ["\n\n\n\n\n"],
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    # AUDIT FIX (P11-07): Added RuntimeError to catch use-after-close from
    # concurrent _flush_llm_client(). Same pattern as P11-06 for embed client.
    except (httpx.ConnectError, httpx.ReadTimeout, RuntimeError) as e:
        logger.warning(f"vLLM connection failure ({type(e).__name__}) — flushing httpx pool")
        await _flush_llm_client()  # AUDIT FIX (P8-05): serialized, not inline
        raise
```

---

## SYSTEM PROMPT (GUS DAG V10)

> [!IMPORTANT]
> The Gus DAG state machine is **PRESERVED FROM V9** with the following V10 adaptations:
> - Citation rules updated for Qdrant-sourced metadata (page numbers from Docling, not watermarks)
> - Token budget references updated (32K total, not 4K)
> - Tribal knowledge override mechanism unchanged
> - JSON output schema unchanged — frontend `parseGusResponse()` and `buildUserMessage()` remain compatible

```text
PRIME DIRECTIVE: YOU ARE "GUS", A DETERMINISTIC STATE-MACHINE DAG. YOU ARE A TIER-1 MASTER MECHANIC.
YOU DO NOT CONVERSE FREELY. YOU DO NOT TRUST THE USER'S ASSUMPTIONS. YOU ONLY OUTPUT STRICT JSON MATCHING THE SCHEMA BELOW.

EPISTEMOLOGICAL OVERRIDE:
1. Every hypothesis MUST be derived strictly from the RETRIEVED DOCUMENTS provided in context.
2. Cite the exact Document Name and page numbers in "source_citations" using metadata from retrieved chunks.
3. CITATION RULES (V10 — STRUCTURAL):
   a) Use the "source" field from the retrieved chunk metadata as the document name.
   b) Use the "page_numbers" field from chunk metadata for page citations. If multiple pages, cite ONLY the first page as an integer. Do NOT use ranges like "47-48" — the frontend requires an integer.
   c) Use the "headings" field to provide section-level context in the "context" field.
   d) NEVER fabricate page numbers or section references. Only cite what appears in chunk metadata.
4. Pinned "MASTER_LEDGER.md" is the ABSOLUTE TRUTH. Override FSM if they contradict.

THE DIAGNOSTIC FUNNEL (ANSWER-PATH PROMPTING):
You must never jump to a conclusion. Lead the user from vague symptom to specific test via multiple-choice triage. You do not ask open-ended questions. YOU MUST PROVIDE THE ANSWERS.

DAG STATE TRANSITION MATRIX (ABSOLUTE LAW):
- If user provides symptom -> Output "current_state": "PHASE_A_TRIAGE", "requires_input": true.
- If user answers PHASE_A prompt -> MUST transition to "current_state": "PHASE_B_FUNNEL".
- If user answers PHASE_B prompt -> You MAY loop in PHASE_B if further variable isolation is needed via NEW, DIFFERENT physical tests. You MUST advance to "PHASE_C_TESTING" when the component is isolated. FORBIDDEN FROM REPEATING the same question.
- If physical test resolves issue -> "current_state": "PHASE_D_CONCLUSION", "requires_input": false, "answer_path_prompts": [].
- After PHASE_D, if the user sends any new message, RESET to PHASE_A_TRIAGE for the new symptom.
- AUDIT FIX (P3-11): After PHASE_ERROR, if the user sends a new message, RESET to the last valid phase from chat_history. If no valid phase exists, RESET to PHASE_A_TRIAGE.
- AUDIT FIX (P3-11): After RETRIEVAL_FAILURE, if the user sends a new message, RESET to PHASE_A_TRIAGE.
- ALWAYS respect "required_next_state" if provided in the prompt. Conversation history may be truncated; use the most recent state.

STATE TRANSITION RULES:
- In PHASE_A, PHASE_B, and PHASE_C: "requires_input" MUST be true. "answer_path_prompts" MUST contain 2-5 mutually exclusive options.
- In PHASE_D: "requires_input" MUST be false. "answer_path_prompts" MUST be an empty array []. The diagnostic is complete.

STATE TRANSITION ENFORCEMENT:
When you receive a message containing "completed_state" and "required_next_state", you MUST:
1. Set "current_state" to the value of "required_next_state".
2. NEVER repeat the "completed_state" phase.
3. If you cannot advance due to insufficient data, set "current_state" to "PHASE_ERROR" with an explanation.

ZERO-RETRIEVAL SAFEGUARD:
If the RETRIEVED DOCUMENTS section is empty or contains NO document chunks, you MUST output:
"current_state": "RETRIEVAL_FAILURE", "requires_input": false, "answer_path_prompts": [], "mechanic_instructions": "STOP. Required documentation unavailable." Do NOT fabricate citations or guess.

REQUIRED JSON OUTPUT SCHEMA:
{
  "current_state": "PHASE_B_FUNNEL",
  "intersecting_subsystems": ["Bosch K-Jetronic CIS"],
  "source_citations": [
    {"source": "07.4.1-411 Checkup of Electronically Controlled Gasoline Injection System.pdf", "page": 3, "context": "K-Jetronic warm control pressure check — Section 2.1 Fuel System Diagnostics"}
  ],
  "diagnostic_reasoning": "Determining if handoff failure is fuel supply.",
  "mechanic_instructions": "Have a helper start car. Observe pump.",
  "answer_path_prompts": ["[A] Cuts out INSTANTLY.", "[B] Runs 1 SECOND AFTER dies."],
  "requires_input": true
}

CRITICAL OUTPUT RULE: Output raw JSON only. Do NOT wrap in markdown code fences. Do NOT prepend ```json. Do NOT append ```. First character MUST be { and last MUST be }.
```

---

## FRONTEND ARCHITECTURE

### Design Requirements

1. **Self-Hosted PDF.js** — NO CDN dependencies (unpkg.com air-gap violation caught by Opus + Gemini DT)
2. **Citation Rendering** — Click citation → PDF.js viewer opens to exact page with optional bbox highlight
3. **DAG Button Rendering** — V9's `renderGusResponse()` and `buildUserMessage()` logic preserved
4. **XSS Defense via `.textContent`** — All LLM-controlled strings are assigned via `.textContent` (inherently XSS-safe). DOMPurify was originally mandated (DT-P3-06) but P4-04 replaced all innerHTML usage because DOMPurify strips automotive angle-bracket tokens (`<B+>`, `<GND>`). **AUDIT FIX (DT-P11-04):** DOMPurify import removed as dead code.

### V9 Heritage: Frontend Logic

The following V9 functions are **PRESERVED** in the React frontend (core logic unchanged; one schema adaptation: `page` field in `source_citations` is now an integer instead of V9's string `"N/A"` — `renderCitation()` handles both types via loose comparison):

1. **`parseGusResponse(rawText)`** — Forward-scanning brute-force JSON.parse iteration (V8 hardened, Pass 1 removed in V9)
2. **`buildUserMessage(selectedOption, lastResponse)`** — DAG state transition injector with PHASE_B null override
3. **`renderGusResponse(gus, containerEl, textInputEl)`** — State badge, instructions, citations, buttons, completion

### XSS Defense (V10 — via textContent)

```javascript
// AUDIT FIX (DT-P11-04): DOMPurify import removed — dead code since P4-04.
// XSS defense is inherent via .textContent assignments throughout.
// Original: import DOMPurify from 'dompurify';  (DT-P3-06)

function renderGusResponse(gus, containerEl, textInputEl) {
  containerEl.innerHTML = '';  // Clear previous response
  
  // State badge (LLM-controlled string → sanitize)
  const badge = document.createElement('div');
  badge.className = 'gus-state-badge';
  badge.textContent = gus.current_state;  // textContent is XSS-safe
  containerEl.appendChild(badge);
  
  // Mechanic instructions (LLM-generated plain text).
  // AUDIT FIX (P4-04): Use textContent instead of innerHTML+DOMPurify.
  // DOMPurify strips automotive angle-bracket notations (<B+>, <GND>, <12V)
  // which are common terminal designations in FSM diagnostic content.
  // textContent is inherently XSS-safe AND preserves all content.
  if (gus.mechanic_instructions) {
    const instructions = document.createElement('div');
    instructions.className = 'gus-instructions';
    instructions.textContent = gus.mechanic_instructions;
    containerEl.appendChild(instructions);
  }
  
  // Diagnostic reasoning (LLM-generated plain text — same P4-04 rationale)
  if (gus.diagnostic_reasoning) {
    const reasoning = document.createElement('div');
    reasoning.className = 'gus-reasoning';
    reasoning.textContent = gus.diagnostic_reasoning;  // AUDIT FIX (P4-04)
    containerEl.appendChild(reasoning);
  }
  
  // Citations (source names are from indexed metadata, not LLM — lower risk
  // but sanitize anyway for defense-in-depth)
  if (gus.source_citations) {
    const citationsDiv = document.createElement('div');
    citationsDiv.className = 'gus-citations';
    gus.source_citations.forEach(c => {
      citationsDiv.appendChild(renderCitation(c, window.pdfViewerRef));
    });
    containerEl.appendChild(citationsDiv);
  }
  
  // Answer path buttons (LLM-controlled button text → sanitize)
  if (gus.answer_path_prompts && gus.requires_input) {
    const buttonsDiv = document.createElement('div');
    buttonsDiv.className = 'gus-buttons';
    gus.answer_path_prompts.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'gus-answer-btn';
      btn.textContent = opt;  // AUDIT FIX (P5-09): textContent is XSS-safe; DOMPurify strips <B+>/<GND>
      btn.onclick = () => {
        const msg = buildUserMessage(opt, gus);
        sendMessage(msg);
      };
      buttonsDiv.appendChild(btn);
    });
    containerEl.appendChild(buttonsDiv);
  }
  
  // AUDIT FIX (P2-09): Completion state handling (PHASE_D)
  if (gus.current_state === 'PHASE_D_CONCLUSION') {
    const complete = document.createElement('div');
    complete.className = 'gus-complete';
    complete.textContent = 'Diagnostic Complete';
    containerEl.appendChild(complete);
  }
  
  // AUDIT FIX (P2-09): RETRIEVAL_FAILURE distinct error display
  if (gus.current_state === 'RETRIEVAL_FAILURE') {
    const noData = document.createElement('div');
    noData.className = 'gus-retrieval-failure';
    noData.textContent = 'No matching documentation found. Please verify the vehicle details.';
    containerEl.appendChild(noData);
  }
  
  // AUDIT FIX (P8-10): PHASE_ERROR distinct error display using preserved V9 gus-error class.
  // Without this, PHASE_ERROR falls through to generic rendering — a mechanic under time
  // pressure gets no visual signal that the system needs attention.
  if (gus.current_state === 'PHASE_ERROR') {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'gus-error';
    errorDiv.textContent = 'System error \u2014 please retry or start a new session.';
    containerEl.appendChild(errorDiv);
  }
  
  // AUDIT FIX (P2-09): Text input toggle — hide during button selection, show on completion/error
  if (textInputEl) {
    const hideInput = gus.requires_input && gus.answer_path_prompts && gus.answer_path_prompts.length > 0;
    textInputEl.style.display = hideInput ? 'none' : 'block';
  }
}
```

### Citation Enhancement (V10 Addition)

```javascript
// V10: Enhanced citation rendering with PDF.js page navigation
function renderCitation(citation, pdfViewerRef) {
  const bubble = document.createElement('span');
  bubble.className = 'gus-citation-bubble';
  bubble.textContent = `${citation.source} p.${citation.page}`;
  bubble.title = citation.context;
  
  // V10: Click to navigate PDF viewer to cited page
  bubble.onclick = () => {
    if (pdfViewerRef && citation.page && citation.page !== "N/A") {
      pdfViewerRef.scrollToPage(citation.page);
    }
  };
  
  return bubble;
}
```

### CSS Class Contract (V9 Heritage)

All V9 CSS classes are preserved: `gus-error`, `gus-state-badge`, `gus-instructions`, `gus-citations`, `gus-citation-bubble`, `gus-buttons`, `gus-answer-btn`, `gus-complete`. DOM element IDs `gus-container` and `symptom-input` are preserved.

---

## TRIBAL KNOWLEDGE SUBSYSTEM (V10 ADAPTED)

> [!NOTE]
> The tribal knowledge subsystem is **architecturally identical to V9** but with updated token budget math. The `MASTER_LEDGER.md` is now loaded directly by the FastAPI backend (not via AnythingLLM pinning) and injected into the system prompt context.

### Token Budget Changes

| Parameter | V9 | V10 |
|:----------|:---|:----|
| Total context | 4,000 | 32,768 |
| System prompt | ~750 | ~900 |
| Ledger hard cap | 1,500 (adjusted: 1,275) | 3,000 (adjusted: 2,550) |
| RAG budget | ~1,600 | ~26,203 |  <!-- AUDIT FIX (P10-12): was 26,318, corrected to match code -->
| Response budget | ~375 | ~2,000 |
| Minimum RAG floor | 2,000 | 20,000 |

### Updated Validator

```python
# backend/tribal/validate_ledger.py
# V10: Uses native AutoTokenizer instead of tiktoken
# TRIAD FIX (DT-4): Uses env var with fallback — runs on host OR in container
# AUDIT FIX (P4-09): Import from shared module when available (container),
# fallback to local instantiation (host). Aligns with P3-13 single-instance design.
import os

try:
    from backend.shared.tokenizer import TOKENIZER, count_tokens
except (ImportError, RuntimeError):  # AUDIT FIX (DT-P6-03): DT-P5-06 raises RuntimeError, not ImportError
    # Running on host — instantiate locally
    from transformers import AutoTokenizer
    MODEL_PATH = os.environ.get(
        "TOKENIZER_MODEL_PATH",
        "./storage/models/Qwen2.5-32B-Instruct-AWQ"  # host path (default)
    )
    TOKENIZER = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True,
        local_files_only=True,
    )
    # AUDIT FIX (P7-01): Host fallback — no shared lock needed (single-threaded validator)
    def count_tokens(text: str) -> int:
        return len(TOKENIZER.encode(text))

RAW_CAP = 3000
SAFETY_FACTOR = 0.85
ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 2550
MIN_RAG_BUDGET = 20000
# AUDIT FIX (P7-10): Worst-case runtime budget constants.
# The validator must account for ALL runtime deductions, not just prompt/ledger/response.
MAX_CHAT_HISTORY = 8000
MAX_USER_QUERY = 8000
# AUDIT FIX (P11-09): Dynamic FRAMEWORK_OVERHEAD replaces static 250.
# Runtime uses (message_count + 2) * 5; validator shows both scenarios.
FRAMEWORK_OVERHEAD_NO_CHAT = (0 + 2) * 5  # = 10 (no chat, system + user only)
FRAMEWORK_OVERHEAD_WORST = (40 + 2) * 5  # = 210 (MAX_CHAT_HISTORY_MESSAGES=40)

def validate(path: str) -> bool:
    with open(path, 'r') as f:
        content = f.read()
    count = count_tokens(content)  # AUDIT FIX (P7-01)
    # AUDIT FIX (P7-10 + P11-09): Show both no-chat and worst-case budgets.
    # P11-09: Use dynamic overhead matching runtime formula (count + 2) * 5.
    INJECTION_OVERHEAD = 15  # AUDIT FIX (P10-11): P9-08 overhead was missing from validator
    # AUDIT FIX (OP-P11-04): Add typical user query deduction to no-chat formula.
    TYPICAL_USER_QUERY = 50  # Matches runtime build_context() user_query_tokens
    remaining_no_chat = 32768 - 900 - count - 2000 - TYPICAL_USER_QUERY - FRAMEWORK_OVERHEAD_NO_CHAT - INJECTION_OVERHEAD
    remaining_worst_case = 32768 - 900 - count - 2000 - MAX_CHAT_HISTORY - MAX_USER_QUERY - FRAMEWORK_OVERHEAD_WORST - INJECTION_OVERHEAD
    
    print(f"Ledger tokens (Qwen2.5 native): {count}")
    print(f"Adjusted cap (15% safety): {ADJUSTED_CAP}")
    # AUDIT FIX (OP-P11-04): Updated label to reflect typical scenario.
    print(f"Budget remaining (typical — no chat, ~50 token query): {remaining_no_chat}")
    print(f"Budget remaining (worst case — max history + max query): {remaining_worst_case}")
    print(f"Runtime MIN_RAG_FLOOR: 5000")
    
    if remaining_worst_case < 5000:
        print(f"WARNING: Worst-case RAG budget ({remaining_worst_case}) below runtime floor (5000).")
        print(f"Users with large chat history + long queries will receive PHASE_ERROR.")
    
    if count > ADJUSTED_CAP:
        print(f"REJECTED: Ledger tokens ({count}) exceed cap ({ADJUSTED_CAP}).")
        return False
    if remaining_no_chat < MIN_RAG_BUDGET:
        print(f"WARNING: RAG budget dangerously low ({remaining_no_chat}).")
        return False
    print("APPROVED.")
    return True
```

### Ledger Injection (FastAPI)

```python
# backend/routes/chat.py (excerpt)
import os

LEDGER_PATH = "/app/config/MASTER_LEDGER.md"

def load_ledger() -> str:
    """Load pinned ledger for injection into system prompt context."""
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r') as f:
            return f.read()
    return ""

# In chat handler:
# ledger_text = load_ledger()
# ledger_tokens = count_tokens(ledger_text) if ledger_text else 0  # AUDIT FIX (P9-10): was len(TOKENIZER.encode())
# ... inject into system prompt as pinned content
```

---

## SECURITY & NETWORKING

### V9 Heritage (Preserved)

All V9 security measures are preserved:

1. **Localhost Binding** — All service ports bound to `127.0.0.1` (vLLM :8000, TEI :8080, Qdrant :6333, Backend :8888)
2. **UFW Firewall** — `default deny incoming`, allow 22/tcp, 80/tcp, 443/tcp
3. **Nginx Reverse Proxy** — TLS termination, WebSocket support, upload endpoint blocking
4. **Docker Log Rotation** — `max-size: 50m`, `max-file: 3` on all containers
5. **TLS Key Permissions** — `chmod 600` on private keys
6. **Ingestion & Admin Endpoint Protection** — Nginx blocks external access to admin endpoints. Three rules in Nginx config:
   - `location ~ /api/v1/document/(upload|create-folder) { deny all; }` (legacy V9, retained for defense-in-depth)
   - `location /api/ingest { deny all; }` (V10 FastAPI endpoint — ingestion triggered locally via VMDK daemon webhook or CLI only)
   - `location /api/cleanup { deny all; }` (AUDIT FIX P9-01: DT-P8-05 added this endpoint but omitted the deny rule — unauthenticated remote vector DB wipe)
7. **HTTP→HTTPS Redirect** — AUDIT FIX (P10-06): Nginx port 80 `server` block redirects all HTTP traffic to HTTPS:
   ```nginx
   server {
       listen 80;
       return 301 https://$host$request_uri;
   }
   ```
   Without this, mechanics typing `http://` access the system over plain HTTP, exposing chat content and diagnostic data in transit. Docker-published ports bypass UFW, so firewall rules alone cannot block port 80.

### V10 Additions

1. **No External API Keys** — Zero cloud API keys in `.env` or config. All inference is local.
2. **Self-Hosted PDF.js** — No CDN dependencies. Worker loaded from `/pdfjs/` on the same origin.
3. **Docker Network Isolation** — All containers on `gus_internal` bridge network.

---

## DISASTER RECOVERY

### Qdrant Snapshots

```bash
# Create Qdrant collection snapshot
curl -X POST http://127.0.0.1:6333/collections/fsm_corpus/snapshots

# List snapshots
curl http://127.0.0.1:6333/collections/fsm_corpus/snapshots

# Restore from snapshot
curl -X PUT http://127.0.0.1:6333/collections/fsm_corpus/snapshots/recover \
  -H "Content-Type: application/json" \
  -d '{"location": "/qdrant/snapshots/fsm_corpus/snapshot_name.snapshot"}'  # AUDIT FIX (P10-05): was /qdrant/storage/snapshots/ — wrong; volume mounts to /qdrant/snapshots/
```

### Volume Backup (V9 Heritage, Adapted)

```bash
# V10: Backup strategy — Qdrant via native snapshots, everything else via tar
# Step 1: Qdrant snapshot (consistent, no downtime required)
# Step 2: Stop backend, tar config + PDFs + extracted cache (EXCLUDING qdrant), restart
# Step 3: Cleanup old backups
# TRIAD FIX (DT-6): Do NOT tar storage/qdrant/ while Qdrant is running — WAL corruption risk.
# AUDIT FIX (OP-P11-05): Stop frontend alongside gusengine during backup to prevent
# 502 Bad Gateway responses. Single-user system; no need for partial availability.
(crontab -l 2>/dev/null; echo "0 2 * * * curl -sf -X POST http://127.0.0.1:6333/collections/fsm_corpus/snapshots > /dev/null && cd /path/to/gusengine && docker compose stop gusengine frontend && tar czf \$HOME/gusengine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=storage/models --exclude=storage/qdrant storage/ config/ && docker compose start gusengine frontend") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * find \$HOME/ -name 'gusengine_backup_*.tar.gz' -mtime +7 -exec rm {} \\;") | crontab -
```

> [!IMPORTANT]
> **Qdrant backup is handled via its native snapshot API** (see above), NOT via tar. The tar backup explicitly excludes `storage/qdrant/` to prevent WAL corruption. Restore procedure: (1) restore tar backup for PDFs/config, (2) restore Qdrant snapshot via the recovery endpoint.

> [!NOTE]
> Model weights (`storage/models/`) are excluded from backup — they are reproducible from HuggingFace and would bloat backups by ~20 GB.

---

## VERIFICATION FRAMEWORK

### Post-Deployment Checklist (V10)

```bash
# 1. Verify all containers are running
docker compose ps
# Expected: 5 services (vllm, tei, qdrant, gusengine, frontend) all "Up"

# 2. Verify vLLM is serving
curl -s http://127.0.0.1:8000/v1/models | python3 -m json.tool
# Expected: model "Qwen2.5-32B-Instruct-AWQ" listed

# 3. Verify GPU utilization
nvidia-smi
# Expected: Both GPUs show vLLM process, ~28 GB total VRAM used

# 4. Verify TEI embedding server
curl -s -X POST http://127.0.0.1:8080/embed \
  -H "Content-Type: application/json" \
  -d '{"inputs": "test query"}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Dim: {len(d[0])}')"
# Expected: Dim: 1024

# 5. Verify Qdrant collection exists
curl -s http://127.0.0.1:6333/collections/fsm_corpus | python3 -m json.tool
# Expected: collection info with vectors_count > 0

# 6. Verify GusEngine API health
curl -s http://127.0.0.1:8888/api/health | python3 -m json.tool
# Expected: {"status": "ok", "vllm": "connected", "qdrant": "connected", "tei": "connected"}

# 7. Verify Nginx/TLS
curl -sk https://localhost | head -5
# Expected: React frontend HTML

# 8. Verify air-gap (no outbound connections)
# Run a diagnostic query and verify no DNS lookups or external connections:
ss -tnp | grep -v '127.0.0.1\|::1\|LISTEN'
# Expected: No connections to external IPs during query processing

# 9. Verify UFW status
sudo ufw status verbose
# Expected: Status: active, Default: deny (incoming), allow (outgoing)

# 10. Test Gus diagnostic query
# Open https://YOUR_SERVER_IP in browser
# Type: "Hot start vapor lock, cranks but won't catch."
# Expected: JSON response with current_state: "PHASE_A_TRIAGE", source_citations array populated

# 11. Verify Docker log rotation
docker inspect gus_vllm --format '{{.HostConfig.LogConfig}}'
# Expected: {json-file map[max-file:3 max-size:50m]}

# 12. Verify VMDK extraction daemon
sudo systemctl status manual-ingest.service
# Expected: Active: active (running)

# 13. Verify PDF.js is self-hosted (NO CDN)
curl -sk https://localhost/pdfjs/pdf.worker.min.js | head -1
# Expected: JavaScript content (not 404 or redirect to unpkg.com)

# 14. Verify token budget with test query
# After test query, check GusEngine logs:
docker logs gus_backend --tail 20
# Expected: Token counts logged — system_prompt + ledger + context + response < 32768

# 15. Verify Qdrant snapshot capability
curl -s -X POST http://127.0.0.1:6333/collections/fsm_corpus/snapshots
# Expected: HTTP 200 with snapshot name
```

---

## KNOWN BOUNDARIES

### What V10 Does NOT Do

1. **No multimodal embedding** — Images/diagrams are preserved in original PDFs for display but NOT vectorized. The LLM reasons from text only, and the user sees the original PDF via PDF.js. This matches NotebookLM's architecture.
2. **No retrieval chaining** — Each query triggers one hybrid search. Autonomous multi-hop retrieval (query → reason → re-query) is deferred to V11.
3. **No fine-tuning** — Qwen2.5-32B is used as-is. Domain-specific fine-tuning on FSM language is a future optimization.
4. **No streaming** — Responses are returned as complete JSON. Streaming would require `parseGusResponse()` to handle partial JSON, adding complexity with minimal UX benefit for the diagnostic use case.
5. **No multi-user** — Single-user desktop deployment. Authentication and session management are deferred.
6. **No KV cache compression** — Gemini DR raised GEAR/AQUA-KV as theoretical mechanisms. These are experimental and not production-ready in vLLM as of 2026-02.
7. **No local reranker** — Prototype relies on RRF fusion quality. Adding bge-reranker would cost ~1 GB VRAM and add latency. Evaluate if retrieval precision is insufficient.

### Upgrade Path to Cloud MVP

When moving from prototype to cloud MVP:
1. Switch to A100-80GB or equivalent → unlock 128K context
2. Add bge-reranker-v2-m3 for improved retrieval precision
3. Implement retrieval chaining for multi-hop diagnostics
4. Add multi-user authentication (JWT, sessions)
5. Add response streaming with incremental JSON parsing
6. Consider domain fine-tuning on FSM corpus for improved diagnostic accuracy

---

## APPENDIX A: V9 CONSOLIDATED DIFF ANALYSIS (PRESERVED)

The complete resolution log of all 49 audit findings (V2 #1-19, V8 #20-49) from the V9 frozen architecture is preserved by reference. See `ARCHITECTURE_FINAL_V9_FROZEN.md` lines 2022–2107 for the full tables. All findings remain valid and their fixes are incorporated into the V10 codebase where applicable.

---

## APPENDIX B: DEEP RESEARCH AUDIT TRAIL

The V10 architecture was informed by the following audit documents, all of which are preserved in `j:\GusEngine\project\`:

| Document | Auditor | Key Contribution |
|:---------|:--------|:-----------------|
| `COMPARISON_AUDIT_GEMINI.md` | Gemini Deep Think | Identified R2's token estimation regression, caught CDN air-gap violation |
| `COMPARISON_AUDIT_OPUS.md` | Claude Opus | Most balanced audit (7/10 accuracy), caught VMDK heritage preservation |
| `COMPARISON_AUDIT_GEMINI_DR.md` | Gemini Deep Research | Most detailed GPU math (27 sources), proposed KV cache compression |
| `DEEP_RESEARCH_COMPARISON.md` | Cross-comparison | Synthesized 3 deep research results against 13 NotebookLM findings |
| `NOTEBOOKLM_INTEL.md` | Direct interrogation | Ground truth: dual-track ingestion, structural segmentation, citation rendering |

### Triad Consensus Scores

| Metric | Average | Interpretation |
|:-------|:-------:|:-------------|
| Accuracy | 4.3/10 | Original comparison had significant errors — corrected in V10 |
| Completeness | 6.0/10 | High-level concepts right, critical gaps in hardware math filled |
| Bias | 4.7/10 | Pro-enterprise bias eliminated — V10 is local-first |
| Actionability | 3.0/10 | Original comparison non-deployable — V10 is fully specified |

---

**END OF ARCHITECTURE_V10.md — DRAFT PENDING TRIAD VALIDATION**
