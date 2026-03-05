# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 6

## YOUR ROLE

You are a hostile production auditor performing **Phase 6** of a multi-pass audit. Phase 1 found 20 isolated execution bugs. Phase 2 found 15 cross-component interaction bugs. Phase 3 found 17 edge-case defects. Phase 4 found 15 fix interaction defects (budget overflow, single-signal fusion crash, path mismatch, content stripping). Phase 5 found 16 convergence defects across two independent auditors — including silent partial ingestion, eviction role-alternation crash, mode-incompatible score filtering, httpx connection exhaustion, and orphan assistant context poisoning. All **83 findings** have been patched.

**Your job is NOT to re-audit those 83 fixes.** Your job is to:

1. **Construct adversarial edge cases** — The system has been through 5 rounds of document-level auditing. The easy bugs are gone. What remains are scenarios that only manifest under specific input combinations, timing conditions, or data-dependent paths. Build Scenario Traces that chain 3+ components and demonstrate failure through concrete data.
2. **Stress-test the Phase 5 corrections** — Phase 5 made significant control flow reversals: `continue` was reverted to `break`, the orphan assistant guard was removed, a zero-success IngestionError raise was added, pool limits were applied, and the score floor became mode-adaptive. Each reversal invalidates assumptions that other code was written against. Find where those assumptions survive.
3. **Probe the boundary between document-level audit and runtime behavior** — This architecture has NEVER been executed. 83 fixes have been applied on paper. Identify specific scenarios where the document is internally consistent but runtime behavior would diverge (e.g., asyncio scheduling, httpx pool exhaustion timing, Qdrant MVCC during concurrent upsert+query, Python garbage collection of `id()`-tracked objects).

Phase 1 found the obvious. Phase 2 found the interactions. Phase 3 found the edge cases. Phase 4 found fix conflicts. Phase 5 found convergence failures and corrected structural reversals. **You are looking for: what breaks at the boundary between a correct specification and messy reality?**

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
| DT-P3-03 | User query length cap | `MAX_USER_QUERY_TOKENS=10000` — early reject before budget math |
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
| P5-04 | Mode-adaptive score floor | RRF: `0.013` / Dense-only: `0.35` — prevents off-topic injection in fallback |
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
| DT-P5-06 | `SystemExit` → `RuntimeError` | Tokenizer pre-check now catchable by `except ImportError` in host validator |
| DT-P5-07 | Orphan assistant strip (always) | Removed P4-03 `len>1` guard + P4-02 content truncation. Empty history > poisoned history. |

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## AUDIT DIMENSIONS (PHASE 6 — EDGE CASE STRESS TESTING)

### Dimension 1: EVICTION CHAIN — POST-REVERSAL EDGE CASES

The eviction system has been through 6 fixes and 2 reversals. Its current state:
- Loop walks newest→oldest, `break` on first budget overflow (DT-P5-01)
- Leading orphan assistant always stripped — even if it empties history (DT-P5-07)
- No content truncation of oversized messages (DT-P5-07 removed P4-02)
- `and truncated` guard prevents break on the very first message (P3-02)

Probe these edge cases:

1. **Single-message history with user message:** `chat_history = [{user: 9000}]`. Budget is 8000. Loop: 9000 > 8000 but `truncated` is empty → P3-02 guard fires, message is kept. `truncated = [{user: 9000}]`. Not an assistant, so no strip. `chat_history_tokens = 9000`. This exceeds `MAX_CHAT_HISTORY_TOKENS`. The old P4-02 truncation would have caught this — **it's been removed.** Does `build_context()` receive `chat_history_tokens = 9000` and compute a negative `available` value? Does `MIN_RAG_FLOOR` clamp save it, or does the total prompt exceed 32,768?

2. **All-assistant history:** `chat_history = [{assistant: 100}, {assistant: 100}]`. Eviction keeps both (200 < 8000). Strip: first is assistant → strip it. `truncated = [{assistant: 100}]`. First is STILL assistant → **does the strip logic fire again, or is it a one-shot check?** If one-shot, the LLM sees `system → assistant → user` — wrong role order.

3. **Empty history after strip:** `chat_history = [{assistant: 7500}]`. Loop: 7500 < 8000 → keep. `truncated = [{assistant: 7500}]`. Strip: first is assistant → strip. `truncated = []`. `chat_history = []`. `chat_history_tokens = running - 7500 = 0`. What happens when `generate_response()` receives an empty `chat_history`? Does Qwen2.5's `apply_chat_template()` handle it, or does it crash on an empty messages list?

4. **Budget interaction with strip:** `chat_history = [{assistant: 7900}, {user: 50}]`. Loop (reversed): keeps {user: 50} (running=50), keeps {assistant: 7900} (running=7950). Budget OK. orphan check: first is assistant → strip. `running = 7950 - 7900 = 50`. Only 50 tokens of chat history remain. The budget gave 7950 tokens to chat history but 7900 were stripped. **Is the freed budget reclaimed by `build_context()`, or is it wasted?**

### Dimension 2: INGESTION ERROR CHAIN — COMPLETE TRACE

The ingestion pipeline now has three error paths: IngestionError (parse failure), per-chunk Exception (embed/index failure), and DT-P5-04's zero-success IngestionError. Trace the complete chain:

1. **Partial failure (50/200) flow:** 50 chunks fail, 150 succeed. `failed_count = 50`. `indexed_count = 150`. The partial failure block writes to `FAILURE_MANIFEST_PATH`. But `indexed_count > 0`, so DT-P5-04 doesn't fire. The function returns 150. Background wrapper logs "Background ingestion complete: manual.pdf (150 chunks)". **The operator sees "150 chunks" and might assume this is the full PDF.** How does the operator know the PDF originally had 200 chunks? Is the manifest entry enough?

2. **Manifest write race condition:** Two concurrent ingestions (PDF-A and PDF-B) both partially fail. Both attempt `open(FAILURE_MANIFEST_PATH, "a")` simultaneously. Python's `open("a")` mode is POSIX-atomic for individual `write()` calls on most filesystems, but `f.write(f"...")` may issue multiple `write()` syscalls for f-strings that exceed the buffer. **Can manifest entries from concurrent writes interleave mid-line?**

3. **IngestionError → IngestionError double-write:** If DT-P5-04 fires (`indexed_count == 0`), it raises IngestionError AFTER the partial failure block already wrote to the manifest (because `failed_count > 0` is also true when all chunks fail). The background wrapper ALSO writes to the manifest when catching IngestionError. **Does the same PDF appear twice in the manifest with different messages?**

### Dimension 3: SEARCH SCORING — DENSE-ONLY CALIBRATION

P5-04 set the dense-only floor at 0.35. Verify this calibration:

1. **BGE-M3 cosine similarity behavior:** BGE-M3 dense vectors are 1024-dimensional, L2-normalized. Cosine similarity for even completely unrelated texts rarely drops below 0.2-0.3 in high-dimensional embedding spaces. **Is 0.35 actually selective enough?** What percentage of random query-document pairs would exceed 0.35? Should it be 0.50 or higher?

2. **Dynamic ratio threshold in dense mode:** The `min_score_ratio = 0.70` was calibrated for RRF where scores cluster in a narrow band (~0.0125 to 0.0164). In cosine mode, scores spread widely (0.3 to 0.95). `threshold = top_score * 0.70` means if the best match scores 0.90, the cutoff is 0.63. **This is aggressive filtering that may drop relevant but lower-scoring chunks.** Is the ratio appropriate for both score distributions?

3. **Score interpretation inconsistency:** In RRF mode, `results.points[0].score` is a fused rank score. In dense-only mode, it's a raw cosine similarity. The log message currently says `"Top score {top_score:.4f}"`. **Does downstream code (e.g., context builder, logging, monitoring) ever interpret the score value as a quality indicator?** If so, comparing 0.016 (RRF) to 0.85 (cosine) across sessions produces nonsensical quality metrics.

### Dimension 4: RUNTIME vs SPECIFICATION DIVERGENCE

This architecture has been audited 5 times but never executed. Identify scenarios where document correctness doesn't guarantee runtime correctness:

1. **`asyncio.to_thread()` + Qdrant synchronous client:** `hybrid_search()` is dispatched via `asyncio.to_thread()`. Inside, it calls `client.query_points()` which is synchronous. The Qdrant Python SDK's synchronous client uses `requests` under the hood. `asyncio.to_thread()` runs in the default `ThreadPoolExecutor` (max 5 threads on most systems). **During concurrent chat requests, all 5 threads could be blocked on Qdrant I/O.** New chat requests queue behind them. What's the maximum concurrent chat request capacity?

2. **TOKENIZER thread safety:** `AutoTokenizer.from_pretrained()` returns a HuggingFace tokenizer. `TOKENIZER.encode()` is called from multiple async contexts: `chat()` handler, `build_context()`, `parse_and_chunk()` (via `asyncio.to_thread()`). HuggingFace tokenizers are **NOT guaranteed thread-safe** for the Rust-based fast tokenizers. If two `to_thread()` dispatches call `TOKENIZER.encode()` simultaneously, **can tokenizer state corruption occur?**

3. **httpx connection pool under load:** P5-05 set `max_connections=100`. During a 500-PDF bulk ingestion with `EMBED_SEMAPHORE=8` and `INGEST_SEMAPHORE=2`, the maximum concurrent `embed_text()` calls is `min(8, 2*chunks_per_pdf)`. With 200 chunks/PDF, that's 8 concurrent requests. `max_connections=100` is generous. **But what happens when the TEI container restarts?** Does httpx detect stale connections in the pool, or do subsequent requests fail with connection reset errors until pool connections expire?

4. **Qdrant `id()` stability in Python:** P5-02 (now removed) used `id(m)` to track which messages survived eviction. This was removed. But verify: does ANY remaining code use `id()` for object identity tracking? Python's `id()` returns the memory address of an object. **After garbage collection, a new object can reuse a freed address.** If `id()` is used across GC boundaries, object identity checks become unreliable.

5. **`os.path.realpath()` in Docker containers:** The ingestion path validation uses `os.path.realpath()` to resolve symlinks. Inside a Docker container, `/app/pdfs/` is a bind mount from the host. `realpath()` resolves paths within the container's filesystem namespace. **What if the host directory contains symlinks?** `realpath()` inside the container cannot resolve host-side symlinks — they appear as broken links or regular files. Does `parse_and_chunk()` handle broken symlinks?

### Dimension 5: CONVERGENCE & SYSTEM TOPOLOGY

After 5 rounds and 83 fixes:

1. **Fix generation rate:** Phase 1: 20, Phase 2: 15, Phase 3: 17, Phase 4: 15, Phase 5: 16 (Opus 11 + DT 5). The rate is **oscillating, not converging.** However, Phase 5 included 3 structural reversals (DT-P5-01, DT-P5-07, P5-02 superseded). If you subtract reversals (corrections of corrections), the net NEW defect rate is 13. Assess: is the reversal pattern healthy (converging to correct design) or pathological (thrashing between incompatible approaches)?

2. **Removed code inventory:** DT-P5-07 removed P4-02 (content truncation) and P4-03 (strip guard). DT-P5-01 removed DT-P4-05 (continue behavior) and P5-02 (detection logging). That's 4 fixes removed. Were the original justifications for those fixes wrong, or were they correct at the time but invalidated by subsequent changes? If the latter, **what prevents DT-P5-01 and DT-P5-07 from being invalidated by Phase 6 findings?**

3. **Unsettled components:** Which components have been modified the MOST across 5 phases? If the same 50 lines of chat history eviction have received 8 modifications, that section is fundamentally under-designed. **Should it be redesigned from first principles rather than receiving a 9th incremental patch?**

### Dimension 6: PATH TRAVERSAL & SECURITY BOUNDARY AUDIT

The ingestion path validation chain (DT-P5-05 + P2-11 + DT-P3-04) has been modified 4 times. Verify its security:

1. **DT-P5-05 `split("pdfs/", 1)[-1]` traversal:** The split boundary is the string `"pdfs/"`. What if the host path is `/home/user/storage/pdfs/../../../etc/passwd.pdf`? `split("pdfs/", 1)` → `["...", "../../../etc/passwd.pdf"]`. `[-1]` → `"../../../etc/passwd.pdf"`. `os.path.join("/app/pdfs", "../../../etc/passwd.pdf")` → `"/app/pdfs/../../../etc/passwd.pdf"`. `os.path.realpath()` → `"/etc/passwd.pdf"`. `startswith("/app/pdfs/")` → **FALSE. Caught.** Verify this trace is correct.

2. **Null byte injection:** What if `body["pdf_path"]` contains a null byte: `"/home/user/storage/pdfs/\x00../../etc/passwd.pdf"`? Python 3 strings can contain null bytes. Does `os.path.realpath()` truncate at the null byte (C-library behavior) or process the full string? If truncated, `realpath("/home/user/storage/pdfs/")` → `"/app/pdfs"`. `startswith("/app/pdfs/")` → **FALSE (no trailing slash).** Is this actually safe, or does it depend on platform behavior?

3. **Encoded path components:** What if the webhook payload uses URL encoding: `"pdfs%2F..%2F..%2Fetc%2Fpasswd.pdf"`? Does `split("pdfs/", 1)` still match? URL encoding is NOT automatically decoded by FastAPI `await request.json()` — it preserves the literal string. But does Qdrant, the filesystem, or any downstream component perform decoding?

---

## SCENARIO TRACES (Phase 6 — Edge Case Chains)

**Scenario Y: Oversized Single User Message (Post-DT-P5-07)**
```
chat_history = [{user: 12000}]
MAX_CHAT_HISTORY_TOKENS = 8000
```
Eviction loop: 12000 > 8000, but `truncated` is empty → P3-02 keeps it. Not assistant → no strip. `chat_history_tokens = 12000`. P4-02 truncation is REMOVED. Budget: `32768 - 900 - 2550 - 2000 - 12000 - user_query_tokens`. If `user_query_tokens = 500`: available = `14,818`. MIN_RAG_FLOOR is 5000, so no clamp. **This actually works — 12K chat fits within 32K context.** But what if the user ALSO pastes a 10K query? `32768 - 900 - 2550 - 2000 - 12000 - 10000 = 5,318`. Still above floor. **What if `user_query_tokens = 15000`?** DT-P3-03 caps at 10000, so it's rejected before reaching eviction. Verify the DT-P3-03 guard fires BEFORE eviction.

**Scenario Z: All-Assistant Chat History**
```
chat_history = [{assistant: 100}, {assistant: 100}, {assistant: 100}]
```
This would occur if the frontend sends malformed history. Eviction keeps all (300 < 8000). Strip: first is assistant → strip. `truncated = [{assistant: 100}, {assistant: 100}]`. First is STILL assistant. **Is there a second strip pass?** If not, vLLM receives `system → assistant → assistant → user`. ChatML violation → HTTP 400?

**Scenario AA: Concurrent Ingestion Manifest Corruption**
```
PDF-A: 200 chunks, 200 fail (TEI down)
PDF-B: 300 chunks, 300 fail (TEI still down)
Both running concurrently under INGEST_SEMAPHORE=2.
```
PDF-A: `indexed_count=0, len(chunks)=200`. Partial block writes "PARTIAL: 0/200". Then DT-P5-04 fires: `raise IngestionError(...)`. Background wrapper catches it, writes another line. PDF-B: same sequence. **Four manifest entries for two PDFs — two from partial block, two from wrapper.** Is this confusing or helpful?

**Scenario AB: TEI Restart Mid-Ingestion**
```
500-chunk PDF ingestion in progress.
Chunks 1-100: embed succeeds, index succeeds.
Chunk 101: TEI container OOM-killed, embed_text() raises httpx.ConnectError.
TEI restarts (Docker healthcheck).
Chunks 102-110: embed_text() raises httpx.ConnectError (TEI still starting).
Chunk 111: TEI ready, embed succeeds.
Chunks 111-500: succeed.
```
Result: `indexed_count=490, failed_count=10`. Partial ingestion. The manifest records the partial. But the 10 missing chunks create a GAP in the UUID5 sequence (`pdf_path_101` through `pdf_path_110`). **If the operator re-ingests the full PDF, do the overlapping UUID5 IDs (`pdf_path_0` through `pdf_path_100`) get upserted (updated) or duplicated?** UUID5 is deterministic, so upsert overwrites. **Does this mean re-ingestion is safe and self-healing?** Verify.

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P6-XX: [Title]
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
- [ ] No finding overlaps with the 83 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace with specific data values
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] All scenario traces (Y through AB) complete with predicted outcomes
- [ ] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [ ] Budget math independently computed for all edge-case scenarios
- [ ] Convergence assessment in Dimension 5 includes quantitative analysis of the reversal pattern
- [ ] Security analysis in Dimension 6 includes at least one path traversal attempt trace
