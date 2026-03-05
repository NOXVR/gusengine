# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 3

## YOUR ROLE

You are a hostile production auditor performing **Phase 3** of a multi-pass audit. Phase 1 found 20 isolated execution bugs (missing try/except, wrong API names, ID collisions). Phase 2 found 15 cross-component interaction bugs (budget math divergence, missing imports, unbounded concurrency). All 35 findings have been patched.

**Your job is NOT to re-audit those 35 fixes.** Your job is to:

1. **Audit the Phase 2 fix code itself** — 15 new code additions were applied in Phase 2 without independent review. Several introduce non-trivial logic (eviction loops, semaphores, path validation, background error wrappers).
2. **Trace complete end-to-end data flows** — verify every variable is correctly threaded from HTTP request to HTTP response.
3. **Identify edge cases in the patched system** — the architecture has been heavily modified. Look for problems that only manifest in the *patched* version.

Phase 1 found the obvious. Phase 2 found the interactions. **You are looking for the edge cases, the off-by-ones, and the architectural gaps that only appear after 35 patches.**

---

## CUMULATIVE FIX CHANGELOG (DO NOT RE-AUDIT)

All findings below have been patched. Use this list to understand what changed, then look for **second-order defects in the fix code itself**.

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
| P2-03 | TOKENIZER import | Imported from `backend.inference.context` in `chat.py` |
| P2-04 | Shared qdrant_client | New `backend/shared/clients.py` singleton module |
| P2-05 | RETRIEVAL_FAILURE trigger | `RETRIEVED DOCUMENTS` header always present (with `[No documents retrieved]` placeholder) |
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

---

## PRESERVATION MANDATE (STILL IN EFFECT)

Every finding MUST be tagged with one of:
- `[ADDITIVE]` — adds new code, comments, config, documentation
- `[CORRECTIVE]` — modifies existing values, logic, or wording
- `[SUBTRACTIVE]` — removes ANY function, class, config block, security control, service, or framework component → **BLOCKED. Must include proof of breakage if retained.**

---

## AUDIT DIMENSIONS (PHASE 3 — EDGE CASES)

### Dimension 1: AUDIT THE AUDITORS' FIXES (Phase 2 Fix Code Review)

Phase 2 added 15 fixes. Many introduced non-trivial logic. Audit each fix *as code*:

1. **P2-02 — Chat history eviction loop:** The loop iterates `reversed(chat_history)` and calls `truncated.insert(0, msg)` for each kept message. `list.insert(0, ...)` is O(n) per call, making the entire eviction O(n²). At 100 messages, this is 10,000 operations per request. Is this a performance concern? Is there a correctness concern (e.g., does `reversed()` + `insert(0)` correctly preserve chronological order)?

2. **P2-04 — `qdrant_client` module-level instantiation:** `QdrantClient(url=...)` is instantiated at module import time in `backend/shared/clients.py`. What happens if Qdrant isn't running yet when the Python module loads? Does `QdrantClient()` make a connection attempt at construction time, or is it lazy? If eager, the backend crashes on import before healthchecks can even start.

3. **P2-11 — Path traversal via `os.path.realpath()`:** The fix canonicalizes the path and checks `startswith(ALLOWED_PDF_DIR)`. But `os.path.realpath()` resolves **symlinks**. Can an attacker create a symlink inside `/app/pdfs/` pointing to `/etc/shadow`? The resolved path would be `/etc/shadow`, which fails the `startswith` check — so this is safe. But what about **a symlink AT `/app/pdfs/` itself** pointing elsewhere? Does the Docker volume mount prevent this?

4. **P2-06 — `ingest_pdf_background()` error wrapper:** The wrapper writes to `/app/storage/extracted/.ingest_failures.log` using `open(..., "a")`. Is this file-append thread-safe? If two background tasks fail simultaneously, do their writes interleave? On Linux, POSIX guarantees atomic writes up to `PIPE_BUF` (4KB) for `O_APPEND` — are the log lines always under 4KB?

5. **DT-P2-04 — Ingestion semaphore placement:** The semaphore wraps `parse_and_chunk` but NOT `embed_text()` or `index_chunk()`. With 514 queued tasks and semaphore=2, at most 2 parse, but up to 512 tasks could be simultaneously calling `embed_text()` (HTTP POST to TEI). Does TEI handle 512 concurrent requests? Does httpx? Could this flood TEI and cause timeouts?

6. **P2-05 — `[No documents retrieved]` placeholder:** The placeholder text `[No documents retrieved]` is injected into the system prompt's RETRIEVED DOCUMENTS section. Could the LLM interpret this as an actual document title and try to cite it? Would it generate `"source": "[No documents retrieved]", "page": 1`?

7. **P2-09 — Text input toggle logic:** `hideInput = gus.requires_input && gus.answer_path_prompts && gus.answer_path_prompts.length > 0`. After a PHASE_ERROR (where `requires_input=false`), does the text input re-enable correctly? After PHASE_D (no `requires_input` or `answer_path_prompts` in the response), does the input state reset?

### Dimension 2: END-TO-END DATA FLOW INTEGRITY

Trace the **complete** happy-path data flow. Verify every variable name matches between producer and consumer:

1. **Frontend → Backend:** `sendMessage()` sends `{message: ..., chat_history: [...]}`. The backend reads `body["message"]` as `user_query` and `body.get("chat_history", [])`. Verify: does the frontend send `message` or `query`? Does `chat_history` contain `{role: "user"|"assistant", content: "..."}` format?

2. **Backend → vLLM:** `generate_response()` constructs `messages`. The `model` field is `"Qwen2.5-32B-Instruct-AWQ"`. The Docker `--served-model-name` is `Qwen2.5-32B-Instruct-AWQ`. Verify exact string match.

3. **vLLM → Backend → Frontend:** vLLM returns `response.json()["choices"][0]["message"]["content"]`. The backend wraps this in `{"response": response}`. The frontend calls `JSON.parse(data.response)`. Verify: is `response` always a valid JSON string? What if Qwen2.5 outputs malformed JSON?

4. **`build_context()` return type:** The signature says `-> tuple[str, list[dict]]` but the function is called as `context = build_context(...)` (single assignment). Does it return a tuple or a string? If it returns `(context_string, used_chunks)`, the `context` variable is a tuple, and `system_content += context` will fail with TypeError.

5. **`hybrid_search()` return type:** Returns `list[dict]` with key `token_count`. `build_context()` reads `chunk["token_count"]`. Verify: does the key name match between the Qdrant payload (`token_count`) and the consumer?

6. **`load_ledger()` return value:** Called in chat() as `ledger_text = load_ledger()`. If the ledger file is missing, what does it return? `None`? Empty string `""`? The downstream `if ledger_text:` check works for both, but `len(TOKENIZER.encode(None))` would crash.

### Dimension 3: DAG STATE MACHINE COMPLETENESS

The DAG state machine has a gap identified in Phase 2 Scenario J: **no transition rules for PHASE_ERROR**.

1. **PHASE_ERROR recovery:** After a PHASE_ERROR, the mechanic retries. `chat_history` now contains a PHASE_ERROR response. The system prompt's DAG matrix has no rule for "current_state = PHASE_ERROR, user sends new message." What does the LLM do? Is there a deterministic answer, or is it probabilistic?

2. **RETRIEVAL_FAILURE recovery:** Same gap — no transition out of RETRIEVAL_FAILURE.

3. **Frontend PHASE_ERROR handling:** Does `buildUserMessage()` inject `required_next_state` after a PHASE_ERROR? If it does, what value does it inject? If it doesn't, the LLM receives no state guidance.

4. **State accumulation in chat_history:** Over 25 turns,`chat_history` contains multiple state transitions. The LLM sees the full history of states. Can it get confused if it sees `PHASE_A → PHASE_B → PHASE_B → PHASE_ERROR → PHASE_A`? Does the system prompt handle this explicitly, or rely on LLM inference?

5. **`parseGusResponse()` robustness:** The function is described as "brute-force V9 heritage parser" but is not shown in full. What happens if vLLM returns a response starting with `Sure, here's the diagnostic:` followed by JSON? Does `parseGusResponse()` extract the JSON from arbitrary text? What if the JSON is truncated mid-object?

### Dimension 4: NUMERICAL VERIFICATION (Complete Budget Math)

Run the **full token budget calculation** with real numbers for three scenarios. Show your work.

**Scenario: First Request (no history, no ledger)**
```
max_context = 32768
system_prompt_tokens = 900
ledger_tokens = 0
response_budget = 2000
chat_history_tokens = 0
user_query_tokens = ~50 (short symptom)
available_for_RAG = ?
```
Verify: is the available RAG budget reasonable?

**Scenario: Typical mid-session request (ledger active, 10 turns)**
```
max_context = 32768
system_prompt_tokens = 900
ledger_tokens = 2550
response_budget = 2000
chat_history_tokens = ~5000 (10 turns × 500 tokens)
user_query_tokens = ~100
available_for_RAG = ?
```
Verify: is this enough for a useful diagnostic? How many 512-token chunks fit?

**Scenario: Cap-triggering long session (ledger active, 20+ turns)**
```
max_context = 32768
system_prompt_tokens = 900
ledger_tokens = 2550
response_budget = 2000
chat_history_tokens = 8000 (capped by eviction)
user_query_tokens = ~200 (detailed symptom)
available_for_RAG = ?
```
Verify: does `available_for_RAG` stay above `MIN_RAG_FLOOR=5000`? What happens if it doesn't? Does the code path handle underflow correctly?

**Also verify:** The `system_prompt_tokens=900` default. Count the approximate tokens in the full system prompt text (the DAG state machine document). Is 900 reasonable or is it significantly off?

### Dimension 5: COMPLETENESS OF SHOWN CODE

The architecture document is a *specification*, not a complete codebase. Some modules are fully shown, others are partially described. The following components are referenced but **not shown in full**:

1. **`parseGusResponse()`** — described as "brute-force V9 heritage parser" and "parses the raw LLM response string into a structured JSON object." Full implementation not shown. How does it handle markdown-wrapped JSON? Truncated JSON? Non-JSON responses?

2. **`buildUserMessage()`** — described as injecting `completed_state` and `required_next_state`. Full implementation not shown. What does it do after PHASE_ERROR? After PHASE_D?

3. **`sendMessage()`** — called by button click handlers. Not shown. Does it send via WebSocket or HTTP? Does it include the full `chat_history`?

4. **`load_ledger()`** — called in `chat()`. Not shown. What does it return when the file is missing? Does it cache the result or read from disk on every request?

5. **`validate_ledger.py`** — described as computing token budgets with `SAFETY_FACTOR=0.85` and `MIN_RAG_BUDGET=20000`. Not shown in full. Does it use the same TOKENIZER as the runtime? If it uses a different tokenizer, the validated budget won't match the actual budget.

For each, state whether the **absence of the full implementation** represents a risk. If the shown interface (signature + description) is sufficient to verify correctness, say so. If the hidden implementation could contain bugs that break the shown code, flag it.

### Dimension 6: DOCKER AND INFRASTRUCTURE EDGE CASES

1. **Container startup order:** `depends_on: condition: service_healthy` ensures containers start after deps are healthy. But `QdrantClient()` in `backend/shared/clients.py` is instantiated at module import time. If the backend container starts, Python imports the module, `QdrantClient()` tries to connect — does it fail if Qdrant's healthcheck hasn't passed yet? Or does `depends_on` guarantee Qdrant is ready before the backend even starts?

2. **TEI healthcheck accuracy:** The TEI healthcheck pings `/health`. Does TEI report healthy before it finishes loading the 2.3GB BGE-M3 model? If yes, the backend starts, sends an embed request, and gets a 503 (model loading). The error handler returns PHASE_ERROR, but the root cause is a startup race.

3. **Qdrant collection auto-creation:** The architecture shows `ensure_collection()` in `qdrant_setup.py`. When is this called? At backend startup? On first request? If the backend starts but `ensure_collection()` hasn't run, `hybrid_search()` queries a non-existent collection and crashes.

4. **Docker restart loops:** All containers have `restart: always`. If the backend crashes on startup (e.g., system prompt file missing → `SystemExit`), Docker restarts it immediately. Infinite restart loop. Does `SystemExit` vs `raise` matter for Docker's restart policy?

---

## SCENARIO TRACES (Phase 3 — Edge Cases)

**Scenario K: Eviction Edge Case — Single Massive Message**
A mechanic pastes a 9000-token symptom description as a single message. This single message exceeds `MAX_CHAT_HISTORY_TOKENS=8000`. Trace the eviction loop. Does it evict everything including the giant message? Does it keep nothing? Does it enter an infinite loop?

**Scenario L: build_context Return Type Mismatch**
Trace `context = build_context(results, ...)` through to `system_content += f"...\n\n{context}"`. If `build_context` returns a tuple `(str, list)`, what does `f"...\n\n{(context_string, [chunk1, chunk2])}"` produce? Is this caught before reaching vLLM?

**Scenario M: Concurrent Eviction + Token Counting**
Two chat requests arrive simultaneously. Both call `TOKENIZER.encode()` in the eviction loop. `TOKENIZER` is a module-level singleton imported from `context_builder.py`. Is `AutoTokenizer.encode()` safe to call concurrently from two coroutines on the same event loop (without `asyncio.to_thread`)?

**Scenario N: Ingestion Semaphore Starvation**
514 PDFs queued. Semaphore = 2. First PDF is a 600-page degraded scan, takes 10 hours. Second PDF is 2 pages, takes 30 seconds. After PDF #2 finishes, does PDF #3 start immediately? Or is the semaphore blocked until PDF #1 also finishes? What's the total ingestion time?

**Scenario O: LLM Returns Non-JSON**
Qwen2.5 ignores the JSON output instruction and returns: `"Based on the symptoms described, this could be a fuel delivery issue. Let me ask some clarifying questions:\n\n1. Does the engine crank?\n2. ..."`. Trace through `chat()` → frontend `parseGusResponse()`. What does the mechanic see? Is it graceful or a crash?

---

## OUTPUT FORMAT

For each finding, provide:

```
### FINDING-P3-XX: [Title]
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
- [ ] No finding overlaps with the 35 items in the cumulative fix changelog
- [ ] Every finding includes a concrete execution trace
- [ ] No `[SUBTRACTIVE]` finding without proof of breakage
- [ ] All 5 scenario traces complete with predicted outcomes
- [ ] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [ ] Token budget math independently computed for all 3 scenarios
