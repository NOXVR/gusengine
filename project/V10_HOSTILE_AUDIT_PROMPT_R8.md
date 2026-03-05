# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 8

## YOUR ROLE

You are a hostile production auditor performing **Phase 8** of a multi-pass audit on a single-server RAG-based automotive diagnostic system. Your predecessors found 113 bugs across 7 phases. All 113 have been patched. The full patch history is in the changelog below.

**Your job is NOT to re-audit those 113 fixes.** Your job is to break this system. Read the architecture document end-to-end and find every remaining defect — bugs, logic errors, implicit assumptions, missing guards, algebraic mistakes, integration failures, race conditions, resource leaks, and deployment blockers. Do not constrain your analysis to any predefined dimensions. Go wherever the evidence leads.

After 7 phases and 113 fixes, the easy bugs are gone. What remains are:
- **Integration seams** where independently-correct components interact incorrectly
- **Implicit contracts** enforced by convention but not by code
- **Algebraic errors** in the budget chain that compound under edge cases
- **Operational failure modes** that only manifest under real container orchestration
- **Fix-introduced regressions** — Phase 7 found one (P7-09: missing `import os`). There may be more.

**Do not be lazy. Do not stop at the first few findings. Do not limit yourself to what sounds interesting. Audit the ENTIRE document with the same intensity.** The system diagnoses brake and fuel system failures for mechanics — incorrect diagnostic advice is a life-safety issue.

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

### Phase 7 — Systemic Design Flaws (18 fixes across two auditors + Gemini cross-reference)

#### Opus Phase 7 — Initial Batch (7 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P7-01 | **count_tokens() wiring (CRITICAL)** | All 10 direct `TOKENIZER.encode()` calls replaced with `count_tokens()`. 4 imports updated. `LockedTokenizer` wrapper for Docling's chunker. |
| P7-02 | FRAMEWORK_OVERHEAD constant | `FRAMEWORK_OVERHEAD = 100` deducted from build_context() → **raised to 250 by P7-17** |
| P7-03 | MIN_RAG_FLOOR rejection | Silent override replaced with `raise ValueError` — caught by chat handler as PHASE_ERROR |
| P7-04 | Circuit breaker | 5 consecutive chunk failures → `IngestionError` — prevents CPU-speed data discard |
| P7-05 | Embed semaphore timeout | `asyncio.wait_for(EMBED_SEMAPHORE.acquire(), timeout=5.0)` — prevents chat starvation |
| P7-07 | ~~Pre-ingestion chunk delete~~ | ~~Delete stale chunks before re-index~~ **REMOVED by P7-14 (search blackout risk)** |
| P7-08 | Model name from env var | `VLLM_MODEL = os.environ.get("VLLM_MODEL", "Qwen2.5-32B-Instruct-AWQ")` |

#### Gemini Phase 7 Cross-Reference (3 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| GP7-05 | TEI pool flush | `embed_text()` catches `ConnectError`/`ReadTimeout` → flushes httpx pool via `_flush_embed_client()` |
| GP7-10 | vLLM healthcheck upgrade | Docker healthcheck `/health` → `/v1/models` — verifies GPU engine, not just HTTP |
| GP7-11 | Search filter telemetry | `SEARCH FILTER SUPPRESSION` warning when chunks found but all below threshold |

#### Opus Phase 7 — Second Batch (8 findings)

| # | Fix | What Changed |
|:--|:----|:-------------|
| P7-09 | **Missing `import os` (CRITICAL)** | Added to `pipeline.py` — P7-07's `os.path.basename()` was NameError. Regression from P7-07 patch. |
| P7-10 | Validator budget formula | Shows both no-chat and worst-case budgets with all runtime deductions |
| P7-11 | Runtime ledger cap | `LEDGER_MAX_TOKENS` guard truncates oversized ledger with warning |
| P7-12 | LLM client pool flush | GP7-05 pattern applied to `generate_response()` — flush on `ConnectError`/`ReadTimeout` + explicit `Timeout`/`Limits` |
| P7-13 | Embed flush race protection | `asyncio.Lock` serializes `_flush_embed_client()` — prevents double-close under concurrent TEI failures |
| P7-14 | **Re-ingestion blackout fix** | Removed P7-07 pre-delete. UUID5 upsert handles matching chunks. Ghost chunk cleanup deferred to offline `/api/cleanup`. |
| P7-15 | Chat history validation | Schema validation: each entry must be `dict` with `str` content and valid role. Malformed entries dropped with warning. |
| P7-17 | FRAMEWORK_OVERHEAD increase | `100` → `250` — covers worst-case 40+ message ChatML framing |

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## YOUR AUDIT MANDATE

Read the attached `ARCHITECTURE_V10.md` in its entirety. Audit everything — token arithmetic, Python code correctness, Docker configuration, system prompt logic, frontend JavaScript, data flow between modules, import paths, API contracts, concurrency safety, error handling completeness, and operational deployment viability.

**Do not limit yourself to any predefined set of dimensions or scenarios.** Prior phases used structured dimensions as scaffolding. You are past that. Interpret the document as a hostile reviewer. Find what is wrong. Trace execution paths with concrete values. Show your proof.

The system has been through 7 rounds of audit and 113 patches. The remaining defects — if any exist — are subtle. They live in the seams between components, in edge cases that no prior auditor traced, in algebraic assumptions that are almost-but-not-quite correct, and in operational conditions that the document describes but does not fully account for.

---

## AREAS OF POTENTIAL INTEREST

The following are **not prescriptive audit targets** — they are areas where we believe post-P7 changes may have introduced new behavior worth examining. You are free to ignore these entirely if your independent analysis finds more significant issues elsewhere.

- **FRAMEWORK_OVERHEAD was raised from 100→250** (P7-17). The budget chain is now tighter. We have not independently verified whether 250 is sufficient for all legal message counts.
- **P7-14 removed the pre-delete during re-ingestion.** The system now relies entirely on UUID5 upsert for re-ingestion correctness. Ghost chunks from shrunk PDFs accumulate.
- **P7-13 added asyncio.Lock to the TEI pool flush** but P7-12's LLM pool flush has no equivalent lock. The asymmetry may or may not matter depending on concurrency patterns.
- **P7-11's ledger truncation** uses `TOKENIZER.decode(TOKENIZER.encode(text)[:N])` and then hardcodes the token count without re-counting. Encode→decode round-trips can change token counts.
- **P7-15 validates chat_history entries individually** but does not cap message count. Message count affects ChatML framing tokens, which are budgeted by FRAMEWORK_OVERHEAD.

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P8-XX: [Title]
- **Severity:** CRITICAL / SIGNIFICANT / MINOR
- **Classification:** [ADDITIVE] / [CORRECTIVE] / [SUBTRACTIVE]
- **Description:** What is wrong and why it matters.
- **Proof:** Trace the exact execution path, showing the failure with concrete data.
- **Fix:** Exact code change required.
```

## VERDICTS

After completing your audit, provide:

1. **PASS / CONDITIONAL / BLOCKED** verdict
2. For CONDITIONAL: list exact fixes required before deployment
3. **Confidence score** (0-100%) — your confidence that no CRITICAL defects remain
4. **Residual risk** — what cannot be verified from the document alone and must be caught by integration testing
5. **Convergence assessment** — given 113 fixes over 7 phases with this finding profile, should the system proceed to operational testing or does another audit phase have positive expected value?

## INTEGRITY CHECKLIST

Before submitting, confirm:
- [ ] No finding overlaps with the 113 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace with specific data values
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] You audited the ENTIRE document, not just the areas of potential interest listed above
- [ ] Budget math independently computed — not copied from any prior audit or from this prompt
- [ ] At minimum, you assessed: token arithmetic, code correctness, concurrency safety, deployment viability
