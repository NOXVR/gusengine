# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 5

## YOUR ROLE

You are a hostile production auditor performing **Phase 5** of a multi-pass audit. Phase 1 found 20 isolated execution bugs. Phase 2 found 15 cross-component interaction bugs. Phase 3 found 17 edge-case defects. Phase 4 found 15 fix interaction defects across two independent auditors — including budget overflow from math clamping, single-signal fusion crashes, host-to-container path mismatch, and DOMPurify content stripping. All **67 findings** have been patched.

**Your job is NOT to re-audit those 67 fixes.** Your job is to:

1. **Find fourth-order effects** — 67 patches are now layered. Phase 4 fixes modified core control flow (eviction `break` → `continue`, conditional fusion query, markdown fence stripping, basename path extraction). These changes alter execution paths that ALL previous fixes assumed were stable. Find where old assumptions break.
2. **Stress-test the Phase 4 code itself** — Phase 4 added: a post-eviction content truncation guard (P4-02), a persistent LLM httpx singleton (P4-06), a 5-attempt startup retry loop (P4-07), per-chunk error handling in ingestion (P4-08), regex-based markdown fence stripping (DT-P4-06), conditional Qdrant query routing (DT-P4-02), and basename-based path construction (DT-P4-04). These are all first-audit code.
3. **Verify convergence** — After 4 rounds and 67 fixes, the system should be stabilizing. If you find only MINOR/edge-case issues, that signals convergence. If you find CRITICAL issues, the system is NOT converging and deeper structural problems exist.

Phase 1 found the obvious. Phase 2 found the interactions. Phase 3 found the edge cases. Phase 4 found fix-on-fix conflicts. **You are looking for residual instability: does the system converge to correctness, or do fixes keep generating new failure modes?**

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
| P4-02 | Post-eviction content truncation | Oversized single message → `TOKENIZER.decode(tokens[:8000])` |
| P4-03 | Eviction strip guard | DT-P3-07 strip only if `len(truncated) > 1` — prevents empty history |
| P4-04 | textContent for plaintext | `mechanic_instructions`/`diagnostic_reasoning` → `.textContent` (preserves `<B+>`) |
| P4-05 | Chat embed semaphore | `embed_text()` in chat wrapped in `EMBED_SEMAPHORE` |
| P4-06 | Persistent LLM httpx | `_get_llm_client()` singleton replaces per-call `httpx.AsyncClient` |
| P4-07 | Startup retry loop | 5-attempt exponential backoff in `ensure_qdrant_collection()` + `SystemExit` on fail |
| P4-08 | Per-chunk error handling | try/except per chunk in ingestion — skip on failure, don't abort PDF |
| P4-09 | Validator shared tokenizer | `validate_ledger.py` imports from shared module with host fallback |
| P4-10 | JSON schema validation | `current_state` field required after `json.loads()` |
| P4-11 | Tokenizer pre-check | `os.path.isdir()` + `SystemExit` with clear message |
| DT-P4-02 | Conditional fusion query | Single-prefetch → direct query; dual-prefetch → `FusionQuery(RRF)` |
| DT-P4-04 | Basename path extraction | `os.path.basename()` extracts filename from host webhook path |
| DT-P4-05 | Eviction skip oversized | `break` → `continue` — skip oversized messages, salvage older ones |
| DT-P4-06 | Markdown fence stripping | Strip `` ```json `` wrappers before `json.loads()` + schema check |

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## AUDIT DIMENSIONS (PHASE 5 — CONVERGENCE ANALYSIS)

### Dimension 1: PHASE 4 FIX CODE REVIEW

Phase 4 added 15 fixes, several introducing new control flow. Audit each as production code:

1. **P4-02 — Post-eviction content truncation:** Uses `TOKENIZER.decode(tokens[:8000])` to hard-truncate oversized messages. `decode(encode(text)[:N])` can split a multi-byte character or a mid-word boundary. If the truncated text ends with a partial JSON structure or a broken sentence, does this corrupt the LLM's interpretation of the chat history? What if the truncated message was the user's only context for the diagnostic — they lose the second half of their symptom description.

2. **DT-P4-05 — Eviction `break` → `continue`:** The eviction loop now CONTINUES past oversized messages. With `break`, the loop always terminated at the first oversized message. With `continue`, the loop processes ALL messages in reverse order, skipping any that don't fit, and keeping smaller ones that do. But `truncated.insert(0, msg)` inserts at position 0 — is the message ordering still correct when messages are non-contiguously selected? Can the resulting history have interleaved user/assistant pairs from different conversation turns?

3. **DT-P4-06 — Regex fence stripping:** The regex `re.sub(r'^```(?:json)?\s*\n?', '', response.strip())` strips a single opening fence. What if the LLM outputs nested fences (```json\n```json\n{...}\n```\n```)? What about partial fences like ` ```json{...}` (no newline)? Does `response.strip()` remove leading whitespace that might be significant within the JSON? Can the regex accidentally match content INSIDE the JSON payload (e.g., a diagnostic_reasoning field containing triple backticks)?

4. **DT-P4-02 — Conditional fusion query:** The `len(prefetch_list) >= 2` check routes to fusion vs direct. But the direct query uses `using="dense"`. If Qdrant's collection was created with named vectors (`dense` and `sparse`), does `using="dense"` require the vector name to match exactly? What if the collection schema uses a different name?

5. **DT-P4-04 — Basename path extraction:** `os.path.basename(body["pdf_path"])` extracts the filename. But `os.path.basename("/home/user/storage/pdfs/subdir/manual.pdf")` returns `"manual.pdf"` — the `subdir/` is lost. If the host PDF directory has subdirectories, basename flattens the structure and may cause filename collisions. Is the host PDF directory flat or hierarchical?

6. **P4-07 — Startup retry with `SystemExit`:** After 5 failed attempts, `raise SystemExit(...)` fires. In a Docker container with `restart: unless-stopped`, this triggers an infinite restart loop if Qdrant is permanently down. The backoff totals 1+2+4+8+16 = 31 seconds. Docker's default restart policy uses exponential backoff too. Can the combined backoff strategy cause resource exhaustion from repeated container startups?

7. **P4-08 — Per-chunk error handling:** The `except Exception` catches ALL errors per chunk. If TEI is permanently down, every single chunk will individually fail, log a warning, and continue. For a 200-chunk PDF, this produces 200 warning logs and indexes 0 chunks — but reports `"Indexed 200 chunks"` because the count is `len(chunks)`, not successful insertions. Is the success count accurate?

### Dimension 2: FIX CHAIN INTEGRITY (Phase 4 Interactions)

Phase 4 fixes modified control flow that earlier fixes depend on. Trace these chains:

1. **Eviction overhaul: P3-02 + DT-P3-07 + P4-03 + DT-P4-05 + P4-02.** Five fixes now govern eviction. Trace: chat_history = [{user: 10001}, {assistant: 200}, {user: 500}, {assistant: 300}]. Loop (reversed): keeps 300, keeps 500, keeps 200, skips 10001 (continue). truncated = [{assistant:200}, {user:500}, {assistant:300}]. DT-P3-07+P4-03: first is assistant, len(truncated)=3 > 1, so strip it. Final: [{user:500}, {assistant:300}]. tokens = 800. P4-02: 800 < 8000, no truncation. **Is the message ordering correct after the `continue` skip?**

2. **JSON defense chain: P3-12 + P4-10 + DT-P4-06.** Three fixes now govern JSON validation. `DT-P4-06` strips fences, `P4-10` validates schema, `P3-12` catches non-JSON. Trace: LLM outputs `"```json\n{\"current_state\": \"PHASE_B_FUNNEL\", ...}\n```"`. Regex strips fences → raw JSON → `json.loads()` succeeds → `current_state` present → passes. **But what if the LLM outputs `"Here is the response:\n```json\n{...}\n```"` (prose before the fence)?** The regex only strips leading ```` ``` ```` — the "Here is the response:" survives. `json.loads()` fails. PHASE_ERROR returned. Is this a realistic LLM output pattern?

3. **Ingestion path chain: DT-P4-04 + P2-11 + DT-P3-04.** The `basename()` extraction feeds into `realpath()` + `startswith()` validation. Trace: host sends `{"pdf_path": "/home/user/../../../etc/passwd.pdf"}`. `basename()` = `"passwd.pdf"`. `join("/app/pdfs", "passwd.pdf")` = `"/app/pdfs/passwd.pdf"`. `realpath()` = `"/app/pdfs/passwd.pdf"`. `startswith("/app/pdfs/")` = True. `endswith(".pdf")` = True. **File doesn't exist → ingestion fails gracefully or crashes?** Does `parse_and_chunk()` handle FileNotFoundError?

4. **Search fallback chain: DT-P4-02 + DT8 + H05.** DT8 conditionally drops sparse prefetch. DT-P4-02 routes single-prefetch to direct query. H05 applies `min_absolute_score` floor. **But H05's score filtering uses RRF scores.** In the dense-only direct query path, scores are cosine similarity (range 0-1), NOT RRF rank scores (range ~0.01-0.02). If `min_absolute_score = 0.013`, a cosine score of 0.85 passes trivially. The filter is meaningless in dense-only mode. **Is this a correctness issue, or just a no-op?**

### Dimension 3: FRONTEND STATE MACHINE CONSISTENCY (Post-P4)

Phase 4 changed how the backend formats responses. Verify frontend compatibility:

1. **P4-04 (textContent):** `mechanic_instructions` and `diagnostic_reasoning` are now set via `.textContent` instead of `.innerHTML + DOMPurify.sanitize()`. If the LLM ever outputs actual HTML formatting (e.g., `<b>IMPORTANT</b>: Check voltage`), `.textContent` will display the raw tags as text: `"<b>IMPORTANT</b>: Check voltage"`. Is this acceptable? The system prompt says "output raw JSON only" — does it also prohibit HTML in field values?

2. **DT-P4-06 (fence stripping) + P4-10 (schema check):** The backend now strips fences and validates schema. If validation passes, `response = stripped` is returned. But the frontend's `parseGusResponse()` was designed to handle fence-wrapped JSON (forward-scanning brute-force extraction). Now the backend pre-strips fences. Is `parseGusResponse()` still needed? If removed, what handles edge cases where the backend's regex fails but the frontend parser would succeed?

3. **P4-02 (content truncation):** Truncated chat messages are sent back to the LLM in subsequent turns. The LLM sees a user message that ends mid-sentence. Does the SYSTEM_PROMPT instruct the LLM how to handle truncated context? Or does the LLM attempt to "complete" the truncated message in its next response?

### Dimension 4: NUMERICAL VERIFICATION (Post-Phase-4 Budget Math)

Phase 4's eviction overhaul changes the budget math. Verify:

**Scenario U: Continue-based eviction with interleaved sizes**
```
chat_history = [
  {user: 3000}, {assistant: 3000},  // Turn 1
  {user: 5000}, {assistant: 200},   // Turn 2 (user pasted large diagnostic)
  {user: 500},                      // Turn 3 (current)
]
user_query = 500 (current message, NOT in history)
```
Eviction loop (reversed): keeps 500, keeps 200, keeps 5000 (running=5700), continue on 3000 (5700+3000=8700>8000), continue on 3000 (5700+3000=8700>8000). truncated = [{assistant:200}, {user:5000}, {user:500}]? Or [{user:5000}, {assistant:200}, {user:500}]? **Verify message ordering after non-contiguous selection.**

**Scenario V: Regex fence stripping edge case**
```
LLM output: "```json\n{\"current_state\":\"PHASE_B_FUNNEL\",\"diagnostic_reasoning\":\"Check ```connector``` pins\"}\n```"
```
After regex stripping: does the inner ```` ``` ```` survive or get stripped? Trace the regex behavior character by character.

**Scenario W: Dense-only score filtering**
```
Dense cosine similarity scores: [0.92, 0.87, 0.73, 0.45, 0.12]
min_absolute_score = 0.013
min_score_ratio = 0.70
threshold = 0.92 * 0.70 = 0.644
```
All scores ≥ 0.013 (absolute floor trivially passes). Scores ≥ 0.644: [0.92, 0.87, 0.73]. **Is this the correct filtering behavior for dense-only, or should scoring parameters differ from RRF mode?**

**Scenario X: Failed chunk count reporting**
```
200-chunk PDF, TEI permanently down.
Per-chunk error handler catches all 200 failures.
After loop: logger.info(f"Indexed {len(chunks)} chunks from {pdf_path}")
```
Log says "Indexed 200 chunks" but 0 were actually indexed. **Is this misleading?**

### Dimension 5: CONVERGENCE ASSESSMENT

This is the critical dimension. After 4 rounds and 67 fixes:

1. **Fix generation rate:** Phase 1: 20, Phase 2: 15, Phase 3: 17, Phase 4: 15. The rate is NOT decreasing. If Phase 5 finds 10+ non-edge-case issues, the system is NOT converging. Assess: are the remaining risks STRUCTURAL (the architecture has fundamental design flaws that keep generating bugs) or SURFACE-LEVEL (each fix correctly resolves its target but exposes adjacent edge cases)?

2. **Fix depth pattern:** Phase 1 found missing code. Phase 2 found wrong interactions. Phase 3 found edge cases. Phase 4 found fix-on-fix conflicts. If Phase 5 finds fix-on-fix-on-fix conflicts, the fix layering strategy itself is the problem. Assess: should the eviction system be redesigned from scratch rather than receiving a 6th incremental patch?

3. **Test-by-audit limitations:** This architecture has never been executed. All fixes are theoretical. What is the probability that the first real execution reveals a category of bug that document-level auditing CANNOT catch (e.g., asyncio event loop interaction, httpx connection pool behavior, Qdrant MVCC edge cases)?

### Dimension 6: DOCKER/INFRASTRUCTURE — POST-P4 STATE

Phase 4 modified startup behavior and ingestion paths:

1. **P4-07 + Docker restart policy:** `ensure_qdrant_collection()` now `raise SystemExit(...)` after 5 failed retries. With Docker `restart: unless-stopped`, this creates a restart loop. Total delay per cycle: 31s (backoff) + container boot time. If Qdrant takes 2 minutes to load persistence, the backend cycles through 3-4 restarts before stabilizing. **Is this acceptable, or should the retry count/backoff be extended?**

2. **DT-P4-04 + Volume mount assumptions:** `os.path.basename()` assumes the host daemon sends a full path and the PDF filename is unique. The Docker volume mount maps `./storage/pdfs:/app/pdfs`. If the host directory contains `subdir/manual.pdf` and `manual.pdf`, both resolve to `/app/pdfs/manual.pdf` after basename flattening. **Does the host directory structure support this assumption?**

3. **P4-08 + ingestion metrics:** Per-chunk error handling means a partial ingestion is possible (e.g., 150/200 chunks indexed). The success log reports `len(chunks)` not actual indexed count. Downstream, the operator believes the PDF is fully indexed. **Is partial ingestion worse than total failure?** At least total failure triggers the error manifest.

---

## SCENARIO TRACES (Phase 5 — Convergence Paths)

**Scenario U: Non-Contiguous Eviction Ordering**
chat_history contains 5 messages from 3 turns. The `continue`-based eviction loop skips 2 oversized messages in the middle. Are the remaining messages in correct chronological order? Does the LLM see a coherent conversation, or a jumbled sequence with missing context?

**Scenario V: Nested Markdown Fences in LLM Output**
The LLM wraps its JSON in ```json fences AND includes triple backticks inside a field value (e.g., in `diagnostic_reasoning` referring to a code block). Does the regex strip the outer fence correctly? Does it corrupt the inner content?

**Scenario W: Dense-Only Fallback Scoring**
TEI sparse fails. Search falls back to dense-only mode via DT-P4-02. The score filtering logic applies RRF-calibrated thresholds to cosine similarity scores. Are the filter parameters appropriate for both scoring regimes, or should they adapt based on query mode?

**Scenario X: Silent Partial Ingestion**
TEI flickers during a 200-chunk bulk ingestion. P4-08 catches each failure individually. 50 chunks fail, 150 succeed. The success log reports 200. The operator never re-ingests the PDF. 25% of the FSM content is permanently missing from the vector store. The mechanic gets an incomplete diagnostic. **How would the operator or system detect this?**

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P5-XX: [Title]
- **Dimension:** [1-6]
- **Severity:** CRITICAL / SIGNIFICANT / MINOR
- **Classification:** [ADDITIVE] / [CORRECTIVE] / [SUBTRACTIVE]
- **Description:** What is wrong and why it matters.
- **Proof:** Trace the exact execution path, showing the failure.
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
- [ ] No finding overlaps with the 67 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] All scenario traces (U through X) complete with predicted outcomes
- [ ] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [ ] Budget math independently computed for all edge-case scenarios
- [ ] Convergence assessment in Dimension 5 includes a quantitative verdict
