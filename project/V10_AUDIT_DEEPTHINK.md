# V10 ARCHITECTURE AUDIT — TRIAD AUDITOR (GEMINI DEEP THINK)

## VRAM Verification

**Model Weights:** Qwen2.5-32B-Instruct-AWQ (4-bit). 32 billion parameters × 4 bits ÷ 8 bits/byte = 16 GB. With AWQ group indexing metadata overhead, ~18 GB is accurate.
**KV Cache:** 64 layers × 8 KV heads × 128 dim × 2 (K+V) × 2 bytes (FP16) × 32,768 tokens = 8,589,934,592 bytes = ~8 GB. V10's calculation is exact.
**Total Footprint:** 18 GB (Weights) + 8 GB (KV Cache) + 2 GB (vLLM) + 2 GB (BGE-M3) + 0.5 GB (TEI) = 30.5 GB.
**Headroom:** 48 GB (Dual RTX 4090) - 30.5 GB = 17.5 GB remaining.
VRAM VERIFIED.

## Findings Table

| # | Line(s) | Section | Severity | Finding | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | L146-152, L214 | Docker Compose / Ingestion | 💀 CRITICAL | Missing model volume mount in `gusengine` causes fatal boot crash. | The `gusengine` container mounts `pdfs`, `extracted`, and `config` (L149-151). However, `parser.py` (L214) and `context_builder.py` instantiate `AutoTokenizer.from_pretrained("/app/models/Qwen2.5-32B-Instruct-AWQ")`. The container has no access to this directory and will instantly throw `FileNotFoundError`. |
| 2 | L183-195, L226 | Ingestion Pipeline | 💀 CRITICAL | Docling/EasyOCR runtime model downloads violate air-gap. | V10 sets `do_ocr=True` (L226), which triggers EasyOCR. EasyOCR dynamically downloads PyTorch weights (`craft_mlt_25k.pth`, `english_g2.pth`) upon first execution. V10 omits these from the pre-download commands (L183). In an air-gapped environment, ingestion will timeout and crash. |
| 3 | L655, L689 | Tribal Knowledge | 💀 CRITICAL | `validate_ledger.py` execution on host OS guarantees crash. | V10 claims this subsystem is "architecturally identical to V9," which runs `validate_ledger.py` on the host filesystem via the host `venv`. But V10's script imports `transformers` (not in host venv) and hardcodes the Docker path `/app/models/...` (L655). The script will crash instantly. |
| 4 | L168-176, L716 | Docker Compose / Security | 💀 CRITICAL | `frontend` container is missing Nginx configuration. | V10 claims to preserve V9's security (TLS, upload blocking) via Nginx (L716). However, the `frontend` container mounts only `pdfs` and `certs` (L168-176). Without mounting `nginx.conf`, it serves the default Nginx page, failing to proxy `/api` and dropping all security rules. |
| 5 | L411-413 | Retrieval Pipeline | ⚠️ SIGNIFICANT | RRF dynamic percentage threshold is mathematically incoherent. | V10 calculates `threshold = top_score * 0.40`. As proven in Doc 6 (Gemini DT Audit), RRF produces normalized rank-fractions (`1/(rank+60)`). A 40% drop from rank 1 yields a score lower than `rank 80`. With `top_k=20`, this threshold filters absolutely nothing. |
| 6 | L766 | Disaster Recovery | ⚠️ SIGNIFICANT | Backing up live Qdrant database guarantees corruption. | The DR cron job stops `gusengine` but leaves `qdrant` running while `tar` archives the `./storage/` directory (which contains `./storage/qdrant`). Archiving a live vector database via file copy guarantees torn writes and corrupted snapshots. |
| 7 | L274-284 | Ingestion Pipeline | ⚠️ SIGNIFICANT | VMDK Daemon preservation contradiction. | V10 claims `vmdk_extractor.py` is "PRESERVED UNCHANGED" (L274), but then dictates its output destination changes, `chunk_pdf()` is "NO LONGER CALLED", and it triggers an `/api/ingest` webhook (L284). An unchanged V9 script will physically fragment PDFs and break Docling parsing. |
| 8 | L158, L660 | Tribal Knowledge | ⚠️ SIGNIFICANT | Ledger token budget mismatch risks context overflow. | Docker Compose sets `LEDGER_MAX_TOKENS=2000` (L158), which `build_context` uses for context math. However, `validate_ledger.py` allows the ledger to reach `ADJUSTED_CAP = 2550` (L660). A 2550-token ledger will overflow the strict 32,768 context limit by 550 tokens. |
| 9 | L556, L560 | Frontend Architecture | 🔍 MINOR | DOMPurify claim contradicts unchanged V9 heritage. | V10 claims LLM strings are sanitized with DOMPurify (L556), but explicitly lists `renderGusResponse()` as "PRESERVED UNCHANGED" (L560). V9's implementation uses raw `.innerHTML` directly. Both claims cannot be true simultaneously. |

## Heritage Verification

| V9 Component | Preserved in V10? | Accurate? | Notes |
| --- | --- | --- | --- |
| Gus DAG State Machine | ✅ | ✅ | Updated accurately for Qdrant metadata citation rules without contradicting V9 intent. |
| parseGusResponse() | ✅ | ✅ | V8 hardened forward-scanning brute-force iteration explicitly maintained. |
| buildUserMessage() | ✅ | ✅ | Preserved correctly with the `required_next_state: null` override logic for PHASE_B looping. |
| Security Measures | ✅ | ❌ | Fails. Nginx container lacks a config volume, silently dropping all V9 proxy rules, TLS setup, and upload blocks. |
| VMDK/OVA Daemon | ✅ | ❌ | Fails. Fatal contradiction claiming the script is "UNCHANGED" while mandating it no longer calls `chunk_pdf()` and triggers webhooks. |
| Tribal Knowledge | ✅ | ❌ | Fails. `validate_ledger.py` uses Docker-internal paths (`/app/models`) but executes natively on the host OS, guaranteeing a crash. |

## NotebookLM Parity Check

| NotebookLM Finding | V10 Implementation | Gap? |
| --- | --- | --- |
| Dual-track ingestion | Master PDFs preserved in `./storage/pdfs` for UI display; text extracted by Docling for LLM context. | No. Successfully separates visual repository from semantic search. |
| Structural chunking | Docling `HybridChunker` merges peers and splits strictly by document structure. | No. Replaces the blind 400-char splitting of V9. |
| Token-capped context | `build_context()` greedily appends sequentially ordered chunks until the 32K budget exhaustion. | No. Parity achieved. |
| Citation Architecture | System Prompt explicitly requires verbose JSON schema arrays containing `source`, `page`, and `context`. | **Yes.** V10 fails to adopt NotebookLM's plain `[N]` integer format (NotebookLM Finding 10), retaining V9's verbose JSON schema. |

## Audit Checklist Results

### A. Component Map
* [PASS] All 5 containers represented
* [PASS] Port assignments consistent between diagram and Docker Compose
* [FAIL] Volume mounts described match Docker Compose volumes (`gusengine` missing model mount)
* [FAIL] No external network dependencies at inference time (EasyOCR weights dynamically download)

### B. GPU Memory Budget
* [PASS] VRAM math independently verified
* [PASS] KV cache formula correct for Qwen2.5-32B architecture
* [PASS] Scale-up table realistic
* [PASS] No claim of 128K context on 48GB VRAM

### C. Docker Compose
* [PASS] All service definitions syntactically valid
* [PASS] GPU passthrough configured correctly
* [PASS] Localhost binding on all internal ports
* [PASS] Log rotation on all containers
* [FAIL] Environment variables consistent with code references (`LEDGER_MAX_TOKENS=2000` vs `2550`)
* [FAIL] Model paths in volume mounts match model download commands (`gusengine` missing mount)
* [PASS] `depends_on` ordering correct

### D. Ingestion Pipeline
* [PASS] Docling API usage correct
* [PASS] `do_ocr=True` explicitly set
* [PASS] HybridChunker usage correct
* [FAIL] AutoTokenizer usage correct (Lacks `local_files_only=True`, path issues on host)
* [PASS] Page number extraction from Docling metadata realistic
* [PASS] Ingestion time estimate for 514 PDFs (~2,442 pages) realistic

### E. Embedding & Indexing
* [PASS] BGE-M3 dimensions correct (1024 dense)
* [PASS] Qdrant collection schema valid (dense + sparse vectors)
* [PASS] Sparse vector configuration correct for BM25-like behavior
* [PASS] Index function correctly creates points with all required payload fields

### F. Retrieval Pipeline
* [PASS] Qdrant query API usage correct (Prefetch, FusionQuery, Fusion.RRF)
* [FAIL] Dynamic threshold calculation correct (Percentage on RRF score is mathematically flawed)
* [PASS] Greedy context builder correctly counts tokens
* [FAIL] Token budget math adds up (Ledger cap mismatch of 550 tokens)
* [PASS] Context formatting includes provenance headers

### G. Inference Layer
* [PASS] vLLM CLI flags correct and compatible with Qwen2.5-32B-AWQ
* [PASS] OpenAI-compatible API endpoint correct (`/v1/chat/completions`)
* [PASS] Temperature 0.1 appropriate for deterministic JSON output
* [PASS] Message assembly (system + context + history + user) correct

### H. System Prompt (Gus DAG V10)
* [PASS] DAG state machine preserved from V9
* [FAIL] Citation rules updated for Qdrant metadata (violates NotebookLM Parity check)
* [PASS] JSON output schema unchanged from V9
* [PASS] RETRIEVAL_FAILURE safeguard preserved
* [PASS] STATE TRANSITION ENFORCEMENT preserved
* [PASS] No contradictions between V10 system prompt and V9 system prompt

### I. Frontend Architecture
* [PASS] PDF.js self-hosted (no CDN dependency)
* [PASS] V9 CSS class contract preserved
* [PASS] `parseGusResponse()` and `buildUserMessage()` referenced correctly
* [FAIL] DOMPurify sanitization mentioned (Contradicts unchanged V9 `renderGusResponse`)

### J. Tribal Knowledge
* [PASS] Token budget updated for 32K context
* [FAIL] AutoTokenizer replaces tiktoken (Host script attempts to access container paths)
* [PASS] Ledger injection mechanism (FastAPI file read) described
* [FAIL] Archive lifecycle mentioned (Missing in V10 document entirely)

### K. Security
* [FAIL] All V9 security measures listed (Nginx proxy config completely absent)
* [FAIL] No new external API dependencies (EasyOCR violates air-gap)
* [FAIL] Air-gap verified across all components (Docling OCR dynamic downloads)

### L. Verification
* [FAIL] All 15 checklist items executable (Path errors and air-gap timeouts will crash)
* [PASS] Expected outputs realistic
* [PASS] GPU verification step included
* [PASS] Air-gap verification step included

### M. Known Boundaries
* [PASS] Honestly stated limitations
* [PASS] No overclaiming of capabilities
* [PASS] Upgrade path realistic

## Summary Statistics

| Metric | Count |
| --- | --- |
| 💀 CRITICAL findings | 4 |
| ⚠️ SIGNIFICANT findings | 4 |
| 🔍 MINOR findings | 1 |
| Total lines audited | 1,123 |
| Heritage items verified | 3/6 PASS |
| NotebookLM parity items | 3/4 PASS |

## Overall Verdict

**VERDICT: BLOCKED**

The V10 architecture successfully models the NotebookLM retrieval paradigm and correctly solves the 48GB VRAM constraint physics. However, it fails execution due to fatal container pathing errors in the validation scripts, missing volume mounts in the backend, dynamic weight-download air-gap violations, and severe security regressions where the missing Nginx configuration leaves the frontend broken and unsecured. Fix the infrastructure file paths and pre-download EasyOCR weights to achieve a deployable prototype.
