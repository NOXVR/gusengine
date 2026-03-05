# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 4

## YOUR ROLE

You are a hostile production auditor performing **Phase 4** of a multi-pass audit. Phase 1 found 20 isolated execution bugs (missing try/except, wrong API names, ID collisions). Phase 2 found 15 cross-component interaction bugs (budget math divergence, missing imports, unbounded concurrency). Phase 3 found 17 edge-case defects in the patched system (tuple injection, budget overflow paradox, DOMPurify absence, path traversal bypass, eviction role corruption). All **52 findings** have been patched.

**Your job is NOT to re-audit those 52 fixes.** Your job is to:

1. **Stress-test the fix interactions** — 52 patches have been layered onto the architecture. Look for conflicts, ordering dependencies, and emergent behavior between patches.
2. **Find failure modes in the NEW code added by Phase 3** — Phase 3 added significant new logic: a persistent httpx client singleton, an embed semaphore, a shared tokenizer module, a startup collection hook, server-side JSON validation, DAG recovery rules, a user query length cap, and a post-eviction role validator. These are all first-audit code.
3. **Probe the remaining unverified surface area** — some components are described-but-not-shown (parsers, frontend state machines, validators). Assess whether the shown interfaces are sufficient to guarantee correctness, or whether hidden implementations create residual risk.

Phase 1 found the obvious. Phase 2 found the interactions. Phase 3 found the edge cases. **You are looking for third-order effects: fix-on-fix conflicts, subtle state corruption, and any remaining first-request-crash scenarios.**

---

## CUMULATIVE FIX CHANGELOG (DO NOT RE-AUDIT)

All findings below have been patched. Use this list to understand what changed, then look for **conflicts between fixes and emergent behavior in the fully-patched system**.

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

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## AUDIT DIMENSIONS (PHASE 4 — FIX INTERACTION ANALYSIS)

### Dimension 1: PHASE 3 FIX CODE REVIEW

Phase 3 added 17 fixes, many introducing new modules and logic. Audit each as production code:

1. **P3-05 — Persistent httpx client (`_http_client` singleton):** The `_get_client()` function uses a module-level `_http_client` global. If TEI restarts or drops the connection mid-session, does `httpx.AsyncClient` detect the dead connection and fail gracefully? Or does it silently reuse a dead socket and hang? The `is_closed` check only catches explicit `.aclose()` — not server-side disconnects.

2. **P3-04 — EMBED_SEMAPHORE(8) interacts with INGEST_SEMAPHORE(2):** 2 parse jobs release their semaphore, then up to 2 tasks enter the embed loop simultaneously. Each task iterates N chunks (potentially hundreds), acquiring EMBED_SEMAPHORE(8) per chunk. With 2 tasks × hundreds of chunks, can they deadlock? Is there a scenario where all 8 embed permits are held by task A's chunks while task B starves? What about interaction with asyncio's single-threaded event loop?

3. **P3-12 — Server-side JSON validation:** The response is validated with `json.loads(response)`, but only the raw string is returned. If the LLM outputs valid JSON with wrong schema (e.g., `{"answer": "yes"}` instead of the DAG schema), this pass through validation. Is server-side schema validation needed, or does the frontend `parseGusResponse()` handle malformed-but-valid JSON?

4. **P3-03 — `ensure_qdrant_collection()` startup hook:** Uses `@app.on_event("startup")`. If `create_collection()` fails (e.g., Qdrant returns 503 during its own startup), the FastAPI app still launches. Subsequent requests hit a non-existent collection. Should the startup hook retry or block?

5. **DT-P3-07 — Post-eviction role validator:** The fix strips a leading assistant message AND adjusts `chat_history_tokens_removed`. But after the pop, is `running` still accurate? If the popped assistant message had 500 tokens, `running -= 500` is correct. But is the `chat_history_tokens` variable (set later to `running`) used downstream correctly? Trace the variable to `build_context()`.

6. **P3-13 — Shared tokenizer module (`backend/shared/tokenizer.py`):** The `AutoTokenizer.from_pretrained()` call runs at module import time. If the model files are missing or corrupted, this import fails. Since both `parser.py` and `context_builder.py` import from this module, a corrupted tokenizer model kills the ENTIRE backend — both ingestion and chat. Is there error handling at import time?

### Dimension 2: FIX INTERACTION MATRIX

Multiple Phase 3 fixes interact with each other. Trace these specific interaction chains:

1. **Eviction trilogy: P3-02 + DT-P3-07 + P2-02.** The eviction loop (P2-02) now has three guards: (a) keep ≥1 message (P3-02), (b) strip dangling assistant (DT-P3-07), (c) original token cap. Trace: if chat_history = [{role: "user", tokens: 9000}, {role: "assistant", tokens: 100}], what happens? P3-02 forces keeping the 9000-token user message. DT-P3-07 checks if first is assistant — it's user, so no strip. Result: chat_history_tokens = 9000. This exceeds MAX_CHAT_HISTORY_TOKENS=8000 but is kept because P3-02 prevents empty truncation. Does this cause a downstream budget overflow?

2. **Embed chain: P3-05 + P3-04 + P3-08.** Persistent httpx client (P3-05) + embed semaphore(8) (P3-04) + async search dispatch (P3-08). During ingestion, 8 embed requests run concurrently via the persistent client. Meanwhile, a chat request triggers `asyncio.to_thread(hybrid_search)` which needs Qdrant. Does the event loop properly interleave embed_text coroutines with the to_thread dispatch? Or can the 8 embed permits block the chat path?

3. **Budget guard chain: DT-P3-03 + P3-01 + H11.** The user query cap (DT-P3-03, 10K tokens) runs before `build_context()`. build_context now returns a properly destructured tuple (P3-01). MIN_RAG_FLOOR (H11, 5000 tokens) is enforced inside build_context. Trace: user sends 9999 tokens (just under cap). Budget = 32768 - 900 - 2550 - 2000 - 8000 - 9999 = 9319. This is above MIN_RAG_FLOOR. But what if `chat_history_tokens` is 9000 (from the P3-02 oversized message scenario)? Budget = 32768 - 900 - 2550 - 2000 - 9000 - 9999 = 8319. Still above 5000. Is there ANY legal combination that forces MIN_RAG_FLOOR to activate AND produces a total > 32768?

4. **JSON defense chain: P3-12 + P3-07 + P2-05.** Empty RETRIEVED DOCUMENTS section (P3-07) triggers the ZERO-RETRIEVAL SAFEGUARD in the system prompt. The LLM should output RETRIEVAL_FAILURE. Server-side JSON validation (P3-12) checks the output. If the LLM outputs valid RETRIEVAL_FAILURE JSON, it passes. But what if the empty section causes the LLM to output `{"current_state": "RETRIEVAL_FAILURE"}` WITHOUT the required fields (`requires_input`, `answer_path_prompts`, etc.)? Is this an incomplete-but-valid JSON that passes P3-12 validation but crashes the frontend?

### Dimension 3: FRONTEND STATE MACHINE CONSISTENCY

After 52 fixes, the backend and frontend must agree on every response schema. Verify:

1. **PHASE_ERROR fields:** Backend sends `{current_state, mechanic_instructions, diagnostic_reasoning, requires_input, answer_path_prompts, source_citations, intersecting_subsystems}` (7 fields). Does `renderGusResponse()` handle ALL 7? Does it crash if any are missing? What if the LLM generates its own PHASE_ERROR with only `{current_state, mechanic_instructions}`?

2. **DT-P3-03 error response:** The new user-query-too-long error returns PHASE_ERROR with `requires_input: false`. After this error, `buildUserMessage()` will receive a PHASE_ERROR as `lastResponse`. The P3-11 DAG recovery rule says "reset to last valid phase." But `buildUserMessage()` may inject `required_next_state` based on PHASE_ERROR. Does the frontend override the DAG recovery rule? Trace the full frontend flow after a query-too-long rejection.

3. **RETRIEVAL_FAILURE with empty section (P3-07):** The RETRIEVED DOCUMENTS section is now empty (no placeholder text). The ZERO-RETRIEVAL SAFEGUARD instructs: "If the section is empty... output RETRIEVAL_FAILURE." Does `renderGusResponse()` have a code path for RETRIEVAL_FAILURE? Does it display a user-friendly message, or does it fall through to a default handler?

### Dimension 4: NUMERICAL VERIFICATION (Edge Case Budget Math)

Phase 3 added two new budget constraints: `MAX_USER_QUERY_TOKENS=10000` (DT-P3-03) and the P3-02 oversized-message keep. Verify these interact safely:

**Scenario P: Maximum legal budget stress**
```
max_context = 32768
system_prompt = 900
ledger = 2550
response_budget = 2000
chat_history = 9000 (P3-02 kept one oversized message)
user_query = 9999 (just under DT-P3-03 cap)
available_for_RAG = ?
```
Does MIN_RAG_FLOOR activate? If so, what is the total tokens sent to vLLM?

**Scenario Q: Rapid-fire queries exceeding budget**
```
max_context = 32768
system_prompt = 900
ledger = 2550
response_budget = 2000
chat_history = 8000 (at cap)
user_query = 10001 (just over DT-P3-03 cap)
```
DT-P3-03 rejects this. The user shortens to 9999. Now trace: does the previous PHASE_ERROR response from the too-long rejection appear in chat_history on the retry? If so, chat_history might now be 8000 + ~200 (the PHASE_ERROR JSON) = 8200. How does eviction handle this?

**Scenario R: Ledger-free first request with max query**
```
max_context = 32768
system_prompt = 900
ledger = 0
response_budget = 2000
chat_history = 0
user_query = 9999
available_for_RAG = ?
```
This should be the most generous RAG budget despite a huge query. Verify the math is correct.

### Dimension 5: RESIDUAL HIDDEN CODE RISK ASSESSMENT

After 3 rounds of auditing, assess the remaining unverified surface area. For each hidden component, give a **risk rating (LOW/MEDIUM/HIGH)** with justification:

1. **`parseGusResponse(rawText)`** — now the last line of defense after P3-12 (server-side JSON validation). If P3-12 passes valid-but-wrong-schema JSON, does `parseGusResponse` catch it? The architecture says "forward-scanning brute-force" — does this mean it extracts arbitrary JSON objects, or does it validate the DAG schema?

2. **`buildUserMessage(selectedOption, lastResponse)`** — now critical after P3-11 (DAG recovery rules). The backend injects recovery rules into the system prompt, but `buildUserMessage()` injects `required_next_state` into the user message. If both disagree on the recovery path, which wins?

3. **`load_ledger()`** — called on every request. The Phase 3 report noted this reads from disk every time. For a single-user air-gapped system, is this a latency concern? What if the file is being written to (manual edit) during a read — can a partial read occur?

4. **`validate_ledger.py`** — uses `SAFETY_FACTOR=0.85` and `MIN_RAG_BUDGET=20000`. Does it use the same tokenizer (Qwen2.5 AutoTokenizer) as the runtime? If it uses a different tokenizer, the validated budget won't match the actual budget. After P3-13 (shared tokenizer module), is the validator importing from the same module?

### Dimension 6: DOCKER INFRASTRUCTURE — POST-FIX STATE

Phase 3 added `ensure_qdrant_collection()` at startup. Verify the startup sequence is now correct:

1. **Full startup timeline:** Qdrant starts → healthcheck passes → backend starts → `@app.on_event("startup")` fires → `ensure_qdrant_collection()` runs → `qdrant_client.get_collection("fsm_corpus")` → if not found, `create_collection()`. Trace: what if Qdrant reports healthy (TCP accepting connections) but the persistence engine hasn't finished loading? Does `get_collection()` return an error or an empty result?

2. **TEI startup race with persistent client:** TEI starts → healthcheck passes (`/health` returns 200) → backend starts → first chat request → `embed_text()` → `_get_client()` creates persistent `httpx.AsyncClient` → POST to TEI `/embed`. If TEI's model is still loading but `/health` returns 200, the embed request gets a 503. The error handler returns PHASE_ERROR. But the `_http_client` singleton is now initialized. Does it need to be reset after a TEI 503?

3. **Container restart behavior:** If the backend crashes (e.g., `SystemExit` from missing system prompt), Docker restarts it. On restart, `@app.on_event("startup")` fires again. `ensure_qdrant_collection()` tries `get_collection()` — collection exists from last boot. The startup hook succeeds. But is there any state leak from the previous process (e.g., orphaned httpx connections, stale semaphore state)? Note: `asyncio.Semaphore` is in-process — it resets on restart.

---

## SCENARIO TRACES (Phase 4 — Fix Interaction Paths)

**Scenario P: Oversized Message Kept by P3-02 + User Query at Cap**
A mechanic has a 9000-token message in chat_history. P3-02 forces it to be kept (can't empty the history). Then the mechanic sends a 9999-token query (just under the DT-P3-03 cap). Trace the budget math end-to-end. Does the prompt fit in 32768? If not, what breaks — vLLM? Token budget floor? MIN_RAG_FLOOR?

**Scenario Q: PHASE_ERROR Accumulation in Chat History**
Mechanic sends a 10001-token query → DT-P3-03 rejects with PHASE_ERROR. Frontend adds PHASE_ERROR to chat_history. Mechanic retries with a shorter query. chat_history now has the rejection. The eviction loop runs. The PHASE_ERROR message is ~200 tokens. Does this push chat_history over 8000? If so, what gets evicted? Can the PHASE_ERROR itself be evicted, or does it survive? Trace the DAG recovery rule in the LLM system prompt — does the LLM see the PHASE_ERROR in history and correctly reset?

**Scenario R: Persistent httpx Client After TEI Restart**
TEI crashes and restarts. The persistent `_http_client` singleton still holds HTTP/2 connection state to the old TEI process. Next embed request uses the stale client. What happens? Does httpx detect the broken connection and reconnect? Does it raise an exception that triggers the embed error handler? Or does it hang indefinitely?

**Scenario S: Race Between Ingestion and First Chat**
Fresh deployment. `ensure_qdrant_collection()` creates the collection at startup. Simultaneously, the V9 daemon fires `/api/ingest` for the first PDF. The ingest route calls `embed_text()` which hits TEI, then `index_chunk()` which calls `client.upsert()`. Meanwhile, a mechanic sends the first chat query. `hybrid_search()` queries the collection with `FusionQuery`. Qdrant has 10 partially-indexed chunks. Does `FusionQuery` work correctly on a collection being actively written to? Is there a consistency guarantee?

**Scenario T: DOMPurify Sanitization of Valid Diagnostic Content**
Qwen2.5 outputs `mechanic_instructions: "Check voltage at pin <B+> with multimeter. If >14V..."`. DOMPurify sees `<B+>` as an HTML tag. Does it strip it? Does it escape it as `&lt;B+&gt;`? The mechanic sees `Check voltage at pin  with multimeter` (content stripped) or `Check voltage at pin &lt;B+&gt;` (escaped but readable). Which behavior does DOMPurify exhibit? Is diagnostic content containing angle brackets common in automotive FSMs?

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P4-XX: [Title]
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
- [ ] No finding overlaps with the 52 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] All scenario traces (P through T) complete with predicted outcomes
- [ ] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [ ] Budget math independently computed for all edge-case scenarios
