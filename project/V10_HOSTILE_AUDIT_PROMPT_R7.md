# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 7

## YOUR ROLE

You are a hostile production auditor performing **Phase 7** of a multi-pass audit. Phase 1 found 20 isolated execution bugs. Phase 2 found 15 cross-component interaction bugs. Phase 3 found 17 edge-case defects. Phase 4 found 15 fix interaction defects. Phase 5 found 16 convergence defects across two independent auditors. Phase 6 found 12 fixes across two independent auditors — including budget desync overflow, TEI token limit ordering, exception handler mismatch, dense-only ratio over-filtering, thread-safe tokenizer wrapper, null byte injection, and httpx timeout reduction. All **95 findings** have been patched.

**Your job is NOT to re-audit those 95 fixes.** Your job is to:

1. **Hunt for systemic design flaws** — After 6 rounds, the incremental bugs are drying up. What remains are architectural assumptions that no single-fix patch can address. Identify places where the design itself — not the implementation — creates fragility. Look for implicit contracts between components that are never enforced.
2. **Stress-test the Phase 6 corrections** — Phase 6 made three structural changes: (a) the query length cap was moved above the TEI embed call and reduced from 10000→8000, (b) the dynamic score ratio was disabled in dense-only mode, and (c) validate_ledger.py's exception handler was widened. Each change alters the behavior envelope. Find where downstream code assumed the old behavior.
3. **Probe operational failure modes** — This system runs on a single Lambda Labs A6000 box with 48GB VRAM and 128GB RAM. The architecture specifies 4 Docker containers (vLLM, TEI, Qdrant, FastAPI). Identify scenarios where container orchestration, resource exhaustion, or cascading restart behavior creates failure modes that the architecture doesn't address.

Phase 1 found the obvious. Phase 2 found the interactions. Phase 3 found the edge cases. Phase 4 found fix conflicts. Phase 5 found convergence failures. Phase 6 found specification/runtime divergence. **You are looking for: what systemic assumptions does this architecture make that break under real operational conditions?**

---

## CUMULATIVE FIX CHANGELOG (DO NOT RE-AUDIT)

All findings below have been patched. Use this list to understand what changed, then look for **new failure modes in the fully-patched system**.

### Phase 1 — Isolated Execution Bugs (20 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| H01 | Comment label correction | "Default" → "Typical (with ledger)" |
| H02 | GPU memory utilization | `0.85` → `0.75` |
| H03 | Docker healthchecks | Added `healthcheck` + `condition: service_healthy` |
| H04 | Chat handler defined | Full `chat()` function added |
| H05 | Absolute RRF threshold | Added `min_absolute_score` parameter |
| H06 | Async index_chunk | Wrapped in `asyncio.to_thread()` |
| H07 | Dynamic header tokens | TOKENIZER computation replaces hardcoded `+20` |
| H08 | DOMPurify implementation | `renderGusResponse()` with sanitization |
| H09 | Embed error handling | try/except → PHASE_ERROR JSON |
| H10 | Search error handling | try/except → PHASE_ERROR JSON |
| H11 | RAG budget floor | `MIN_RAG_FLOOR=5000` |
| H12 | Chat history cap | `MAX_CHAT_HISTORY_TOKENS=8000` |
| H13 | LLM error handling | try/except → PHASE_ERROR JSON |
| DT2 | Served model name | `--served-model-name Qwen2.5-32B-Instruct-AWQ` |
| DT3 | UUID chunk IDs | Deterministic UUID5 replaces sequential IDs |
| DT5 | Background ingestion | BackgroundTasks + HTTP 202 + empty chunk guard |
| DT7 | Docling wrapper | `HuggingFaceTokenizer` wraps raw AutoTokenizer |
| DT8 | Sparse prefetch omission | Conditional omission when sparse unavailable |
| DT10 | Citation page integer | "cite ONLY the first page as an integer" |
| — | GPU util progression | `0.85` → `0.80` → `0.75` |

### Phase 2 — Interaction Bugs + Fix Regressions (15 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P2-01 | User query token budget | `user_query_tokens` deducted in `build_context()` |
| P2-02 | Physical chat history eviction | Oldest-first eviction loop in `chat()` handler |
| P2-03 | TOKENIZER import | Imported from backend module in `chat.py` |
| P2-04 | Shared qdrant_client | New `backend/shared/clients.py` singleton module |
| P2-05 | RETRIEVAL_FAILURE trigger | `RETRIEVED DOCUMENTS` header always present |
| P2-06 | Background error wrapper | `ingest_pdf_background()` with error logging + failure manifest |
| P2-07 | Logger in search.py | `import logging` + `logger` added |
| P2-08 | UUID format fix | `.hex` → `str()` + type hint `int` → `str` |
| P2-09 | renderGusResponse complete | Added PHASE_D, RETRIEVAL_FAILURE, PHASE_ERROR, textInputEl toggle |
| P2-10 | PHASE_ERROR schema | Added `requires_input`, `answer_path_prompts`, `source_citations`, `intersecting_subsystems` |
| P2-11 | Path traversal prevention | `os.path.realpath()` + `ALLOWED_PDF_DIR` + `.pdf` extension check |
| P2-12 | System prompt error handling | `os.path.exists()` check → `SystemExit` on missing file |
| P2-13 | GPU util table sync | Config table updated `0.85` → `0.75` |
| P2-14 | RRF floor calibration | `min_absolute_score` raised from `0.005` to `0.013` |
| DT-P2-04 | Ingestion semaphore | `INGEST_SEMAPHORE = asyncio.Semaphore(2)` gates `parse_and_chunk` |

### Phase 3 — Edge Cases + Fix-on-Fix Defects (17 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P3-01 | Tuple destructuring | `context, used_chunks = build_context(...)` — was receiving raw tuple |
| P3-02 | Eviction keeps ≥1 message | Added `and truncated` guard so eviction never empties history |
| P3-03 | Collection auto-creation | `@app.on_event("startup")` → `ensure_qdrant_collection()` idempotent |
| P3-04 | Embed semaphore | `EMBED_SEMAPHORE = asyncio.Semaphore(8)` rate-limits TEI requests |
| P3-05 | Persistent httpx client | Module-level `_http_client` singleton replaces per-call instantiation |
| P3-06 | Logger in context_builder | `import logging` + `logger` added to `context_builder.py` |
| P3-07 | Empty RETRIEVED DOCUMENTS | Placeholder `[No documents retrieved]` removed — section left empty |
| P3-08 | Async hybrid_search | Wrapped in `asyncio.to_thread()` to avoid blocking event loop |
| P3-09 | Error manifest completeness | Unexpected errors also written to `.ingest_failures.log` |
| P3-11 | DAG recovery rules | PHASE_ERROR → last valid phase; RETRIEVAL_FAILURE → PHASE_A_TRIAGE |
| P3-12 | Server-side JSON validation | `json.loads(response)` check → PHASE_ERROR if LLM returns non-JSON |
| P3-13 | Shared tokenizer module | `backend/shared/tokenizer.py` — single instance for parser + context builder |
| DT-P3-03 | User query length cap | `MAX_USER_QUERY_TOKENS=10000` → **reduced to 8000 by DT-P6-02** |
| DT-P3-04 | Path traversal trailing slash | `startswith(ALLOWED_PDF_DIR + "/")` — prevents sibling dir bypass |
| DT-P3-06 | DOMPurify import | Uncommented import + `npm install dompurify` in air-gap prep |
| DT-P3-07 | Eviction role validator | Post-truncation strip of leading assistant message |
| P3-10 | Text input toggle | Cleared by auditor — no fix needed |

### Phase 4 — Fix Interaction Defects (15 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P4-01 | Missing `import asyncio` | Added to `chat.py` — was required by P3-08's `asyncio.to_thread()` |
| P4-02 | Post-eviction content truncation | ~~Oversized single message → `TOKENIZER.decode(tokens[:8000])`~~ **REMOVED by DT-P5-07** |
| P4-03 | Eviction strip guard | ~~DT-P3-07 strip only if `len(truncated) > 1`~~ **REMOVED by DT-P5-07** |
| P4-04 | textContent for plaintext | `mechanic_instructions`/`diagnostic_reasoning` → `.textContent` (preserves `<B+>`) |
| P4-05 | Chat embed semaphore | `embed_text()` in chat wrapped in `EMBED_SEMAPHORE` |
| P4-06 | Persistent LLM httpx | `_get_llm_client()` singleton replaces per-call `httpx.AsyncClient` |
| P4-07 | Startup retry loop | 10-attempt exponential backoff (P5-08 extension) in `ensure_qdrant_collection()` + `SystemExit` on fail |
| P4-08 | Per-chunk error handling | try/except per chunk in ingestion — skip on failure, don't abort PDF |
| P4-09 | Validator shared tokenizer | `validate_ledger.py` imports from shared module with host fallback |
| P4-10 | JSON schema validation | `current_state` field required after `json.loads()` |
| P4-11 | Tokenizer pre-check | `os.path.isdir()` + ~~`SystemExit`~~ **`RuntimeError` (DT-P5-06)** with clear message |
| DT-P4-02 | Conditional fusion query | Single-prefetch → direct query; dual-prefetch → `FusionQuery(RRF)` |
| DT-P4-04 | ~~Basename path extraction~~ | ~~`os.path.basename()`~~ **Replaced by relative path extraction (DT-P5-05)** |
| DT-P4-05 | ~~Eviction skip oversized~~ | ~~`break` → `continue`~~ **REVERTED to `break` by DT-P5-01** |
| DT-P4-06 | Markdown fence stripping | Strip `` ```json `` wrappers before `json.loads()` + schema check |

### Phase 5 — Convergence Defects (16 fixes across two independent auditors)

#### Opus Phase 5 (11 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P5-01 | Indexed count tracking | `indexed_count`/`failed_count` replace `len(chunks)` — no silent partial ingestion |
| P5-02 | ~~Non-contiguous eviction detection~~ | ~~Gap and same-role detection~~ **SUPERSEDED by DT-P5-01 (break revert)** |
| P5-03 | Secondary brace extraction | JSON fallback: `{` to `}` extraction if fence-strip fails |
| P5-04 | Mode-adaptive score floor | RRF: `0.013` / Dense-only: `0.35` → **raised to `0.50` by P6-04** |
| P5-05 | httpx pool management | `Limits(max_connections=100, max_keepalive=20)` + `close_embed_client()` + shutdown handler |
| P5-06 | ~~Truncation marker~~ | ~~`[MESSAGE TRUNCATED]` appended~~ **REMOVED by DT-P5-07 (orphan stripped instead)** |
| P5-07 | Frontend parse comment | Skipped — no target code in arch doc |
| P5-08 | Startup retry extension | 5→10 attempts, backoff capped 60s. Max wait ~303s (~5 min) |
| P5-09 | DOMPurify removal from textContent | Removed `DOMPurify.sanitize()` from `.textContent` — was stripping `<B+>`/`<GND>` |
| P5-10 | Failure manifest path fix | `/app/storage/extracted/` → `/app/extracted/` via `FAILURE_MANIFEST_PATH` constant |
| P5-11 | Separator token accounting | `\n\n---\n\n` cost budgeted per chunk boundary in context loop |

#### Deep Think Phase 5 (5 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| DT-P5-01 | Eviction `continue` → `break` **REVERT** | Contiguous eviction — prevents role alternation crash (HTTP 400). Removes P5-02 detection code. |
| DT-P5-04 | Zero-success IngestionError | `raise IngestionError(...)` when `indexed_count == 0` — no silent total failure |
| DT-P5-05 | Relative path extraction | `raw_path.split("pdfs/", 1)[-1]` replaces `os.path.basename()` — preserves subdirectories |
| DT-P5-06 | `SystemExit` → `RuntimeError` | Tokenizer pre-check now catchable by `except (ImportError, RuntimeError)` in host validator |
| DT-P5-07 | Orphan assistant strip (always) | Removed P4-03 `len>1` guard + P4-02 content truncation. Empty history > poisoned history. |

### Phase 6 — Specification/Runtime Divergence (12 fixes across two independent auditors)

#### Opus Phase 6 (9 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P6-01 | **Budget desync guard (CRITICAL)** | Post-eviction hard enforcement: if `chat_history_tokens > MAX_CHAT_HISTORY_TOKENS` → PHASE_ERROR. Prevents oversized single message from reaching vLLM. |
| P6-02 | `if` → `while` orphan strip | Handles consecutive leading assistant messages (malformed frontend payload). |
| P6-03 | Double-write manifest guard | Partial failure block gated with `and indexed_count > 0` — no double-write when all chunks fail. |
| P6-04 | Dense-only score floor | `0.35` → `0.50` — above BGE-M3's random-pair cosine noise band (0.25–0.45). |
| P6-05 | Dedicated search thread pool | `_SEARCH_POOL = ThreadPoolExecutor(max_workers=4)` — chat search no longer starved by ingestion. |
| P6-06 | Thread-safe tokenizer wrapper | `threading.Lock` + `count_tokens()` function serializes `TOKENIZER.encode()` calls. |
| P6-07 | Null byte path guard | `if "\x00" in raw_path:` → reject before `os.path.realpath()` raises `ValueError`. |
| P6-08 | httpx timeout reduction | `30s` → `10s` (connect: `5s`) — fail-fast on stale keep-alive after TEI restart. |
| P6-09 | Empty chat history comment | Documented that empty `chat_history` after orphan strip produces valid ChatML. |

#### Deep Think Phase 6 (3 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| DT-P6-02 | **Query cap moved above embed** | `user_query_tokens` validation moved BEFORE TEI embed call. Cap reduced `10000` → `8000` to align with TEI's 8192-token hardware limit. Prevents TEI crash before validator fires. |
| DT-P6-03 | **validate_ledger exception fix (CRITICAL)** | `except ImportError:` → `except (ImportError, RuntimeError):` — DT-P5-06's `RuntimeError` was not caught, crashing host-side validator. |
| DT-P6-05 | Dense-only ratio disabled | `effective_ratio = min_score_ratio if len(prefetch_list) >= 2 else 0.0` — prevents cosine-space over-filtering. Absolute floor (P6-04: 0.50) and top_k handle filtering instead. |

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## AUDIT DIMENSIONS (PHASE 7 — SYSTEMIC DESIGN ANALYSIS)

### Dimension 1: TOKEN BUDGET INTEGRITY — FULL-PATH VERIFICATION

The token budget is the single most critical invariant: every prompt sent to vLLM MUST fit within `--max-model-len 32768`. After 95 fixes, the budget math now involves 6 independent deductions. Verify the worst-case arithmetic end-to-end:

1. **Budget proof for maximum legal inputs:** Compute the absolute maximum prompt size using the worst values that pass ALL guards:
   - System prompt: ~900 tokens (fixed, loaded from file)
   - Ledger: ADJUSTED_CAP = 2550 tokens (validated by `validate_ledger.py`)
   - Chat history: 8000 tokens MAX (enforced by P6-01 guard)
   - User query: 8000 tokens MAX (enforced by DT-P6-02 guard, reduced from 10000)
   - Response buffer: 2000 tokens (from `max_tokens` parameter)
   - RAG context: `32768 - 900 - 2550 - 8000 - 8000 - 2000 = 11,318` tokens available

   **But the P6-01 guard only fires AFTER eviction.** If a single user message is exactly 8000 tokens, it passes both DT-P6-02 (`≤ 8000`) and P6-01 (`8000 ≤ 8000`). With a maxed-out ledger (2550) and maxed query (8000): available = `32768 - 900 - 2550 - 8000 - 8000 - 2000 = 11,318`. This is above MIN_RAG_FLOOR (5000). **Is this actually correct? Does `generate_response()` really only use `available` tokens of context, or does it send ALL `used_chunks` regardless of budget?**

2. **Double deduction audit:** `user_query_tokens` is computed at the DT-P6-02 guard (before embed). It is then passed to `build_context()` which deducts it. But the user query is ALSO part of the messages sent to `generate_response()` as `user_message=user_query`. **Is the user query's token cost deducted twice — once in `build_context()` and once implicitly in the messages array?** If `build_context()` already accounts for it, the actual prompt is: `system + context + chat_history + user_message = 900 + (available - user_query_tokens) + chat_history_tokens + user_query_tokens`. The user_query_tokens cancel out. Verify this is actually correct algebra, or whether the cancellation produces 11,318 + 8,000 = 19,318 tokens of context.

3. **MIN_RAG_FLOOR override risk:** When `available < MIN_RAG_FLOOR (5000)`, the floor is hardcoded to 5000. This adds tokens beyond what the arithmetic allows. If `available` computes to -500 (theoretically prevented by guards), the floor makes it 5000. **Does the combination of P6-01 guard + DT-P6-02 guard mathematically guarantee `available ≥ 0`?** Show the proof, or show the counterexample.

### Dimension 2: CONCURRENCY & RESOURCE EXHAUSTION

The system runs on a single server with finite resources. The architecture specifies concurrency controls (`INGEST_SEMAPHORE=2`, `EMBED_SEMAPHORE=8`, `_SEARCH_POOL=4`) but these operate independently. Probe their interaction:

1. **Semaphore starvation cascade:** During bulk ingestion, `INGEST_SEMAPHORE(2)` allows 2 PDFs to parse concurrently. Each enters the embed loop which acquires `EMBED_SEMAPHORE(8)`. A chat request also acquires `EMBED_SEMAPHORE` (P4-05). With 2 PDFs × 200 chunks each, the embed semaphore is held for the duration of each `embed_text()` call. **Can a situation arise where all 8 embed permits are held by ingestion chunks, and the chat embed request waits indefinitely?** The `httpx.Timeout(10.0)` should cause embed to fail and release, but **does the semaphore release on exception?** `async with EMBED_SEMAPHORE` does guarantee release — verify this for the ingestion path too.

2. **Thread pool exhaustion:** `_SEARCH_POOL` has 4 workers. `asyncio.to_thread()` uses the default pool (varies by implementation, typically `min(32, os.cpu_count() + 4)`). During concurrent chat and ingestion: chat search uses `_SEARCH_POOL` (4 threads), index_chunk uses default pool via `asyncio.to_thread()`. **If 20 concurrent ingestion chunks hit `asyncio.to_thread(index_chunk, ...)` simultaneously, do they queue behind the default pool limit?** Is the default pool size explicitly set anywhere, or is it implementation-dependent?

3. **VRAM pressure during concurrent operations:** vLLM uses `--gpu-memory-utilization 0.75` (36GB of 48GB). TEI-GPU uses the remaining ~12GB. **What happens when vLLM serves a long-context inference (32K tokens) while TEI processes 8 concurrent embed requests?** Do they share CUDA memory space? If vLLM's KV cache expands dynamically, can it push TEI into GPU OOM?

4. **Qdrant concurrent read/write:** During bulk ingestion, `index_chunk()` upserts while `hybrid_search()` queries. Qdrant uses MVCC with segments. **Can a query return stale results for a document that is mid-upsert?** The UUID5 IDs are deterministic per chunk — if a chunk is being re-embedded (re-ingestion), does the query see the old or new vector?

### Dimension 3: FAILURE RECOVERY & CASCADE BEHAVIOR

The architecture has error handling at every layer, but error handling assumes independent failures. Probe cascading failures:

1. **TEI container death spiral:** TEI has a 30s start_period and restarts via Docker. If TEI crashes during bulk ingestion: (a) In-flight `embed_text()` calls get `httpx.ConnectError`, handled by P4-08. (b) Chat `embed_text()` gets "search system unavailable" PHASE_ERROR. (c) TEI restarts. But during restart, `_http_client` (P3-05) still holds stale TCP connections from the dead container. **Does `httpx.Timeout(10.0, connect=5.0)` (P6-08) detect a stale connection, or does it hang for 10s per request until pool connections expire?** With 8 concurrent embed requests on stale connections, that's 8 × 10s = 80s of wasted time before connections cycle.

2. **Qdrant persistence restart:** Qdrant stores data to disk. If Qdrant restarts during ingestion: (a) `ensure_qdrant_collection()` ran at startup — does it run again on Qdrant restart? (b) In-flight `index_chunk()` calls fail. (c) P4-08 logs and skips affected chunks. (d) **But the `_SEARCH_POOL` threads may hold references to the synchronous Qdrant client.** Does `QdrantClient` reconnect automatically, or do all search requests fail until the FastAPI container restarts?

3. **vLLM OOM recovery:** If vLLM processes a 32K-token request and OOM-kills, Docker restarts it. The healthcheck (`curl /health`) waits 120s start_period. During this window: (a) `generate_response()` gets `httpx.ConnectError` → PHASE_ERROR. (b) `_get_llm_client()` returns a client with stale connections. **Same stale-connection problem as TEI.** But vLLM's start_period is 120s — that's 120s of "AI engine unavailable" errors. Is there a retry mechanism in `generate_response()`, or does every request during the restart window fail immediately?

4. **Full system cold start ordering:** On a clean boot, Docker Compose starts all 4 services. `depends_on: service_healthy` ensures vLLM/TEI/Qdrant are healthy before FastAPI starts. **But what if FastAPI starts, Qdrant becomes healthy, then Qdrant crashes and restarts AFTER FastAPI's startup hook ran?** The `ensure_qdrant_collection()` ran once. It doesn't run again. If Qdrant loses its in-memory state on restart but persists to disk, the collection exists. But if Qdrant's volume mount is ephemeral (`/tmp/qdrant_storage` in some configs), the collection is gone and all queries return 404.

### Dimension 4: IMPLICIT CONTRACT VIOLATIONS

After 95 fixes, the system has accumulated implicit contracts between components that are never enforced by code. Identify contracts that exist only in comments or by convention:

1. **`count_tokens()` vs raw `TOKENIZER.encode()`:** P6-06 added a thread-safe `count_tokens()` wrapper with `_TOKENIZER_LOCK`. But the chat handler, eviction loop, and build_context all use `len(TOKENIZER.encode(...))` directly. **Is `count_tokens()` actually called anywhere, or was it defined but never wired in?** If the raw `TOKENIZER.encode()` is still used everywhere, the threading lock provides zero protection.

2. **`MAX_USER_QUERY_TOKENS` vs `MAX_CHAT_HISTORY_TOKENS` independence:** Both are set to 8000. But they're defined as local constants in different scopes — `MAX_USER_QUERY_TOKENS` inside the chat handler, `MAX_CHAT_HISTORY_TOKENS` also inside the chat handler. If someone changes one but not the other, the budget math breaks silently. **Should these be module-level constants, or imported from a shared config?**

3. **Qdrant collection name hardcoding:** The string `"fsm_corpus"` appears in at least 4 locations: `create_collection()`, `hybrid_search()`, `index_chunk()`, and `ensure_qdrant_collection()`. If any one is changed without updating the others, operations silently target a non-existent collection. **Is there a shared constant for this?**

4. **vLLM model name contract:** `--served-model-name Qwen2.5-32B-Instruct-AWQ` (Docker) must match `"model": "Qwen2.5-32B-Instruct-AWQ"` (generate_response). Both are hardcoded strings in different files. **What happens if the operator upgrades to a new model and only updates one location?**

### Dimension 5: CONVERGENCE HEALTH ASSESSMENT

After 6 phases, 95 fixes, and 5 structural reversals, assess the architecture's convergence trajectory:

1. **Fix generation rate by phase:** P1:20 → P2:15 → P3:17 → P4:15 → P5:16 → P6:12. The rate is declining but NOT converging to zero. **At what phase will the diminishing returns make further auditing counterproductive?** Is 7 that phase?

2. **Fix interaction depth:** Count how many fixes reference other fixes. P6-01 references P3-02. DT-P6-02 references DT-P3-03. P6-03 references DT-P5-04. **If the average fix now references 2+ prior fixes, the system is entering a complexity regime where further patches risk regression more than they reduce risk.** Quantify the reference depth.

3. **Component stability ranking:** Rank the top-5 most-modified components by fix count. If chat history eviction has received 10+ modifications, it is the weakest structural element. **Should the next step be a redesign (extract eviction to its own module with unit tests) rather than a 7th audit?**

4. **Forensic validation result:** A full diff between the original V10 and the current document (858 insertions, 120 deletions) was classified line-by-line. All changes are accounted for. **Does this give you confidence that the document is internally consistent, or does the sheer volume of changes (978 net modified lines) introduce cognitive complexity that makes the document itself a source of bugs?**

### Dimension 6: OPERATIONAL OBSERVABILITY GAPS

The system has logging but no structured observability. Identify what the operator CANNOT know:

1. **Ingestion progress visibility:** The operator triggers 500 PDF ingestions via the V9 daemon. Each returns HTTP 202 immediately. How does the operator know when ingestion is complete? The only signal is log lines saying "Background ingestion complete." **Is there an endpoint or mechanism to query ingestion status?** If not, the operator is flying blind.

2. **Token budget utilization metrics:** The system enforces budgets but doesn't report them. After a chat response, can the operator see: how many tokens were used by chat history, ledger, context, user query, and response? **Without this, budget-related issues (e.g., context too small because ledger is maxed) are invisible.**

3. **Search quality feedback loop:** The system filters chunks by score, but there's no logging of HOW MANY chunks were filtered, what scores they had, or whether the user's query was related to the filtered content. **If the score floor (P6-04: 0.50) is too aggressive, relevant chunks are silently discarded and the operator has no way to know.**

4. **Health check granularity:** Docker healthchecks check if services respond to `/health`. **But they don't check functional health.** vLLM's `/health` can return 200 while the model is in a degraded state (e.g., KV cache exhausted, inference queue full). TEI's `/health` can return 200 while the model weights are corrupted. **Are the healthchecks sufficient for production reliability?**

---

## SCENARIO TRACES (Phase 7 — Systemic Failure Chains)

**Scenario AC: Maximum Legal Prompt Size**
```
System prompt: 900 tokens
Ledger: 2550 tokens (at ADJUSTED_CAP)
Chat history: exactly 8000 tokens (single huge user message, passes P6-01)
User query: exactly 8000 tokens (passes DT-P6-02 at boundary)
```
Budget: `32768 - 900 - 2550 - 8000 - 8000 - 2000 = 11,318` tokens for RAG.
build_context() allocates 11,318 tokens of chunks. generate_response() assembles: system(900) + context(11,318) + chat_history(8000) + user_message(8000) = **28,218 tokens + 2000 response = 30,218**. This fits within 32,768.
**But wait:** is `user_query_tokens` double-counted? build_context deducts it from available, but user_message is ALSO in the final prompt. If user_query_tokens is deducted from the RAG budget but the query is sent separately, the actual RAG budget should be `available` without the deduction. Trace the exact data flow.

**Scenario AD: TEI Death During Chat + Ingestion**
```
State: 2 PDFs ingesting (INGEST_SEMAPHORE full), embed loop running.
Event: TEI container OOM-killed.
```
1. Ingestion embed_text() calls: 8 concurrent fail with ConnectError. P4-08 skips those chunks.
2. Chat embed_text() call: fails → "search system unavailable" PHASE_ERROR.
3. TEI restarts (Docker healthcheck detects failure after 15s interval × 3 retries = 45s minimum).
4. During 45s+ restart window: `_http_client` has stale connections. P6-08 timeout is 10s.
5. Each embed request hangs for 10s before failing. With EMBED_SEMAPHORE=8, the first 8 requests each hang 10s, then the next 8, etc.
6. **If 200 chunks are queued: 200/8 = 25 rounds × 10s = 250s of wasted time** before TEI comes back.
7. After TEI restart: does `_http_client` automatically reconnect, or do stale connections persist?

**Scenario AE: Qdrant Restart During Re-Ingestion**
```
State: Operator re-ingests a PDF to fill 10-chunk gap from a previous TEI failure.
The same UUID5 IDs are generated (deterministic).
Chunk 5 of 200 is being upserted when Qdrant restarts.
```
1. `index_chunk()` fails for chunk 5 → P4-08 skips it.
2. Qdrant restarts. Chunks 1-4 were already persisted to WAL. Are they durable?
3. Chunks 6-200: Qdrant client reconnects? Or does every remaining call fail?
4. If `QdrantClient` auto-reconnects: chunks 6-200 succeed. Only chunk 5 is missing.
5. If `QdrantClient` does NOT auto-reconnect: chunks 6-200 ALL fail → `indexed_count = 4` → partial manifest entry. The operator now has a DIFFERENT gap than before.

**Scenario AF: count_tokens() Wrapper Not Wired**
```
P6-06 defined count_tokens() with _TOKENIZER_LOCK.
Chat handler uses: len(TOKENIZER.encode(user_query)) — no lock.
Eviction loop: len(TOKENIZER.encode(m["content"])) — no lock.
build_context(): len(TOKENIZER.encode(...)) — no lock.
```
1. Chat request arrives. `asyncio.to_thread(hybrid_search, ...)` runs in `_SEARCH_POOL`.
2. Simultaneously, ingestion's `asyncio.to_thread(parse_and_chunk, ...)` runs in default pool.
3. `parse_and_chunk()` calls `TOKENIZER.encode()` (via HuggingFaceTokenizer wrapper in Docling).
4. Chat handler calls `TOKENIZER.encode(user_query)` on the main event loop thread.
5. **Two threads call TOKENIZER.encode() simultaneously. Neither acquires _TOKENIZER_LOCK.**
6. If Qwen2.5's custom tokenizer code has mutable state, corruption is possible.
7. **Is count_tokens() actually used by any call site, or is it dead code?**

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P7-XX: [Title]
- **Dimension:** [1-6]
- **Severity:** CRITICAL / SIGNIFICANT / MINOR
- **Classification:** [ADDITIVE] / [CORRECTIVE] / [SUBTRACTIVE]
- **Description:** What is wrong and why it matters.
- **Proof:** Trace the exact execution path, showing the failure with concrete data.
- **Fix:** Exact code change required.
```

## VERDICTS

After completing all dimensions and scenarios, provide:

1. **PASS / CONDITIONAL / BLOCKED** verdict
2. For CONDITIONAL: list exact fixes required
3. **Confidence score** (0-100%) for each dimension
4. **Residual risk** — what truly cannot be verified from the document alone

## INTEGRITY CHECKLIST

Before submitting, confirm:
- [ ] No finding overlaps with the 95 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace with specific data values
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] All scenario traces (AC through AF) complete with predicted outcomes
- [ ] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [ ] Budget math in Dimension 1 independently computed with ALL 6 deductions
- [ ] Convergence assessment in Dimension 5 includes quantitative fix-reference-depth analysis
- [ ] Dimension 4 verified: is count_tokens() dead code or wired in?
- [ ] Dimension 6 includes at least one concrete observability gap with operator impact
