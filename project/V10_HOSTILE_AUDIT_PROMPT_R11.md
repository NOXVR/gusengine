# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 11

## YOUR ROLE

You are a hostile production auditor performing **Phase 11** of a multi-pass audit on a single-server RAG-based automotive diagnostic system. Your predecessors found **178 bugs** across 10 phases using 5 independent auditors. All 178 have been patched. The full patch history is in the changelog below.

**Your job is NOT to re-audit those 178 fixes.** Your job is to break this system.

Read the attached `ARCHITECTURE_V10.md` (2,342 lines) **in its entirety** — every code block, every comment, every diagram, every configuration value, every YAML block, every shell command, every inline formula. Find every remaining defect: bugs, logic errors, implicit assumptions, missing guards, algebraic mistakes, integration failures, race conditions, resource leaks, data corruption paths, deployment blockers, and semantic contradictions between code and comments.

This system diagnoses brake and fuel system failures for mechanics. Incorrect diagnostic advice is a **life-safety issue**. Audit accordingly.

**Do not be lazy. Do not stop at the first few findings. Do not limit yourself to what sounds interesting. Audit the ENTIRE document with the same intensity from line 1 to line 2,342. The last three phases found startup-crashing import regressions in lines 930-1935 that survived multiple prior reviews — the remaining bugs are hiding in plain sight.**

---

## WHAT 10 PRIOR PHASES FOUND (CONTEXT ONLY — DO NOT RE-AUDIT)

All 178 findings below have been patched. This changelog exists so you understand what changed and can look for **new failure modes in the fully-patched system**. If you find something that overlaps with any of these 178 items, discard it and move on.

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

### Phase 2 — Interaction Bugs (15 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P2-01 | User query budget | `user_query_tokens` deducted in `build_context()` |
| P2-02 | Physical eviction | Oldest-first eviction loop in `chat()` |
| P2-03 | TOKENIZER import | Imported from backend module in `chat.py` |
| P2-04 | Shared qdrant_client | `backend/shared/clients.py` singleton |
| P2-05 | RETRIEVAL_FAILURE trigger | `RETRIEVED DOCUMENTS` header always present |
| P2-06 | Background error wrapper | `ingest_pdf_background()` with error logging + manifest |
| P2-07 | Logger in search.py | `import logging` + `logger` added |
| P2-08 | UUID format fix | `.hex` → `str()` + type hint `int` → `str` |
| P2-09 | renderGusResponse complete | Added PHASE_D, RETRIEVAL_FAILURE, PHASE_ERROR, textInputEl toggle |
| P2-10 | PHASE_ERROR schema | Added `requires_input`, `answer_path_prompts`, `source_citations`, `intersecting_subsystems` |
| P2-11 | Path traversal prevention | `os.path.realpath()` + `ALLOWED_PDF_DIR` + `.pdf` check |
| P2-12 | System prompt error handling | `os.path.exists()` check → `SystemExit` on missing file |
| P2-13 | GPU util table sync | Config table updated `0.85` → `0.75` |
| P2-14 | RRF floor calibration | `min_absolute_score` raised from `0.005` to `0.013` |
| DT-P2-04 | Ingestion semaphore | `INGEST_SEMAPHORE = asyncio.Semaphore(2)` |

### Phase 3 — Edge Cases (17 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P3-01 | Tuple destructuring | `context, used_chunks = build_context(...)` |
| P3-02 | Eviction keeps ≥1 message | Added `and truncated` guard |
| P3-03 | Collection auto-creation | `ensure_qdrant_collection()` idempotent with retry |
| P3-04 | Embed semaphore | `EMBED_SEMAPHORE = asyncio.Semaphore(8)` |
| P3-05 | Persistent httpx client | Module-level `_http_client` singleton |
| P3-06 | Logger in context_builder | `import logging` + `logger` added |
| P3-07 | Empty RETRIEVED DOCUMENTS | Section left empty (no placeholder) |
| P3-08 | Async hybrid_search | Wrapped in `asyncio.to_thread()` |
| P3-09 | Error manifest completeness | Unexpected errors also written to manifest |
| P3-11 | DAG recovery rules | PHASE_ERROR → last valid; RETRIEVAL_FAILURE → PHASE_A |
| P3-12 | Server-side JSON validation | `json.loads(response)` check |
| P3-13 | Shared tokenizer module | `backend/shared/tokenizer.py` singleton |
| DT-P3-03 | User query cap | `MAX_USER_QUERY_TOKENS` → **reduced to 8000 by DT-P6-02** |
| DT-P3-04 | Path traversal trailing slash | `startswith(ALLOWED_PDF_DIR + "/")` |
| DT-P3-06 | DOMPurify import | Uncommented import + `npm install` |
| DT-P3-07 | Eviction role validator | Post-truncation strip of leading assistant |
| P3-10 | Text input toggle | Cleared — no fix needed |

### Phase 4 — Fix Interactions (15 fixes)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P4-01 | Missing `import asyncio` | Added to `chat.py` |
| P4-02 | Post-eviction truncation | **REMOVED by DT-P5-07** |
| P4-03 | Eviction strip guard | **REMOVED by DT-P5-07** |
| P4-04 | textContent for plaintext | Preserves `<B+>` tokens |
| P4-05 | Chat embed semaphore | `embed_text()` wrapped in `EMBED_SEMAPHORE` |
| P4-06 | Persistent LLM httpx | `_get_llm_client()` singleton |
| P4-07 | Startup retry loop | 10-attempt exponential backoff |
| P4-08 | Per-chunk error handling | try/except per chunk — skip on failure |
| P4-09 | Validator shared tokenizer | Host fallback for shared module |
| P4-10 | JSON schema validation | `current_state` field required |
| P4-11 | Tokenizer pre-check | `os.path.isdir()` + `RuntimeError` |
| DT-P4-02 | Conditional fusion query | Single-prefetch → direct; dual → FusionQuery(RRF) |
| DT-P4-04 | Path extraction | **Replaced by DT-P5-05** |
| DT-P4-05 | Eviction skip | **REVERTED to `break` by DT-P5-01** |
| DT-P4-06 | Markdown fence stripping | Strip ```json wrappers before parse |

### Phase 5 — Convergence Defects (16 fixes, 2 auditors)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P5-01 | Indexed count tracking | `indexed_count`/`failed_count` |
| P5-02 | Non-contiguous eviction | **SUPERSEDED by DT-P5-01** |
| P5-03 | Secondary brace extraction | `{` to `}` JSON fallback |
| P5-04 | Mode-adaptive score floor | RRF: 0.013 / Dense: **raised to 0.50 by P6-04** |
| P5-05 | httpx pool management | `Limits()` + `close_embed_client()` + shutdown |
| P5-06 | Truncation marker | **REMOVED by DT-P5-07** |
| P5-07 | Frontend parse comment | Skipped — no target |
| P5-08 | Startup retry extension | 10 attempts, 60s cap, ~303s total |
| P5-09 | DOMPurify on textContent | Removed — was stripping `<B+>` |
| P5-10 | Failure manifest path | `/app/storage/extracted/` → `/app/extracted/` |
| P5-11 | Separator token accounting | `\n\n---\n\n` cost budgeted per chunk |
| DT-P5-01 | Eviction `continue` → `break` REVERT | Contiguous eviction preserved |
| DT-P5-04 | Zero-success IngestionError | `raise IngestionError` when `indexed_count == 0` |
| DT-P5-05 | Relative path extraction | `split("pdfs/", 1)[-1]` preserves subdirs |
| DT-P5-06 | SystemExit → RuntimeError | Tokenizer pre-check now catchable |
| DT-P5-07 | Orphan strip (always) | P4-03 guard removed. Empty history > poisoned. |

### Phase 6 — Spec/Runtime Divergence (12 fixes, 2 auditors)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P6-01 | **Budget desync guard (CRITICAL)** | Post-eviction hard enforcement → PHASE_ERROR |
| P6-02 | `if` → `while` orphan strip | Handles consecutive leading assistants |
| P6-03 | Double-write manifest guard | `and indexed_count > 0` |
| P6-04 | Dense-only score floor | `0.35` → `0.50` |
| P6-05 | Dedicated search pool | `_SEARCH_POOL = ThreadPoolExecutor(4)` |
| P6-06 | Thread-safe tokenizer | `threading.Lock` + `count_tokens()` |
| P6-07 | Null byte path guard | Reject before `realpath()` |
| P6-08 | httpx timeout reduction | `30s` → `10s` |
| P6-09 | Empty chat history comment | Documented valid ChatML |
| DT-P6-02 | Query cap moved above embed | Prevents TEI crash. Cap: 8000. |
| DT-P6-03 | Validator exception fix | `except (ImportError, RuntimeError)` |
| DT-P6-05 | Dense-only ratio disabled | `effective_ratio = 0.0` for dense-only |

### Phase 7 — Systemic Design Flaws (18 fixes, 3 auditors)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P7-01 | **count_tokens() wiring (CRITICAL)** | All direct `TOKENIZER.encode()` replaced |
| P7-02 | FRAMEWORK_OVERHEAD | 100 → **250 → dynamic (P8-03)** |
| P7-03 | MIN_RAG_FLOOR rejection | Silent override → `ValueError` |
| P7-04 | Circuit breaker | 5 consecutive failures → abort |
| P7-05 | Embed semaphore timeout | 5s timeout prevents chat starvation |
| P7-07 | Pre-delete | **REMOVED by P7-14** |
| P7-08 | Model name from env | `os.environ.get("VLLM_MODEL", ...)` |
| GP7-05 | TEI pool flush | `_flush_embed_client()` on connection failure |
| GP7-10 | vLLM healthcheck | `/health` → `/v1/models` |
| GP7-11 | Search filter telemetry | `SEARCH FILTER SUPPRESSION` warning |
| P7-09 | **Missing `import os` (CRITICAL)** | `pipeline.py` — regression from P7-07 |
| P7-10 | Validator budget formula | Shows both scenarios |
| P7-11 | Runtime ledger cap | `LEDGER_MAX_TOKENS` truncation |
| P7-12 | LLM pool flush | `_flush_llm_client()` on failure |
| P7-13 | Embed flush lock | `asyncio.Lock` serializes flushes |
| P7-14 | Re-ingestion blackout fix | UUID5 upsert only. Ghost cleanup via `/api/cleanup`. |
| P7-15 | Chat history validation | Schema check + malformed entry drop |
| P7-17 | FRAMEWORK_OVERHEAD increase | 100 → 250 → **dynamic (P8-03)** |

### Phase 8 — Integration Correctness (17 fixes, 2 auditors)

#### Opus Phase 8 (12 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P8-01 | `import os` in `llm.py` | Regression — P7-08's `os.environ.get()` had no import |
| P8-02 | `import logging` + `logger` in `llm.py` | Regression — P7-12's `logger.warning()` had no logger |
| P8-03 | **Dynamic FRAMEWORK_OVERHEAD** | Static 250 → `(message_count + 2) × 5`. Message cap: `MAX_CHAT_HISTORY_MESSAGES=40`. |
| P8-04 | Ledger truncation re-count | `count_tokens()` after decode instead of hardcoding cap |
| P8-05 | LLM flush lock | `asyncio.Lock` + `_flush_llm_client()` |
| P8-06 | Shutdown lock | `close_embed_client()` acquires `_client_lock` |
| P8-07 | Empty content filter | `.strip()` check rejects whitespace-only messages |
| P8-08 | Budget diagram update | Reflects dynamic overhead + user query |
| P8-09 | System prompt verification | Startup check: actual tokens vs configured budget |
| P8-10 | PHASE_ERROR rendering | `gus-error` CSS class for visual feedback |
| P8-11 | Import path alignment | `backend.search` → `backend.retrieval.search` |
| P8-12 | Header token count | `"\n\n"` → `"\n"` to match actual f-string |

#### Deep Think Phase 8 (5 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| DT-P8-03 | `_TOKENIZER_LOCK` on ledger truncation | Raw `TOKENIZER.encode()`/`decode()` now wrapped in thread lock |
| DT-P8-04 | Absolute floor on all chunks | `point.score >= effective_min_absolute` added to per-chunk filter |
| DT-P8-05 | **`/api/cleanup` endpoint** | Ghost chunk deletion by source file via Qdrant payload filter. Life-safety fix. |
| DT-P8-06 | Sparse vector in ingestion | `index_chunk` omits `sparse` key when indices empty — prevents Qdrant HTTP 400 |
| DT-P8-07 | RRF ratio disabled | `effective_ratio = 0.0` for both modes — multiplicative ratio broke additive RRF scores |

### Phase 9 — Deployment & Runtime Hardening (17 fixes, 2 auditors)

#### Opus Phase 9 (12 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P9-01 | **Nginx deny `/api/cleanup` (CRITICAL)** | Added `location /api/cleanup { deny all; }` — unauthenticated remote vector DB wipe |
| P9-02 | **Budget env var wiring (CRITICAL)** | `MAX_CONTEXT_TOKENS`, `SYSTEM_PROMPT_TOKENS`, `RESPONSE_BUDGET_TOKENS` read from env + passed to `build_context()` |
| P9-03 | LLM client shutdown | `_flush_llm_client()` added to `cleanup_clients()` — prevents TCP socket leak |
| P9-04 | Async cleanup delete | Wrapped `qdrant_client.delete()` in `asyncio.to_thread()` in `/api/cleanup` |
| P9-05 | Budget diagram math | RAG context corrected: 24,218 → 26,218. Improvement ratio: 15.1× → 16.4× |
| P9-06 | gusengine Docker healthcheck | `curl -sf http://localhost:8888/api/health`. Frontend `depends_on: condition: service_healthy` |
| P9-07 | Pin Docker image tags | vLLM: `:latest` → `v0.7.2`. TEI: `:latest` → `1.5.0` |
| P9-08 | INJECTION_OVERHEAD | `INJECTION_OVERHEAD=15` deducted in `build_context()` for literal section-connecting strings |
| P9-09 | Search pool shutdown | `_SEARCH_POOL.shutdown(wait=False)` added to `cleanup_clients()` |
| P9-10 | Stale tokenizer comment | `len(TOKENIZER.encode(...))` → `count_tokens(...)` in ledger section comment |
| P9-11 | LockedTokenizer delegation | Added `decode()` with lock + `__getattr__` for forward compatibility |
| P9-12 | System prompt file handle | Bare `open().read()` → `with open() as f: f.read()` context manager |

#### Deep Think Phase 9 (5 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| DT-P9-01 | **Deferred asyncio.Lock() (CRITICAL)** | Module-level `asyncio.Lock()` crashes Python 3.10+ (no event loop at import). Deferred to lazy `_get_*_lock()` async getters. 3 call sites. |
| DT-P9-02 | **PointStruct validation (CRITICAL)** | `index_chunk` raw dict → `models.PointStruct()`. qdrant-client ≥1.7.0 Pydantic validation rejects dicts. |
| DT-P9-03 | **Source path collision (CRITICAL)** | `os.path.basename` → relative path. Prevents cross-directory cleanup destroying unrelated manuals with same filename. |
| DT-P9-04 | **Qdrant snapshots volume (CRITICAL)** | Added `./storage/snapshots:/qdrant/snapshots`. Without mount, `docker compose down` destroys all backup snapshots. |
| DT-P9-05 | Search saturation | `top_k=60` passed to `hybrid_search` (was default 20 — only ~10K tokens, starving the ~26K RAG budget by 50%+) |

### Phase 10 — Concurrency Hardening + Import Regressions (31 fixes, 3 auditors)

#### Opus Phase 10 (17 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P10-01 | Budget diagram + RAG budget | Corrected to ~26,203. Added INJECTION_OVERHEAD to diagram. |
| P10-02 | **`_get_client()` lock (CRITICAL)** | Wrapped in `_client_lock` — prevents use-after-close during concurrent embed/flush |
| P10-03 | **`_get_llm_client()` lock (CRITICAL)** | Wrapped in `_llm_client_lock` — same pattern |
| P10-04 | Thread-safe lock init (×2) | Double-checked locking via `threading.Lock()` for lazy `asyncio.Lock` init |
| P10-05 | Snapshot restore path | `/qdrant/storage/snapshots/` → `/qdrant/snapshots/` |
| P10-06 | HTTP→HTTPS redirect | Documented Nginx redirect requirement. Removed port 80 binding. |
| P10-07 | `__getattr__` lock | LockedTokenizer `__getattr__` acquires `_TOKENIZER_LOCK` |
| P10-09 | **Missing `import asyncio` (CRITICAL)** | `ingest.py` — regression from P9-04's `asyncio.to_thread()` |
| P10-10 | Consolidated import | `from qdrant_client import models` moved to top of `ingest.py` |
| P10-11 | Validator INJECTION_OVERHEAD | Added `INJECTION_OVERHEAD=15` to validator formula |
| P10-12 | Tribal knowledge table | RAG budget corrected to ~26,203 |
| P10-14 | max_tokens sync | `generate_response(max_tokens=_RESPONSE_BUDGET_TOKENS)` |
| P10-15 | Search default top_k | `hybrid_search` default `top_k` → 60 |
| P10-16 | Qdrant client separation | `qdrant_search_client` + `qdrant_ingest_client` for thread safety |
| P10-17 | TEI env var | `TEI_BASE_URL` reads from `os.environ.get()` |
| P10-18 | vLLM env var | `VLLM_BASE_URL` reads from `os.environ.get()` |
| P10-19 | Docker Compose version | Removed deprecated `version: "3.8"` |
| P10-20 | Thread-safe manifest | `_manifest_lock = threading.Lock()` for failure manifest writes |
| P10-21 | Stop sequence | `\n\n\n` → `\n\n\n\n\n` to prevent premature JSON truncation |

#### Deep Think Phase 10 (5 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| DT-P10-01 | **Deferred asyncio.Semaphore() (CRITICAL)** | Same crash as DT-P9-01. `INGEST_SEMAPHORE`/`EMBED_SEMAPHORE` deferred to lazy async getters. 3 caller sites updated. |
| DT-P10-03 | **Cleanup protocol (CRITICAL)** | BEFORE re-ingestion, not after. UUID5 means post-ingest cleanup deletes fresh chunks too. |
| DT-P10-04 | Orphan strip scope | Extracted from token eviction block to global scope. 41 short messages + count truncation skipped the strip. |
| DT-P10-05 | Tokenizer explicit wrappers | `tokenize()` and `__call__()` with `_TOKENIZER_LOCK` — strengthens P10-07 |
| DT-P10-06 | Lazy generator try/except | Chunk iteration moved inside `try/except` — `chunker.chunk()` returns lazy generator |

#### Third Auditor Phase 10 (9 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P10-22 | **Missing `import threading` (CRITICAL)** | `llm.py` — regression from P10-04's `threading.Lock()` |
| P10-23 | **Missing `import os` (CRITICAL)** | `client.py` — regression from P10-17's `os.environ.get()` |
| P10-24 | **Missing `import threading` (CRITICAL)** | `pipeline.py` — regression from P10-20's `threading.Lock()` |
| P10-25 | **Ingest client wiring (CRITICAL)** | `qdrant_ingest_client` wired into `ingest.py` — P10-16 separation was defeated (ingest client declared but never imported) |
| P10-26 | Manifest lock gap | `_manifest_lock` added to partial-failure path in `ingest_pdf()` |
| P10-27 | Budget comment | Corrected to include `user_query_tokens` (~50): 27,293 → 27,243 |
| P10-28 | Frontend healthcheck | Added Docker `healthcheck` to frontend (only service missing one) |
| P10-29 | Collection creation client | `ensure_qdrant_collection()` uses `qdrant_ingest_client` for writes |
| P10-30 | Qdrant shutdown | Both `qdrant_search_client` and `qdrant_ingest_client` closed in shutdown handler |

---

## KNOWN SYSTEMIC FAILURE PATTERNS

The following recurrent defect classes have been observed across 10 phases. Use them as **starting hypotheses**, not as the only vectors:

1. **Import regressions** (7 instances: P7-09, P8-01, P8-02, P10-09, P10-22, P10-23, P10-24) — every phase that adds `os.environ.get()`, `threading.Lock()`, or `asyncio.to_thread()` to a module forgets the corresponding `import`. Verify ALL import blocks against ALL symbols used in each code block.

2. **Declared-but-unwired fixes** (2 instances: P10-16/P10-25, DT-P10-01 callers) — a fix creates a new entity (client, getter, variable) but the callers are never updated to use it. Verify all recently created entities have at least one consumer.

3. **Asymmetric lock patterns** (3 instances: P10-02, P10-03, P10-26) — one code path acquires a lock but a parallel path doing the same operation does not. Look for `_manifest_lock`, `_client_lock`, `_llm_client_lock` usage and verify ALL paths that touch the guarded resource acquire the lock.

4. **Comment/code divergence** (4 instances: H01, P8-08, P9-05, P10-27) — comments state one budget value, code computes another. Verify every inline math comment against the code it describes.

5. **Module-scope asyncio objects** (2 instances: DT-P9-01, DT-P10-01) — `asyncio.Lock()` and `asyncio.Semaphore()` at module scope crash Python 3.10+. Verify no other `asyncio.*` constructors exist at module scope.

---

## PRESERVATION MANDATE

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## YOUR AUDIT MANDATE

Read the attached `ARCHITECTURE_V10.md` end-to-end. Find what is wrong.

You have no predefined targets. No areas of interest. No scaffolding. Ten prior phases found 178 defects across 5 independent auditors and every one has been patched. If defects remain, they are the kind that survive ten rounds of review — they hide in plain sight, in algebraic assumptions that almost work, in concurrency edges that only fire under specific ordering, in operational paths that the code handles but the deployment doesn't, in data flows where the producer and consumer disagree about format or semantics, in SDK version mismatches between what the code assumes and what the pinned image provides, in places where a fix to one module invalidated an assumption in another module that was never re-verified.

**Critical attention areas for Phase 11:**
- **Cross-module wiring**: Verify every `from X import Y` matches the actual symbol name at the source. Phase 10 exposed that `qdrant_ingest_client` was defined but never imported. What else is defined but never used, or used but never defined?
- **Lock scope completeness**: Every resource guarded by a lock in one path — verify ALL paths that touch that resource also acquire the same lock. Phase 10 found 3 instances of asymmetric locking.
- **Lazy getter callers**: `_get_ingest_semaphore()`, `_get_embed_semaphore()`, `_get_client_lock()`, `_get_llm_lock()` — verify every call site properly `await`s the getter and uses the returned object correctly.
- **Budget arithmetic**: Independently compute the token budget from scratch using the formula in `build_context()`. Compare against comments, diagrams, tables, and the validator. Look for off-by-one errors in `INJECTION_OVERHEAD`, `FRAMEWORK_OVERHEAD`, or separator token accounting.
- **Docker/Nginx/systemd coherence**: Cross-reference port bindings, volume mounts, healthcheck URLs, restart policies, and UFW rules for contradictions.

Trace execution paths with concrete values. Show your proof. Compute your own math. Do not trust comments — verify them against the code they describe.

---

## OUTPUT FORMAT

For each finding:

```
### FINDING-P11-XX: [Title]
- **Severity:** CRITICAL / SIGNIFICANT / MINOR
- **Classification:** [ADDITIVE] / [CORRECTIVE] / [SUBTRACTIVE]
- **Description:** What is wrong and why it matters.
- **Proof:** Trace the exact execution path with concrete data values.
- **Fix:** Exact code change required.
```

## VERDICTS

After completing your audit, provide:

1. **Verdict:** PASS / CONDITIONAL / BLOCKED
2. For CONDITIONAL: list exact fixes required before deployment
3. **Confidence score** (0-100%) — your confidence that no CRITICAL defects remain after your fixes
4. **Residual risk** — what cannot be verified from the document alone
5. **Convergence assessment** — given 178 fixes over 10 phases by 5 independent auditors, should the system proceed to operational testing or does another audit phase have positive expected value?

## INTEGRITY CHECKLIST

Before submitting, confirm:
- [ ] No finding overlaps with the 178 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace with specific data values
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] You audited the ENTIRE document (2,342 lines), not just code blocks — including Docker Compose, Nginx config, backup scripts, verification framework, system prompt, frontend JS, validator, tribal knowledge subsystem, and all comments/diagrams
- [ ] All math independently computed — not copied from any prior audit or from this prompt
