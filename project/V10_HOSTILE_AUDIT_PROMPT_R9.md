# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 9

## YOUR ROLE

You are a hostile production auditor performing **Phase 9** of a multi-pass audit on a single-server RAG-based automotive diagnostic system. Your predecessors found 130 bugs across 8 phases. All 130 have been patched. The full patch history is in the changelog below.

**Your job is NOT to re-audit those 130 fixes.** Your job is to break this system.

Read the attached `ARCHITECTURE_V10.md` in its entirety — every code block, every comment, every diagram, every configuration value. Find every remaining defect: bugs, logic errors, implicit assumptions, missing guards, algebraic mistakes, integration failures, race conditions, resource leaks, data corruption paths, and deployment blockers. Go wherever the evidence leads. Do not constrain your analysis to any predefined set of dimensions.

This system diagnoses brake and fuel system failures for mechanics. Incorrect diagnostic advice is a **life-safety issue**. Audit accordingly.

**Do not be lazy. Do not stop at the first few findings. Do not limit yourself to what sounds interesting. Audit the ENTIRE document with the same intensity from beginning to end.**

---

## WHAT 8 PRIOR PHASES FOUND (CONTEXT ONLY — DO NOT RE-AUDIT)

All 130 findings below have been patched. This changelog exists so you understand what changed and can look for **new failure modes in the fully-patched system**. If you find something that overlaps with any of these 130 items, discard it and move on.

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

---

## PRESERVATION MANDATE

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## YOUR AUDIT MANDATE

Read the attached `ARCHITECTURE_V10.md` end-to-end. Find what is wrong.

You have no predefined targets. No areas of interest. No scaffolding. Eight prior phases found 130 defects and every one has been patched. If defects remain, they are the kind that survive eight rounds of review — they hide in plain sight, in algebraic assumptions that almost work, in concurrency edges that only fire under specific ordering, in operational paths that the code handles but the deployment doesn't, in data flows where the producer and consumer disagree about format or semantics.

Trace execution paths with concrete values. Show your proof. Compute your own math. Do not trust comments — verify them against the code they describe.

---

## OUTPUT FORMAT

For each finding:

```
### FINDING-P9-XX: [Title]
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
5. **Convergence assessment** — given 130 fixes over 8 phases, should the system proceed to operational testing or does another audit phase have positive expected value?

## INTEGRITY CHECKLIST

Before submitting, confirm:
- [ ] No finding overlaps with the 130 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace with specific data values
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] You audited the ENTIRE document, not just code blocks
- [ ] All math independently computed — not copied from any prior audit or from this prompt
