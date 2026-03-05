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

version: "3.8"

services:
  # ─── LLM Inference (vLLM) ───
  vllm:
    image: vllm/vllm-openai:latest
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
      test: ["CMD-SHELL", "curl -sf http://localhost:8000/health || exit 1"]
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
    image: ghcr.io/huggingface/text-embeddings-inference:latest
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
      - gusengine
    networks:
      - gus_internal
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

# Download PDF.js for self-hosted frontend (NO CDN)
# V10 FIX: Opus and Gemini DT both flagged R3's unpkg.com CDN dependency
# as an air-gap violation. PDF.js worker MUST be self-hosted.
# TRIAD FIX (OP-13): Use official npm registry, not third-party GitHub fork.
cd ./frontend && npm pack pdfjs-dist@4.0.379 && \
  tar xzf pdfjs-dist-4.0.379.tgz && \
  mkdir -p public/pdfjs && \
  cp package/build/* public/pdfjs/ && \
  rm -rf package pdfjs-dist-4.0.379.tgz && cd ..

# AUDIT FIX (DT-P3-06): DOMPurify for XSS sanitization (air-gap requirement).
# renderGusResponse() calls DOMPurify.sanitize() throughout — without this
# dependency present, ReferenceError crashes the UI on first LLM response.
cd ./frontend && npm install dompurify && cd ..

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
from backend.shared.tokenizer import TOKENIZER  # AUDIT FIX (P3-13): single shared instance
import os

def create_converter():
    """Create Docling converter with OCR enabled for scanned PDFs."""
    pipeline_options = PdfPipelineOptions(
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
    - source: original filename
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
    
    chunker = HybridChunker(
        # AUDIT FIX (DT-7): Docling requires its own BaseTokenizer protocol.
        # Raw HuggingFace AutoTokenizer throws TypeError/AttributeError.
        tokenizer=HuggingFaceTokenizer(tokenizer=TOKENIZER),
        max_tokens=max_tokens,
        merge_peers=True,  # Merge adjacent same-level sections
    )
    
    try:
        chunk_iter = chunker.chunk(doc)  # AUDIT FIX: lazy generator, not list() — avoids OOM on large PDFs
    except Exception as e:
        logger.error(f"CHUNKER FAILURE: {pdf_path} — {e}")
        raise IngestionError(f"Chunking failed for {pdf_path}: {e}") from e
    
    chunks = []
    for chunk in chunk_iter:
        text = chunk.text
        if not text or not text.strip():
            continue  # Skip empty chunks (OCR failures on blank pages)
        token_count = len(TOKENIZER.encode(text))
        
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
            "source": os.path.basename(pdf_path),
            "page_numbers": page_numbers,
            "headings": headings,
            "token_count": token_count,
        })
    
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
from qdrant_client import QdrantClient
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
    client.upsert(
        collection_name="fsm_corpus",
        points=[{
            "id": chunk_id,
            "vector": {
                "dense": dense_vector,
                "sparse": {
                    "indices": sparse_vector["indices"],
                    "values": sparse_vector["values"],
                }
            },
            "payload": {
                "text": chunk["text"],
                "source": chunk["source"],
                "page_numbers": chunk["page_numbers"],
                "headings": chunk["headings"],
                "token_count": chunk["token_count"],
            }
        }]
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

qdrant_client = QdrantClient(url=os.environ.get("QDRANT_URL", "http://qdrant:6333"))
```

> [!NOTE]
> **AUDIT FIX (P3-13): Shared tokenizer singleton.** Both `parser.py` and `context_builder.py`
> previously instantiated their own `AutoTokenizer.from_pretrained()` — loading ~50-100MB of
> vocabulary data each. Now both import from a single module:

```python
# backend/shared/tokenizer.py
import os
from transformers import AutoTokenizer

# AUDIT FIX (P4-11): Pre-check model directory with clear error message.
# Without this, a missing volume mount produces a confusing ImportError
# traceback deep in the transformers library. Matches P2-12 pattern.
_MODEL_PATH = "/app/models/Qwen2.5-32B-Instruct-AWQ"
if not os.path.isdir(_MODEL_PATH):
    raise SystemExit(
        f"Fatal: tokenizer model directory not found at {_MODEL_PATH}. "
        f"Ensure model weights are pre-downloaded to ./storage/models/."
    )

TOKENIZER = AutoTokenizer.from_pretrained(
    _MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True,
)
```

> [!IMPORTANT]
> **AUDIT FIX (P3-03): Collection auto-creation at startup.** Without this, a fresh deployment
> receiving a `/api/chat` request before any PDF is ingested hits a Qdrant 404 on the
> non-existent `fsm_corpus` collection. The error handler returns PHASE_ERROR but with a
> misleading "search system temporarily unavailable" message.

```python
# backend/main.py (startup hook)
from backend.shared.clients import qdrant_client
from backend.indexing.qdrant_setup import create_collection
from qdrant_client.http.exceptions import UnexpectedResponse
import asyncio

@app.on_event("startup")
async def ensure_qdrant_collection():
    """Create collection if it doesn't exist. Retry on transient failure."""
    # AUDIT FIX (P3-03 + P4-07): Idempotent collection creation with retry.
    # P3-03: Fresh deployment hits 404 without this.
    # P4-07: If Qdrant is still loading persistence, create_collection() fails.
    # Without retry, FastAPI launches silently with no collection → permanent PHASE_ERROR.
    for attempt in range(5):
        try:
            qdrant_client.get_collection("fsm_corpus")
            logger.info("Qdrant collection 'fsm_corpus' verified.")
            return
        except Exception:
            try:
                create_collection(qdrant_client)
                logger.info("Qdrant collection 'fsm_corpus' created.")
                return
            except Exception as e:
                logger.warning(f"Qdrant not ready (attempt {attempt+1}/5): {e}")
                await asyncio.sleep(2 ** attempt)  # Backoff: 1, 2, 4, 8, 16s
    logger.critical("FATAL: Could not verify/create Qdrant collection after 5 attempts.")
    raise SystemExit("Qdrant collection setup failed — aborting startup.")
```

### TEI Embedding Client

> [!IMPORTANT]
> **TRIAD FIX (OP-2, OP-6):** The original V10 draft showed how to store and search embeddings but was missing the code that actually GENERATES them via TEI. This section fills that gap. It also validates that TEI exposes sparse vector support for BGE-M3.

```python
# backend/embedding/client.py
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

TEI_BASE_URL = "http://tei:80"

# AUDIT FIX (P3-05): Persistent httpx client instead of per-call instantiation.
# During bulk ingestion (100K+ chunks), creating/destroying an HTTP client per
# embed call exhausts ephemeral ports and accumulates TIME_WAIT sockets.
_http_client: httpx.AsyncClient | None = None

async def _get_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=30.0)
    return _http_client

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
```

### Ingestion Orchestration

```python
# backend/ingestion/pipeline.py
import asyncio
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
INGEST_SEMAPHORE = asyncio.Semaphore(2)

# AUDIT FIX (P3-04): Rate-limit concurrent TEI embedding requests.
# The INGEST_SEMAPHORE gates parse_and_chunk (CPU-bound) but the embed loop runs
# outside it. With 500+ PDFs queued, dozens enter the embed phase simultaneously,
# flooding TEI with concurrent HTTP requests and causing httpx timeouts.
EMBED_SEMAPHORE = asyncio.Semaphore(8)  # TEI handles ~8 concurrent requests efficiently

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
    async with INGEST_SEMAPHORE:
        chunks = await asyncio.to_thread(parse_and_chunk, pdf_path)
    
    if not chunks:
        # AUDIT FIX (DT-5b): Zero extractable text = silent failure.
        # Raise IngestionError so the V9 quarantine logic activates.
        raise IngestionError(f"No chunks extracted from {pdf_path} — likely blank/corrupt PDF")
    
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
            async with EMBED_SEMAPHORE:
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
        except Exception as e:
            logger.warning(f"Chunk {i}/{len(chunks)} failed for {pdf_path}: {e} — skipping")
            continue
    
    logger.info(f"Indexed {len(chunks)} chunks from {pdf_path}")
    return len(chunks)

# AUDIT FIX (P2-06): Background task wrapper with error handling.
# When called via FastAPI BackgroundTasks, exceptions are silently swallowed.
# This wrapper catches IngestionError, logs it, and writes to a failure manifest
# so the V9 daemon (or operator) can identify failed ingestions.
async def ingest_pdf_background(pdf_path: str, client: QdrantClient):
    """Wrapper for BackgroundTask execution with error handling."""
    try:
        count = await ingest_pdf(pdf_path, client)
        logger.info(f"Background ingestion complete: {pdf_path} ({count} chunks)")
    except IngestionError as e:
        logger.error(f"INGESTION FAILED (quarantine candidate): {pdf_path} — {e}")
        # Write to failure manifest for operator/daemon re-check
        with open("/app/storage/extracted/.ingest_failures.log", "a") as f:
            f.write(f"{pdf_path}\t{e}\n")
    except Exception as e:
        logger.error(f"UNEXPECTED INGESTION ERROR: {pdf_path} — {e}", exc_info=True)
        # AUDIT FIX (P3-09): Also log unexpected errors to failure manifest
        # (previously only IngestionError was written — operator would miss these)
        with open("/app/storage/extracted/.ingest_failures.log", "a") as f:
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
> import os
> from fastapi import APIRouter, BackgroundTasks, Request
> from backend.shared.clients import qdrant_client  # AUDIT FIX (P2-04)
> 
> router = APIRouter()
> ALLOWED_PDF_DIR = "/app/pdfs"  # AUDIT FIX (P2-11): path traversal prevention
> 
> @router.post("/api/ingest", status_code=202)
> async def ingest(request: Request, background_tasks: BackgroundTasks):
>     body = await request.json()
>     pdf_path = os.path.realpath(body["pdf_path"])
>     # AUDIT FIX (P2-11 + DT-P3-04): Validate path is within allowed directory.
>     # DT-P3-04: Trailing slash prevents sibling dir bypass ("/app/pdfs_keys/...")
>     if not pdf_path.startswith(ALLOWED_PDF_DIR + "/"):
>         return {"status": "rejected", "message": "Path outside allowed directory"}
>     if not pdf_path.endswith(".pdf"):
>         return {"status": "rejected", "message": "Not a PDF file"}
>     background_tasks.add_task(ingest_pdf_background, pdf_path, qdrant_client)
>     return {"status": "accepted", "message": f"Ingestion queued for {pdf_path}"}
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
import logging
from fastapi import APIRouter, Request
from backend.embedding.client import embed_text
from backend.search import hybrid_search
from backend.inference.context import build_context, load_ledger, TOKENIZER  # AUDIT FIX (P2-03)
from backend.inference.llm import generate_response
from backend.shared.clients import qdrant_client  # AUDIT FIX (P2-04)

logger = logging.getLogger(__name__)

router = APIRouter()

# AUDIT FIX (P2-12): Explicit startup failure instead of confusing ImportError
_PROMPT_PATH = "/app/config/system_prompt.txt"
if os.path.exists(_PROMPT_PATH):
    SYSTEM_PROMPT = open(_PROMPT_PATH).read()
else:
    logger.critical(f"SYSTEM PROMPT NOT FOUND: {_PROMPT_PATH}")
    raise SystemExit(f"Fatal: system prompt missing at {_PROMPT_PATH}")

@router.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_query = body["message"]
    chat_history = body.get("chat_history", [])
    
    # Step 1: Load ledger (may be empty if file missing — degrades gracefully)
    ledger_text = load_ledger()
    ledger_tokens = len(TOKENIZER.encode(ledger_text)) if ledger_text else 0
    
    # Step 2: Compute chat history token cost
    chat_history_tokens = sum(
        len(TOKENIZER.encode(m["content"])) for m in chat_history
    )
    
    # AUDIT FIX (P2-02): Physically truncate chat_history array to match budget cap.
    # Without this, build_context() caps the budget MATH at 8000 tokens but
    # generate_response() still sends ALL messages to vLLM, overshooting 32K.
    # Evict oldest messages first (preserve recent diagnostic context).
    MAX_CHAT_HISTORY_TOKENS = 8000
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        truncated = []
        running = 0
        for msg in reversed(chat_history):
            msg_tokens = len(TOKENIZER.encode(msg["content"]))
            if running + msg_tokens > MAX_CHAT_HISTORY_TOKENS and truncated:
                break  # AUDIT FIX (P3-02): Only break if we already kept ≥1 message
            truncated.insert(0, msg)
            running += msg_tokens
        # AUDIT FIX (DT-P3-07 + P4-03): Eviction may split a user/assistant pair,
        # leaving a dangling assistant message first. Qwen2.5 chat template expects
        # user-first after system prompt — strip the orphan to prevent errors.
        # P4-03: Only strip if it won't empty the history (preserves P3-02 guarantee).
        if truncated and truncated[0]["role"] == "assistant":
            if len(truncated) > 1:
                chat_history_tokens_removed = len(TOKENIZER.encode(truncated[0]["content"]))
                truncated.pop(0)
                running -= chat_history_tokens_removed
            else:
                logger.warning("Skipping assistant-strip: would empty chat history (P3-02 guard)")
        chat_history = truncated
        chat_history_tokens = running
        
        # AUDIT FIX (P4-02): If P3-02 kept a single oversized message, its actual
        # tokens exceed MAX_CHAT_HISTORY_TOKENS. build_context() uses this value for
        # budget math — if we don't truncate here, budget math says 8000 but vLLM
        # receives 9000, causing a ~1000-token overflow → HTTP 400.
        # Force-truncate the message content to fit the budget.
        if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS and len(chat_history) == 1:
            msg = chat_history[0]
            tokens = TOKENIZER.encode(msg["content"])
            if len(tokens) > MAX_CHAT_HISTORY_TOKENS:
                msg["content"] = TOKENIZER.decode(tokens[:MAX_CHAT_HISTORY_TOKENS])
                logger.warning(
                    f"Truncated oversized chat message from {len(tokens)} to "
                    f"{MAX_CHAT_HISTORY_TOKENS} tokens (P4-02)"
                )
                chat_history_tokens = MAX_CHAT_HISTORY_TOKENS
    
    # AUDIT FIX (H09/H10/H13): Comprehensive error handling for the entire
    # embed → search → generate pipeline. Without this, TEI crash, Qdrant 404,
    # or vLLM OOM all produce raw HTTP 500 with Python tracebacks visible to
    # the mechanic. Each failure now returns structured JSON with PHASE_ERROR.
    try:
        # Step 3: Embed user query for retrieval
        # AUDIT FIX (P4-05): Acquire EMBED_SEMAPHORE so chat competes fairly
        # with ingestion. Without this, during bulk ingestion all 8 permits are
        # held and chat sends an unthrottled 9th request → TEI overload.
        from backend.ingestion.pipeline import EMBED_SEMAPHORE
        async with EMBED_SEMAPHORE:
            query_dense, query_sparse = await embed_text(user_query)
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
        # AUDIT FIX (P3-08): hybrid_search() uses synchronous QdrantClient —
        # dispatch to threadpool to avoid blocking event loop and health checks.
        results = await asyncio.to_thread(
            hybrid_search, qdrant_client, query_dense, query_sparse
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
    # AUDIT FIX (P2-01): Include user query tokens in budget deduction
    user_query_tokens = len(TOKENIZER.encode(user_query))
    
    # AUDIT FIX (DT-P3-03): Hard cap on query length BEFORE budget math.
    # Without this, a 25K-token paste-bomb makes available go negative (-5682),
    # MIN_RAG_FLOOR forces available=5000, and the total prompt (41,450 tokens)
    # exceeds vLLM's 32,768 limit → HTTP 400 crash.
    MAX_USER_QUERY_TOKENS = 10000
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
    # AUDIT FIX (P3-01): build_context() returns tuple[str, list[dict]].
    # Destructure the return value — without this, `context` is the raw tuple
    # and f-string formatting injects Python tuple repr into the LLM prompt.
    context, used_chunks = build_context(
        results,
        ledger_tokens=ledger_tokens,
        chat_history_tokens=chat_history_tokens,
        user_query_tokens=user_query_tokens,
    )
    
    # Step 6: Assemble system prompt WITH ledger (injection point)
    # Ledger goes INSIDE the system prompt, before RAG context
    system_prompt = SYSTEM_PROMPT
    if ledger_text:
        system_prompt += f"\n\nMASTER_LEDGER.md:\n{ledger_text}"
    
    try:
        # Step 7: Generate LLM response (context appended in generate_response)
        response = await generate_response(
            system_prompt=system_prompt,
            context=context,
            user_message=user_query,
            chat_history=chat_history,
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
    
    # AUDIT FIX (P3-12 + P4-10): Validate LLM output is valid JSON with required schema.
    # P3-12: Qwen2.5 may ignore JSON instruction and return prose.
    # P4-10: Even valid JSON may have wrong schema (e.g. {"answer":"yes"}).
    # Without current_state, frontend shows "undefined" badge — unprofessional.
    try:
        parsed = json.loads(response)
        if not isinstance(parsed, dict) or "current_state" not in parsed:
            raise ValueError("Missing required 'current_state' field")
    except (json.JSONDecodeError, ValueError):
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
    query_sparse: dict,
    top_k: int = 20,
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
    
    results = client.query_points(
        collection_name="fsm_corpus",
        prefetch=prefetch_list,
        query=FusionQuery(fusion=Fusion.RRF),
        limit=top_k,
    )
    
    if not results.points:
        return []
    
    # AUDIT FIX: Absolute score floor — if even the best result is below
    # min_absolute_score, the query is off-topic and ALL results are irrelevant.
    # This prevents irrelevant chunks from being returned for out-of-corpus queries.
    top_score = results.points[0].score
    if top_score < min_absolute_score:
        logger.warning(f"Top RRF score {top_score:.4f} below absolute floor {min_absolute_score} — discarding all results")
        return []
    
    # Dynamic threshold: keep chunks within 30% of top RRF score
    # TRIAD FIX (DT-5, DR-2): RRF scores cluster tightly in [1/(k+N), 1/(k+1)].
    # With k=60 and top_k=20, scores range [0.0125, 0.0164].
    # A ratio of 0.70 keeps scores >= ~0.0115, filtering only chunks that
    # appeared in only one signal with very low rank.
    # For more aggressive filtering, raise to 0.85 or add a rank-based cutoff.
    threshold = top_score * min_score_ratio
    
    filtered = []
    for point in results.points:
        if point.score >= threshold:
            filtered.append({
                "text": point.payload["text"],
                "source": point.payload["source"],
                "page_numbers": point.payload["page_numbers"],
                "headings": point.payload["headings"],
                "token_count": point.payload["token_count"],
                "score": point.score,
            })
    
    return filtered
```

### Greedy Token-Capped Context Injection

> [!IMPORTANT]
> **NotebookLM Parity:** NotebookLM injects "raw, sequential plain-text strings divided into numerical excerpts" — NOT a fixed number of chunks. V10 replicates this by greedily filling the context window with the highest-scoring chunks until the token budget is exhausted.

```python
# backend/retrieval/context_builder.py
import logging  # AUDIT FIX (P3-06)
from backend.shared.tokenizer import TOKENIZER  # AUDIT FIX (P3-13): single shared instance

logger = logging.getLogger(__name__)  # AUDIT FIX (P3-06)

# AUDIT FIX (H11): Runtime RAG budget floor — prevents long conversations from
# silently pushing RAG context to zero or negative. The ledger validator uses
# MIN_RAG_BUDGET=20000, but at runtime we use a lower floor to allow some
# degradation before hard-cutting chat history.
MIN_RAG_FLOOR = 5000  # Minimum tokens reserved for RAG context at runtime
MAX_CHAT_HISTORY_TOKENS = 8000  # AUDIT FIX (H12): Hard cap on chat history

def build_context(
    chunks: list[dict],
    max_context_tokens: int = 32768,
    system_prompt_tokens: int = 900,
    ledger_tokens: int = 0,
    response_budget: int = 2000,
    chat_history_tokens: int = 0,
    user_query_tokens: int = 0,  # AUDIT FIX (P2-01): user message budget
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
    
    available = (max_context_tokens
                 - system_prompt_tokens
                 - ledger_tokens
                 - response_budget
                 - chat_history_tokens
                 - user_query_tokens)  # AUDIT FIX (P2-01)
    
    # AUDIT FIX (H11): Enforce minimum RAG budget floor at runtime.
    # If available < MIN_RAG_FLOOR after all deductions, warn and enforce.
    if available < MIN_RAG_FLOOR:
        logger.warning(
            f"RAG budget ({available} tokens) below floor ({MIN_RAG_FLOOR}). "
            f"Chat history may need eviction upstream."
        )
        available = MIN_RAG_FLOOR
    
    # Typical (with ledger, no chat): 32768 - 900 - 2550 - 2000 - 0 = 27,318 tokens for RAG
    # Typical (with ledger + chat ~1000): 26,318 tokens — see budget diagram below
    # This is ~16.4× the V9 budget of 1,600 tokens
    
    used_tokens = 0
    used_chunks = []
    context_parts = []
    
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
        header_tokens = len(TOKENIZER.encode(header + "\n\n"))
        total_cost = chunk_tokens + header_tokens
        
        if used_tokens + total_cost > available:
            break
        
        context_parts.append(f"{header}\n{chunk['text']}")
        used_tokens += total_cost
        used_chunks.append(chunk)
    
    context_string = "\n\n---\n\n".join(context_parts)
    return context_string, used_chunks
```

### Token Budget Mathematics (32K Context)

```
┌─────────────────────────────────────────────────┐
│          V10 TOKEN BUDGET (32,768 total)         │
├─────────────────────────────────────────────────┤
│ System Prompt (Gus DAG V10)        ~900 tokens  │
│ Pinned Ledger (MASTER_LEDGER.md)   ~2,550 tokens│
│ Chat History (last 4 turns)        ~1,000 tokens│
│ ─────────────────────────────────────────────── │
│ RAG Context Budget                ~26,318 tokens│
│ Response Budget                    ~2,000 tokens│
│ ─────────────────────────────────────────────── │
│ TOTAL                             ~32,768 tokens│
└─────────────────────────────────────────────────┘

V9 comparison:
  V9  RAG budget: 1,600 tokens (4 × 400-char chunks)
  V10 RAG budget: ~26,318 tokens
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
import httpx

VLLM_BASE_URL = "http://vllm:8000/v1"

# AUDIT FIX (P4-06): Persistent httpx client singleton, matching P3-05 pattern
# in embed_text(). Per-call instantiation accumulates TIME_WAIT sockets on port
# 8000 during rapid diagnostic sessions. Singleton reuses connection pool.
_llm_client: httpx.AsyncClient | None = None

async def _get_llm_client() -> httpx.AsyncClient:
    global _llm_client
    if _llm_client is None or _llm_client.is_closed:
        _llm_client = httpx.AsyncClient(timeout=120.0)
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
    response = await client.post(
        f"{VLLM_BASE_URL}/chat/completions",
        json={
            "model": "Qwen2.5-32B-Instruct-AWQ",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": ["\n\n\n"],  # Prevent runaway generation
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
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
4. **DOMPurify** — All LLM-controlled strings MUST be sanitized before innerHTML. V9 warned about this risk (V9 FROZEN L1549); V10 mandates DOMPurify integration in `renderGusResponse()` as a **V10 ADDITION** (the V9 function logic is otherwise unchanged).

### V9 Heritage: Frontend Logic

The following V9 functions are **PRESERVED** in the React frontend (core logic unchanged; one schema adaptation: `page` field in `source_citations` is now an integer instead of V9's string `"N/A"` — `renderCitation()` handles both types via loose comparison):

1. **`parseGusResponse(rawText)`** — Forward-scanning brute-force JSON.parse iteration (V8 hardened, Pass 1 removed in V9)
2. **`buildUserMessage(selectedOption, lastResponse)`** — DAG state transition injector with PHASE_B null override
3. **`renderGusResponse(gus, containerEl, textInputEl)`** — State badge, instructions, citations, buttons, completion

### DOMPurify Integration (V10 Addition)

```javascript
// V10 ADDITION: Sanitize ALL LLM-controlled strings before innerHTML.
// Prevents XSS from prompt injection or model-echoed payloads.
import DOMPurify from 'dompurify';  // AUDIT FIX (DT-P3-06): Must be installed, not commented out

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
      btn.textContent = DOMPurify.sanitize(opt);  // textContent + sanitize = belt-and-suspenders
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
| RAG budget | ~1,600 | ~26,318 |
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
    from backend.shared.tokenizer import TOKENIZER
except ImportError:
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

RAW_CAP = 3000
SAFETY_FACTOR = 0.85
ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 2550
MIN_RAG_BUDGET = 20000

def validate(path: str) -> bool:
    with open(path, 'r') as f:
        content = f.read()
    count = len(TOKENIZER.encode(content))
    remaining = 32768 - 900 - count - 2000  # total - prompt - ledger - response (count <= 2550)
    
    print(f"Ledger tokens (Qwen2.5 native): {count}")
    print(f"Adjusted cap (15% safety): {ADJUSTED_CAP}")
    print(f"Budget remaining (RAG + history): {remaining}")
    print(f"Minimum RAG budget floor: {MIN_RAG_BUDGET}")
    
    if count > ADJUSTED_CAP:
        print(f"REJECTED: Ledger tokens ({count}) exceed cap ({ADJUSTED_CAP}).")
        return False
    if remaining < MIN_RAG_BUDGET:
        print(f"WARNING: RAG budget dangerously low ({remaining}).")
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
# ledger_content = load_ledger()
# ledger_tokens = len(TOKENIZER.encode(ledger_content))
# ... inject into messages as system-level pinned content
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
6. **Ingestion Endpoint Protection** — Nginx blocks external access to ingestion endpoints. Two rules in Nginx config:
   - `location ~ /api/v1/document/(upload|create-folder) { deny all; }` (legacy V9, retained for defense-in-depth)
   - `location /api/ingest { deny all; }` (V10 FastAPI endpoint — ingestion triggered locally via VMDK daemon webhook or CLI only)

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
  -d '{"location": "/qdrant/storage/snapshots/fsm_corpus/snapshot_name.snapshot"}'
```

### Volume Backup (V9 Heritage, Adapted)

```bash
# V10: Backup strategy — Qdrant via native snapshots, everything else via tar
# Step 1: Qdrant snapshot (consistent, no downtime required)
# Step 2: Stop backend, tar config + PDFs + extracted cache (EXCLUDING qdrant), restart
# Step 3: Cleanup old backups
# TRIAD FIX (DT-6): Do NOT tar storage/qdrant/ while Qdrant is running — WAL corruption risk.
(crontab -l 2>/dev/null; echo "0 2 * * * curl -sf -X POST http://127.0.0.1:6333/collections/fsm_corpus/snapshots > /dev/null && cd /path/to/gusengine && docker compose stop gusengine && tar czf \$HOME/gusengine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=storage/models --exclude=storage/qdrant storage/ config/ && docker compose start gusengine") | crontab -
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
