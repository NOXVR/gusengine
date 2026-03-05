# V10 FIX LIST — TRIAD CONVERGENCE

**Date:** 2026-02-24
**Source Audits:** Deep Think (DT), Gemini Deep Research (DR), Claude Opus (OP)
**Target:** `ARCHITECTURE_V10.md` (1,123 lines)
**Purpose:** Exhaustive remediation schedule. Every validated finding from all three auditors, organized by severity, with exact line references and replacement text.

> [!CAUTION]
> **DO NOT** apply these fixes piecemeal. Line numbers will shift after each edit. Apply in the order listed (top-down by line number within each severity tier), or apply all simultaneously.

---

## STATS

| Metric | Count |
|:-------|:-----:|
| 💀 CRITICAL fixes | 7 |
| ⚠️ SIGNIFICANT fixes | 9 |
| 🔍 MINOR fixes | 9 |
| **Total** | **25** |
| False positives rejected | 3 (DR-1, DR-4, DR-7) |

---

## 💀 CRITICAL FIXES

These are crash-on-boot, security breach, or broken-pipeline issues. The system will not function correctly without every one of these resolved.

---

### FIX-01: Docker network `internal` contradiction
**Source:** OP-1, OP-3
**Lines:** L136, L287
**Problem:** The CAUTION box at L136 claims `internal: true` for the Docker network. The actual YAML at L287 says `internal: false`. These are mutually exclusive. If L287 is authoritative, the air-gap claim is false. If L136 is the intent, the YAML is misconfigured.

Additionally, `internal: false` allows Docker containers to make outbound internet connections. Docker's iptables rules bypass UFW by default, so the comment "firewall handles external" is misleading. A compromised vLLM or TEI container could phone home.

**Resolution:** Set `internal: true`. Published ports with `127.0.0.1` binding still function because Docker uses iptables DNAT for published ports, which operates independently of the bridge network's internal flag. Inter-container communication uses Docker DNS on the bridge network, which also functions with `internal: true`.

**Fix at L136:**
```diff
- The Docker network is `internal: true` for the inference subnet.
+ The Docker network is `internal: true` — containers cannot initiate outbound internet connections. Published ports bound to `127.0.0.1` still accept host connections via iptables DNAT.
```

**Fix at L287:**
```diff
-    internal: false  # Needs host access for localhost binding; firewall handles external
+    internal: true   # Air-gap: blocks container egress. 127.0.0.1 port bindings still work via iptables DNAT.
```

---

### FIX-02: Embedding generation code entirely missing
**Source:** OP-2, OP-6
**Lines:** After L507 (Embedding & Indexing section), before L515
**Problem:** `index_chunk()` accepts `dense_vector` and `sparse_vector` as parameters. `hybrid_search()` accepts `query_dense` and `query_sparse`. But **no code anywhere in V10 shows how TEI is called** to produce these vectors — neither at ingestion time nor at query time. The HTTP calls to TEI's `/embed` and `/embed_sparse` endpoints are absent. This is a broken pipeline: chunks are parsed but never embedded, queries are searched but never vectorized. Compare to L700-753 which DOES show the full HTTP call to vLLM.

This also addresses OP-6 (TEI sparse vector support unverified) — the new code explicitly documents the TEI endpoint and includes a validation step.

**Fix:** Insert new section after L507 (`index_chunk` code block closing), before L510 ("### Ingestion Time Estimate"):

```python
# backend/embedding/client.py
import httpx
from typing import Optional

TEI_BASE_URL = "http://tei:80"

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
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
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
        except (httpx.HTTPStatusError, KeyError):
            # TEI version may not support sparse; log warning and degrade to dense-only
            import logging
            logging.warning("TEI /embed_sparse failed — falling back to dense-only search")
        
        return dense_vector, sparse_vector
```

Additionally, add a new subsection "### Ingestion Orchestration" showing how `parse_and_chunk()`, `embed_text()`, and `index_chunk()` connect:

```python
# backend/ingestion/pipeline.py
from backend.ingestion.parser import parse_and_chunk
from backend.embedding.client import embed_text
from backend.indexing.qdrant_setup import index_chunk
from qdrant_client import QdrantClient

async def ingest_pdf(pdf_path: str, client: QdrantClient, start_id: int = 0):
    """Full ingestion pipeline: parse → embed → index."""
    chunks = parse_and_chunk(pdf_path)
    
    for i, chunk in enumerate(chunks):
        dense, sparse = await embed_text(chunk["text"])
        
        sparse_dict = sparse or {"indices": [], "values": []}
        
        index_chunk(
            client=client,
            chunk=chunk,
            chunk_id=start_id + i,
            dense_vector=dense,
            sparse_vector=sparse_dict,
        )
    
    return len(chunks)
```

And show query-time embedding in the retrieval section (insert before the `hybrid_search` call site, or add a note):

```python
# In backend/routes/chat.py (query-time embedding):
query_dense, query_sparse = await embed_text(user_query)
results = hybrid_search(client, query_dense, query_sparse)
```

---

### FIX-03: Missing model volume mount in `gusengine` container
**Source:** DT-1
**Lines:** L236-239
**Problem:** The FastAPI backend loads `AutoTokenizer.from_pretrained("/app/models/Qwen2.5-32B-Instruct-AWQ")` at L354-357, L604-607, and L890-893. But the `gusengine` container's volume mounts at L236-239 do NOT include `./storage/models:/app/models:ro`. The tokenizer load will crash with `FileNotFoundError` on every code path that counts tokens.

**Fix at L236-239:**
```diff
     volumes:
       - ./storage/pdfs:/app/pdfs:ro
       - ./storage/extracted:/app/extracted
       - ./config:/app/config:ro
+      - ./storage/models:/app/models:ro
```

---

### FIX-04: EasyOCR runtime model download violates air-gap
**Source:** DT-2
**Lines:** L363-366
**Problem:** EasyOCR downloads ~200 MB of model weights (detection + recognition) on first call to `Reader(['en'])`. In an air-gapped environment, this will fail silently or crash. The models must be pre-downloaded and the download path configured.

**Fix:** Add EasyOCR model pre-download to the Model Pre-Download Commands section (after L307), and configure the model path in the Docling configuration.

**Insert after L307** (after BGE-M3 download, before PDF.js download):
```bash
# Pre-download EasyOCR models for air-gapped OCR
pip install easyocr
python3 -c "import easyocr; easyocr.Reader(['en'], gpu=False, download_enabled=True)"
# Models download to ~/.EasyOCR/model/ — copy to persistent storage:
mkdir -p ./storage/models/easyocr
cp -r ~/.EasyOCR/model/* ./storage/models/easyocr/
```

**Add to gusengine Docker volume mounts (L236-239), alongside FIX-03:**
```yaml
      - ./storage/models/easyocr:/root/.EasyOCR/model:ro
```

**Add environment variable to gusengine service (L240-248), after existing env vars:**
```yaml
      - EASYOCR_MODULE_PATH=/root/.EasyOCR
```

**Update EasyOcrOptions at L363-366:**
```diff
         ocr_options=EasyOcrOptions(
             lang=["en"],
             use_gpu=False,  # OCR on CPU to preserve GPU VRAM for LLM
+            download_enabled=False,  # CRITICAL: air-gap — models pre-loaded
         ),
```

---

### FIX-05: `validate_ledger.py` uses container paths but runs on host
**Source:** DT-3
**Lines:** L886-918
**Problem:** `validate_ledger.py` references `/app/models/Qwen2.5-32B-Instruct-AWQ` (container path) but is designed to be run by operators on the host for ledger validation before deployment. The path doesn't exist on the host.

**Fix at L890-893:**
```diff
- TOKENIZER = AutoTokenizer.from_pretrained(
-     "/app/models/Qwen2.5-32B-Instruct-AWQ",
-     trust_remote_code=True
- )
+ import os
+ 
+ # Support both host and container execution:
+ # - Container: /app/models/Qwen2.5-32B-Instruct-AWQ (via volume mount)
+ # - Host:      ./storage/models/Qwen2.5-32B-Instruct-AWQ (relative to project root)
+ MODEL_PATH = os.environ.get(
+     "TOKENIZER_MODEL_PATH",
+     "/app/models/Qwen2.5-32B-Instruct-AWQ"
+ )
+ 
+ TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
```

Add usage note in the section header or as a comment:
```
# Host usage: TOKENIZER_MODEL_PATH=./storage/models/Qwen2.5-32B-Instruct-AWQ python3 validate_ledger.py MASTER_LEDGER.md
# Container usage: python3 validate_ledger.py /app/config/MASTER_LEDGER.md (uses default path)
```

---

### FIX-06: Frontend container missing Nginx config volume mount
**Source:** DT-4
**Lines:** L261-282
**Problem:** The frontend container at L271-273 mounts PDFs and TLS certs but does NOT mount the Nginx configuration file. The container will use the default Nginx config, which won't proxy `/api/*` to the backend, won't serve PDFs from the correct path, and won't enforce upload blocking rules. The frontend will be a static React app with no API connectivity.

**Fix at L271-273:**
```diff
     volumes:
       - ./storage/pdfs:/usr/share/nginx/pdfs:ro
       - ./certs:/etc/nginx/ssl:ro
+      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
```

---

### FIX-07: Upload blocking regex targets dead AnythingLLM endpoint
**Source:** OP-5
**Lines:** L955-956
**Problem:** V10 preserves V9's Nginx rule blocking `/api/v1/document/(upload|create-folder)`. But V10 replaced AnythingLLM with custom FastAPI — this endpoint no longer exists. The actual ingestion endpoint is `/api/ingest` (L65). An attacker on the network could inject arbitrary PDFs into the vector store via `/api/ingest` because Nginx doesn't block it.

**Fix at L956:**
```diff
- 6. **Upload Blocking** — Case-insensitive regex blocks `/api/v1/document/(upload|create-folder)`
+ 6. **Upload Blocking** — Case-insensitive regex blocks:
+    - `/api/v1/document/(upload|create-folder)` (legacy V9, retained for defense-in-depth)
+    - `/api/ingest` (V10 FastAPI ingestion endpoint — EXTERNAL access blocked, only localhost/VMDK daemon may call)
```

Add corresponding Nginx location block to the security section or reference the `nginx.conf` from FIX-06:
```nginx
# In config/nginx.conf:
location ~* ^/api/ingest {
    # Block external ingestion — only localhost (VMDK daemon) may trigger
    allow 127.0.0.1;
    deny all;
}
```

---

## ⚠️ SIGNIFICANT FIXES

These are correctness, data integrity, or hardening issues. The system may partially function without them but will produce incorrect results or have exploitable gaps.

---

### FIX-08: RRF 40% threshold is mathematically incoherent
**Source:** DT-5, DR-2 (3/3 convergence — OP noted it as marginal)
**Lines:** L536, L574-578
**Problem:** RRF scores are computed as `1 / (k + rank)` where k=60 (Qdrant default). All scores fall in the range `[1/80, 1/61]` ≈ `[0.0125, 0.0164]`. The spread between best and worst is only 0.0039. A 40% threshold means `0.0164 * 0.4 = 0.00656`, which is below ALL possible RRF scores — the threshold will never filter anything. It's a no-op.

**Fix at L536:**
```diff
-    score_threshold_pct: float = 0.40,
+    min_score_ratio: float = 0.70,
```

**Fix at L544:**
```diff
-        score_threshold_pct: Dynamic threshold as % of top score
+        min_score_ratio: Keep chunks scoring >= this fraction of top RRF score (0.70 = within 30% of best)
```

**Fix at L574-578:**
```diff
-    # Dynamic threshold: keep chunks scoring >= 40% of top score
-    # AUDIT FIX (R2): Static thresholds fail across score distributions.
-    # Dynamic threshold adapts to query-specific score ranges.
-    top_score = results.points[0].score
-    threshold = top_score * score_threshold_pct
+    # Dynamic threshold: keep chunks within 30% of top RRF score
+    # NOTE (Triad Audit): RRF scores cluster tightly in [1/(k+N), 1/(k+1)].
+    # With k=60 and top_k=20, scores range [0.0125, 0.0164].
+    # A ratio threshold of 0.70 keeps scores >= 0.0115, filtering only
+    # chunks that appeared in only one signal with very low rank.
+    # For more aggressive filtering, raise to 0.85 or add a rank-based cutoff.
+    top_score = results.points[0].score
+    threshold = top_score * min_score_ratio
```

---

### FIX-09: Live Qdrant backup via tar = corruption risk
**Source:** DT-6
**Lines:** L982-988
**Problem:** The cron job stops only `gusengine` but Qdrant remains running. Tarring `./storage/qdrant/` while Qdrant writes to its WAL can produce a corrupt backup. Qdrant has a native snapshot API specifically designed for consistent backups (already shown at L969-980).

**Fix at L982-988:**
```diff
  ### Volume Backup (V9 Heritage, Adapted)
  
  ```bash
- # V10: Backup all persistent volumes
- # Stops only the backend to prevent torn writes; vLLM and Qdrant can hot-snapshot
- (crontab -l 2>/dev/null; echo "0 2 * * * cd /path/to/gusengine && docker compose stop gusengine ; tar czf \$HOME/gusengine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=storage/models storage/ config/ ; docker compose start gusengine") | crontab -
+ # V10: Backup strategy — Qdrant via native snapshots, everything else via tar
+ # Step 1: Qdrant snapshot (consistent, no downtime required)
+ # Step 2: Stop backend, tar config + PDFs + extracted cache, restart
+ # Step 3: Cleanup old backups
+ (crontab -l 2>/dev/null; echo "0 2 * * * curl -sf -X POST http://127.0.0.1:6333/collections/fsm_corpus/snapshots > /dev/null && cd /path/to/gusengine && docker compose stop gusengine && tar czf \$HOME/gusengine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=storage/models --exclude=storage/qdrant storage/ config/ && docker compose start gusengine") | crontab -
  (crontab -l 2>/dev/null; echo "0 3 * * * find \$HOME/ -name 'gusengine_backup_*.tar.gz' -mtime +7 -exec rm {} \\;") | crontab -
  ```
+ 
+ > [!IMPORTANT]
+ > **Qdrant backup is handled via its native snapshot API** (see above), NOT via tar. The tar backup explicitly excludes `storage/qdrant/` to prevent WAL corruption. Restore procedure: (1) restore tar backup, (2) restore Qdrant snapshot via the recovery endpoint.
```

---

### FIX-10: VMDK daemon "PRESERVED UNCHANGED" contradiction
**Source:** DT-7
**Lines:** L426-436
**Problem:** L426 says the daemon is "PRESERVED UNCHANGED" but L429 says `chunk_pdf()` is "NO LONGER CALLED" and L435 adds a webhook trigger to `/api/ingest`. These are functional changes. The contradiction is confusing for implementers.

**Fix at L426-427:**
```diff
- > The `vmdk_extractor.py` daemon from V9 Phase 4 is **PRESERVED UNCHANGED** for extracting PDFs from VMDK/OVA files. The only modification is the output destination: extracted PDFs are placed in `./storage/pdfs/` instead of `~/diagnostic_engine/extracted_manuals/`. The daemon's `wait_for_stable()` TOCTOU locking, three-tier quarantine defense, and manifest-based deduplication remain exactly as documented in V9 (49 verified audit findings).
+ > The `vmdk_extractor.py` daemon from V9 Phase 4 is **PRESERVED WITH TARGETED MODIFICATIONS** for extracting PDFs from VMDK/OVA files. Core logic is unchanged: `wait_for_stable()` TOCTOU locking, three-tier quarantine defense, and manifest-based deduplication remain exactly as documented in V9 (49 verified audit findings). Three changes:
+ > 1. **Output path:** `./storage/pdfs/` replaces `~/diagnostic_engine/extracted_manuals/`
+ > 2. **`chunk_pdf()` removed:** Docling handles all chunking (see Ingestion Pipeline)
+ > 3. **Webhook added:** After dedup, triggers `POST /api/ingest` on localhost:8888
```

---

### FIX-11: Ledger token cap contradictory across three locations
**Source:** DT-8, OP-4 (2/3 convergence)
**Lines:** L248, L672, L878, L896
**Problem:** Four locations give conflicting ledger budget values:
- Docker env var (L248): `LEDGER_MAX_TOKENS=2000`
- Token budget diagram (L672): `~2,000 tokens`
- Tribal Knowledge table (L878): `3,000 (adjusted: 2,550)`
- `validate_ledger.py` (L896): `RAW_CAP = 3000`

If the validator allows 2,550 tokens but the budget only reserves 2,000, the ledger can overflow its allocation by 550 tokens, silently shrinking the RAG budget.

**Resolution:** The RAW_CAP=3000 with SAFETY_FACTOR=0.85 → adjusted 2,550 is the correct validator behavior. The env var and budget diagram should match the adjusted cap.

**Fix at L248:**
```diff
-      - LEDGER_MAX_TOKENS=2000
+      - LEDGER_MAX_TOKENS=2550
```

**Fix at L672:**
```diff
- │ Pinned Ledger (MASTER_LEDGER.md)   ~2,000 tokens│
+ │ Pinned Ledger (MASTER_LEDGER.md)   ~2,550 tokens│
```

**Fix at L675 (recalculate RAG budget):**
```diff
- │ RAG Context Budget                ~26,868 tokens│
+ │ RAG Context Budget                ~26,318 tokens│
```

**Fix at L631 (update comment to match):**
```diff
-    # available ≈ 32768 - 900 - 2000 - 2000 - 0 = 27,868 tokens for RAG
-    # This is ~17× the V9 budget of 1,600 tokens
+    # available ≈ 32768 - 900 - 2550 - 2000 - 0 = 27,318 tokens for RAG
+    # With chat history (~1000): 26,318 tokens ≈ 16.4× the V9 budget
```

**Fix at L904 (update inline math):**
```diff
-     remaining = 32768 - 900 - count - 2000  # total - prompt - ledger - response
+     remaining = 32768 - 900 - count - 2000  # total - prompt - ledger - response (count <= 2550)
```

---

### FIX-12: IDF double-weighting on BGE-M3 sparse vectors
**Source:** DR-3
**Lines:** L478-481
**Problem:** BGE-M3's sparse output is a SPLADE-like learned lexical representation — the model has already learned optimal term weights during training. Setting `modifier=Modifier.IDF` in Qdrant applies BM25-style IDF reweighting ON TOP of the learned weights, double-weighting rare terms. This distorts the search ranking.

**Note:** OP-117 explicitly disagreed ("correct for BM25-like behavior"). However, DR's argument is structurally sound: BGE-M3's sparse vectors are NOT raw term frequencies — they are learned contextual weights. Applying IDF on top is like applying IDF to an already-weighted TF-IDF vector.

**Fix at L478-481:**
```diff
         sparse_vectors_config={
             "sparse": SparseVectorParams(
                 index=SparseIndexParams(on_disk=False),
-                modifier=Modifier.IDF,  # BM25-like IDF weighting
+                modifier=None,  # BGE-M3 sparse output is pre-weighted (SPLADE-like); no additional IDF needed
             )
         },
```

Remove `Modifier` from import at L463:
```diff
- from qdrant_client.models import (
-     VectorParams, SparseVectorParams, Distance,
-     SparseIndexParams, Modifier,
- )
+ from qdrant_client.models import (
+     VectorParams, SparseVectorParams, Distance,
+     SparseIndexParams,
+ )
```

---

### FIX-13: Air-gap violations via AutoTokenizer and Docling Hub calls
**Source:** DR-6, DT-2 (complementary vectors)
**Lines:** L240-248 (gusengine env vars), L350, L354-357, L602-607
**Problem:** `AutoTokenizer.from_pretrained()` with `trust_remote_code=True` attempts to reach huggingface.co to check for updates. In air-gap mode, this either fails (crash) or leaks DNS queries. Additionally, Docling's layout models may attempt downloads.

**Fix:** Add `HF_HUB_OFFLINE=1` to the gusengine container environment and add `local_files_only=True` to all `AutoTokenizer.from_pretrained()` calls.

**Fix at L240-248 (add env var):**
```diff
     environment:
       - VLLM_BASE_URL=http://vllm:8000/v1
       - TEI_BASE_URL=http://tei:80
       - QDRANT_URL=http://qdrant:6333
       - VLLM_MODEL=Qwen2.5-32B-Instruct-AWQ
       - MAX_CONTEXT_TOKENS=32768
       - SYSTEM_PROMPT_TOKENS=900
       - RESPONSE_BUDGET_TOKENS=2000
-      - LEDGER_MAX_TOKENS=2000
+      - LEDGER_MAX_TOKENS=2550
+      - HF_HUB_OFFLINE=1
+      - TRANSFORMERS_OFFLINE=1
```

**Fix at L354-357:**
```diff
  TOKENIZER = AutoTokenizer.from_pretrained(
      "/app/models/Qwen2.5-32B-Instruct-AWQ",
-     trust_remote_code=True
+     trust_remote_code=True,
+     local_files_only=True,
  )
```

**Fix at L604-607 (same pattern):**
```diff
  TOKENIZER = AutoTokenizer.from_pretrained(
      "/app/models/Qwen2.5-32B-Instruct-AWQ",
-     trust_remote_code=True
+     trust_remote_code=True,
+     local_files_only=True,
  )
```

**Fix at L890-893 (same pattern, plus FIX-05 path resolution):**
Already handled in FIX-05. Ensure `local_files_only=True` is added there as well.

---

### FIX-14: `parse_and_chunk()` has zero error handling
**Source:** OP-7
**Lines:** L376-421
**Problem:** No try/except around `converter.convert()` or the chunking loop. A corrupt PDF, an OCR crash, or an empty Docling result will throw an unhandled exception, crashing ingestion of that file and potentially the entire batch. V9's `process_file()` had three-tier quarantine defense (Audit Findings #24, #26, #27). V10's parser has none.

**Fix at L376-421:**
```diff
  def parse_and_chunk(pdf_path: str, max_tokens: int = 512) -> list[dict]:
      """Parse a PDF with Docling and chunk using HybridChunker.
      
      Returns list of chunks with metadata:
      - text: chunk text content
      - source: original filename
      - page_numbers: list of page numbers this chunk spans
      - headings: hierarchical heading path
      - token_count: exact token count via native tokenizer
+     
+     Raises:
+         IngestionError: If parsing fails after logging. Caller should
+         quarantine the file and continue with the next PDF.
      """
-     converter = create_converter()
-     result = converter.convert(pdf_path)
-     doc = result.document
+     import logging
+     logger = logging.getLogger(__name__)
+     
+     try:
+         converter = create_converter()
+         result = converter.convert(pdf_path)
+     except Exception as e:
+         logger.error(f"DOCLING PARSE FAILURE: {pdf_path} — {e}")
+         raise IngestionError(f"Failed to parse {pdf_path}: {e}") from e
+     
+     doc = result.document
+     if doc is None:
+         logger.error(f"DOCLING EMPTY RESULT: {pdf_path} — converter returned None document")
+         raise IngestionError(f"Docling returned empty document for {pdf_path}")
      
      chunker = HybridChunker(
          tokenizer=TOKENIZER,
          max_tokens=max_tokens,
          merge_peers=True,  # Merge adjacent same-level sections
      )
      
      chunks = []
-     for chunk in chunker.chunk(doc):
+     try:
+       chunk_iter = chunker.chunk(doc)
+     except Exception as e:
+         logger.error(f"CHUNKER FAILURE: {pdf_path} — {e}")
+         raise IngestionError(f"Chunking failed for {pdf_path}: {e}") from e
+     
+     for chunk in chunk_iter:
          text = chunk.text
+         if not text or not text.strip():
+             continue  # Skip empty chunks (OCR failures on blank pages)
          token_count = len(TOKENIZER.encode(text))
```

Also add the custom exception class at top of file (after imports):
```python
class IngestionError(Exception):
    """Raised when a PDF fails to parse or chunk. Caller should quarantine."""
    pass
```

---

### FIX-15: Multiple system messages may misbehave with Qwen2.5
**Source:** OP-8
**Lines:** L723-732
**Problem:** Context is injected as a second `{"role": "system", ...}` message. Qwen2.5's chat template uses `<|im_start|>system\n...<|im_end|>` blocks. Multiple system blocks may produce unexpected tokenization or template behavior depending on the vLLM version's chat template handling. The safer pattern is to append context to the single system message.

**Fix at L723-732:**
```diff
     messages = [
-        {"role": "system", "content": system_prompt},
+        {"role": "system", "content": system_prompt + (
+            f"\n\nRETRIEVED DOCUMENTS:\n\n{context}" if context else ""
+        )},
     ]
     
-    # Inject context as a system-level document block
-    if context:
-        messages.append({
-            "role": "system",
-            "content": f"RETRIEVED DOCUMENTS:\n\n{context}"
-        })
-    
     # Add chat history
     messages.extend(chat_history)
```

---

### FIX-16: `awq_marlin` quantization kernels for vLLM performance
**Source:** DR-5
**Lines:** L164-172
**Problem:** vLLM's default AWQ kernels use GEMM. The Marlin kernels (`awq_marlin`) provide 2-3x throughput improvement for batched inference. This requires `--dtype float16` to be explicit.

**Fix at L164-172:**
```diff
     command: >
       --model /models/Qwen2.5-32B-Instruct-AWQ
-      --quantization awq
+      --quantization awq_marlin
+      --dtype float16
       --tensor-parallel-size 2
       --max-model-len 32768
       --gpu-memory-utilization 0.85
       --port 8000
       --trust-remote-code
       --disable-log-requests
```

---

## 🔍 MINOR FIXES

These are code hygiene, documentation accuracy, or low-risk hardening issues. None will cause crashes, but they improve correctness and maintainability.

---

### FIX-17: `table_structure_options` passed as dict instead of Pydantic model
**Source:** OP-9
**Lines:** L368
**Problem:** `table_structure_options={"mode": TableFormerMode.ACCURATE}` — Docling's `PdfPipelineOptions` expects a `TableStructureOptions` Pydantic model. While Pydantic may coerce the dict, this is fragile and version-dependent.

**Fix at L344-348 (imports):**
```diff
  from docling.datamodel.pipeline_options import (
      PdfPipelineOptions,
      EasyOcrOptions,
      TableFormerMode,
+     TableStructureOptions,
  )
```

**Fix at L368:**
```diff
-        table_structure_options={"mode": TableFormerMode.ACCURATE},
+        table_structure_options=TableStructureOptions(mode=TableFormerMode.ACCURATE),
```

---

### FIX-18: Citation `page` field type changed string→int without noting schema break
**Source:** OP-10
**Lines:** L810, L847, L852
**Problem:** V9 example: `"page": "N/A"` (string). V10 example: `"page": 3` (integer). V10 L834 claims frontend functions are "PRESERVED UNCHANGED". But `renderCitation()` at L852 already checks `citation.page !== "N/A"` — if page is now an integer, this check still works in JavaScript (loose equality), but it's confusing and could break in strict comparisons.

**Fix at L810:**
```diff
-     {"source": "07.4.1-411 Checkup of Electronically Controlled Gasoline Injection System.pdf", "page": 3, "context": "K-Jetronic warm control pressure check — Section 2.1 Fuel System Diagnostics"}
+     {"source": "07.4.1-411 Checkup of Electronically Controlled Gasoline Injection System.pdf", "page": "3", "context": "K-Jetronic warm control pressure check — Section 2.1 Fuel System Diagnostics"}
```

Or, if integer is preferred, add a note at L834:
```diff
- The following V9 functions are **PRESERVED UNCHANGED** in the React frontend:
+ The following V9 functions are **PRESERVED UNCHANGED** in the React frontend (with one schema adaptation: the `page` field in `source_citations` is now an integer instead of string. `renderCitation()` handles both types via loose comparison):
```

---

### FIX-19: Missing `import os` in `parser.py`
**Source:** OP-12
**Lines:** L342-350, L414
**Problem:** `os.path.basename(pdf_path)` is called at L414 but `import os` is not in the imports block.

**Fix at L350:**
```diff
  from transformers import AutoTokenizer
+ import os
```

---

### FIX-20: Unused imports in `search.py`
**Source:** OP-11
**Lines:** L526-529
**Problem:** `SearchRequest`, `NamedVector`, `NamedSparseVector`, and `Query` are imported but never used.

**Fix at L526-529:**
```diff
  from qdrant_client.models import (
-     SearchRequest, NamedVector, NamedSparseVector,
      SparseVector, FusionQuery, Fusion, Prefetch, Query,
  )
+ # Note: Query is used by FusionQuery internally; retain if needed by IDE type-checkers
```

Actually, `Query` isn't used either. Clean import:
```diff
- from qdrant_client.models import (
-     SearchRequest, NamedVector, NamedSparseVector,
-     SparseVector, FusionQuery, Fusion, Prefetch, Query,
- )
+ from qdrant_client.models import (
+     SparseVector, FusionQuery, Fusion, Prefetch,
+ )
```

---

### FIX-21: PDF.js downloaded from unofficial GitHub fork
**Source:** OP-13
**Lines:** L312
**Problem:** URL points to `github.com/nicbarker/pdfjs-dist` — not Mozilla's official release. This fork may be outdated, unmaintained, or compromised.

**Fix at L312-314:**
```diff
- curl -L https://github.com/nicbarker/pdfjs-dist/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip \
-   -o /tmp/pdfjs.zip
- unzip /tmp/pdfjs.zip -d ./frontend/public/pdfjs/
+ # Option A: npm (preferred, verifiable via npm registry checksums)
+ cd ./frontend && npm pack pdfjs-dist@4.0.379 && tar xzf pdfjs-dist-4.0.379.tgz && mv package/build/* public/pdfjs/ && rm -rf package pdfjs-dist-4.0.379.tgz && cd ..
+ 
+ # Option B: Official Mozilla release
+ curl -L https://github.com/nicbarker/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip \
+   -o /tmp/pdfjs.zip
+ # TODO: Replace with official mozilla/pdf.js release URL when verified
+ unzip /tmp/pdfjs.zip -d ./frontend/public/pdfjs/
```

> [!NOTE]
> Verify the correct official URL at build time. The npm method is more auditable.

---

### FIX-22: Code comment "27,868" contradicts budget diagram "26,868"
**Source:** OP-14
**Lines:** L631
**Problem:** The code comment calculates with `chat_history_tokens=0` (the default), giving 27,868. The budget diagram at L672-679 includes 1,000 tokens for chat history, giving 26,868. The comment is technically correct for the default but misleading.

**Resolution:** Already handled by FIX-11, which updates the comment to reflect the corrected ledger cap of 2,550. The new comment explicitly notes the chat history deduction.

---

### FIX-23: CPU OCR time estimate may be 2-6× too optimistic
**Source:** OP-15
**Lines:** L513
**Problem:** EasyOCR on CPU for degraded 1960s-era scans could be 1-3 minutes per page, yielding 40-120 hours for 2,442 pages. The current estimate says "8-20 hours."

**Fix at L513:**
```diff
- > **Gemini DT and Gemini DR both flag this:** Docling with OCR on 250K+ pages will take significant time. Estimated 2-5 pages/minute with OCR enabled on CPU = 833-2083 hours for 250K pages. **For prototype with 514 PDFs (~2,442 pages), estimated time is 8-20 hours.** This is a one-time cost. Pre-compute and cache Docling output in `./storage/extracted/`.
+ > **Gemini DT and Gemini DR both flag this:** Docling with OCR on 250K+ pages will take significant time. Estimated 2-5 pages/minute with OCR enabled on CPU for clean documents. **For prototype with 514 PDFs (~2,442 pages) of degraded 1960s-era scans, estimated time is 20-60 hours** (1-3 minutes/page with EasyOCR on CPU for faded/handwritten content). This is a one-time cost. Pre-compute and cache Docling output in `./storage/extracted/`.
```

---

### FIX-24: Missing `PYTORCH_CUDA_ALLOC_CONF` for VRAM stability
**Source:** DR-8
**Lines:** L155-156 (vLLM environment)
**Problem:** At high context lengths (32K), CUDA memory fragmentation can cause OOM errors even with available VRAM. `expandable_segments:True` mitigates this.

**Fix at L155-156:**
```diff
     environment:
       - NVIDIA_VISIBLE_DEVICES=all
+      - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

---

### FIX-25: DOMPurify claim contradicts "PRESERVED UNCHANGED" renderGusResponse
**Source:** DT-9
**Lines:** L830-831, L834
**Problem:** L830 says DOMPurify XSS defense is "addressed" and L831 implies it's added. But L834 says `renderGusResponse()` is "PRESERVED UNCHANGED" from V9. If V9 didn't use DOMPurify and V10 does, then `renderGusResponse()` is NOT unchanged. If V9 already used DOMPurify, then L831's wording is confusing.

**Fix at L830-831:**
```diff
- 4. **DOMPurify** — All LLM-controlled strings sanitized before innerHTML (V9 XSS warning addressed)
+ 4. **DOMPurify** — All LLM-controlled strings MUST be sanitized before innerHTML. V9 warned about this risk (V9 FROZEN L1549); V10 mandates DOMPurify integration in `renderGusResponse()` as a **V10 ADDITION** (the V9 function logic is otherwise unchanged).
```

**Fix at L834:**
```diff
- The following V9 functions are **PRESERVED UNCHANGED** in the React frontend:
+ The following V9 functions are **PRESERVED** in the React frontend (core logic unchanged; DOMPurify sanitization added as V10 hardening):
```

---

## REJECTED FINDINGS (FALSE POSITIVES)

These findings from the audits were investigated and determined to be incorrect. Documented here for audit trail completeness.

| ID | Auditor | Claim | Why Rejected |
|:---|:--------|:------|:-------------|
| DR-1 | Gemini DR | Invalid `do_ocr=True` API usage | V10 L361-368 already uses correct `PdfPipelineOptions(do_ocr=True)` → `PdfFormatOption` hierarchy. The code is correct. |
| DR-4 | Gemini DR | Page number extraction uses flat `chunk.meta.page_no` | V10 L402-406 already uses correct nested traversal: `item.prov[0].page_no for item in chunk.meta.doc_items`. DR's own "fix" is identical to existing code. |
| DR-7 | Gemini DR | Log rotation values need string quotes | V10 L177-179 already uses quotes: `"50m"` and `"3"`. Auditor likely read an older version or hallucinated. |

---

## APPLICATION ORDER

For manual application, process fixes top-to-bottom within each severity tier. Recommended batch order:

**Batch 1 — Critical (must-fix before any testing):**
FIX-01 through FIX-07

**Batch 2 — Significant (must-fix before deployment):**
FIX-08 through FIX-16

**Batch 3 — Minor (should-fix for production quality):**
FIX-17 through FIX-25

---

**END OF V10_FIX_LIST.md**
