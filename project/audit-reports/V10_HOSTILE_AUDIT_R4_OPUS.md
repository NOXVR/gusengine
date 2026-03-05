# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 4 REPORT
## Fix Interaction Analysis & Third-Order Effects

**Auditor:** Claude Opus 4.6 (Hostile Production Auditor)
**Date:** 2026-02-24
**Input:** `ARCHITECTURE_V10.md` (1803 lines), `V10_HOSTILE_AUDIT_PROMPT_R4.md` (253 lines)
**Scope:** Fix-on-fix conflicts, Phase 3 new code defects, residual hidden-code risk
**Prior Findings (Patched):** 52 (Phase 1: 20, Phase 2: 15, Phase 3: 17)

---

## FINDINGS

---

### FINDING-P4-01: Missing `import asyncio` in `chat.py` — First-Request Crash

- **Dimension:** 1 (Phase 3 Fix Code Review)
- **Severity:** CRITICAL
- **Classification:** [ADDITIVE]
- **Description:** P3-08 added `asyncio.to_thread(hybrid_search, ...)` at the search dispatch step in `chat.py` (line 936), but the module's import block (lines 852–860) does not include `import asyncio`. The first chat request that reaches the search step will raise `NameError: name 'asyncio' is not defined`, returning a raw 500 error to the mechanic. Every single chat request crashes.

- **Proof:** The `chat.py` import block as documented:
  ```python
  import json
  import os
  import logging
  from fastapi import APIRouter, Request
  from backend.embedding.client import embed_text
  from backend.search import hybrid_search
  from backend.inference.context import build_context, load_ledger, TOKENIZER
  from backend.inference.llm import generate_response
  from backend.shared.clients import qdrant_client
  ```
  Line 936 calls:
  ```python
  results = await asyncio.to_thread(
      hybrid_search, qdrant_client, query_dense, query_sparse
  )
  ```
  `asyncio` is not in scope. Python raises `NameError` before the try/except on line 932 can catch a search failure — the `NameError` occurs during *expression evaluation* of the `await` statement, which IS inside the try/except. Wait — let me re-examine: the `asyncio.to_thread` name resolution happens at call time, and it IS inside the `try: ... except Exception as e:` block on lines 932–949. So the NameError would be caught by the except clause and returned as PHASE_ERROR with `"Search error: NameError"`. This is not a raw 500 — it's a caught error. However, **every single chat request fails with PHASE_ERROR permanently** because the import is never resolved. The system is non-functional for chat.

- **Fix:** Add `import asyncio` to the import block in `chat.py`:
  ```python
  import asyncio
  import json
  import os
  import logging
  ```

---

### FINDING-P4-02: Budget Overflow When P3-02 Keeps Oversized Chat Message

- **Dimension:** 2 (Fix Interaction Matrix) / 4 (Numerical Verification)
- **Severity:** CRITICAL
- **Classification:** [CORRECTIVE]
- **Description:** P3-02 forces the eviction loop to keep at least one message, even if that message exceeds `MAX_CHAT_HISTORY_TOKENS=8000`. The `build_context()` function separately caps `chat_history_tokens` to 8000 for budget math. But the actual `chat_history` array still contains the oversized message. When `generate_response()` sends the array to vLLM, the real token count exceeds the budgeted amount, potentially pushing the total prompt past vLLM's `max_model_len=32768`.

- **Proof (Scenario P trace):**
  1. `chat_history = [{role: "user", content: <9000 tokens>}]`
  2. Eviction loop: `chat_history_tokens = 9000 > 8000`. Reversed iteration sees the user message (9000 tokens). `running=0`, `0 + 9000 > 8000` BUT `truncated` is empty — P3-02 guard prevents break. Message kept. `running=9000`.
  3. DT-P3-07: first message is "user" role — no strip.
  4. `chat_history_tokens = 9000` (actual).
  5. `build_context()` receives `chat_history_tokens=9000`, internally caps to `8000` for budget math.
  6. `available = 32768 - 900 - 2550 - 2000 - 8000 - 9999 = 9319` (using capped value).
  7. Context builder fills up to 9319 tokens of RAG context.
  8. Actual tokens sent to vLLM: `900 (system) + 2550 (ledger) + 9319 (RAG) + 9000 (actual chat) + 9999 (query) = 31768` input tokens.
  9. Plus `max_tokens=2000` response budget = **33768 total, exceeds 32768 by 1000 tokens**.
  10. vLLM returns HTTP 400 → caught by LLM error handler → PHASE_ERROR.

  The system doesn't crash catastrophically (error is caught), but the mechanic's valid query is rejected even though the budget math *said* it should fit. The overflow is silent — no log message explains why the "budgeted" prompt was rejected by vLLM.

- **Fix:** Enforce the cap on the actual `chat_history` array, not just the budget math. After the eviction loop completes, if `chat_history_tokens > MAX_CHAT_HISTORY_TOKENS`, force-truncate the oversized message's content to fit:
  ```python
  # After eviction loop and DT-P3-07 strip:
  if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS and len(chat_history) == 1:
      # P3-02 kept a single oversized message — truncate its content to budget
      msg = chat_history[0]
      tokens = TOKENIZER.encode(msg["content"])
      if len(tokens) > MAX_CHAT_HISTORY_TOKENS:
          truncated_tokens = tokens[:MAX_CHAT_HISTORY_TOKENS]
          msg["content"] = TOKENIZER.decode(truncated_tokens)
          chat_history_tokens = MAX_CHAT_HISTORY_TOKENS
          logger.warning(f"Truncated oversized chat message from {len(tokens)} to {MAX_CHAT_HISTORY_TOKENS} tokens")
  ```
  Alternatively, remove the cap in `build_context()` and let the *actual* token count flow through, accepting that RAG context shrinks proportionally. This is safer because the budget math then matches reality.

---

### FINDING-P4-03: P3-02 Bypass via DT-P3-07 — Eviction Can Empty Chat History

- **Dimension:** 2 (Fix Interaction Matrix)
- **Severity:** SIGNIFICANT
- **Classification:** [CORRECTIVE]
- **Description:** P3-02 guarantees the eviction loop keeps at least one message (`and truncated` guard prevents break on the first iteration). DT-P3-07 then strips a leading assistant message. If the *only* kept message is an assistant message, DT-P3-07 removes it, leaving `chat_history = []`. This defeats P3-02's intent.

- **Proof:**
  ```
  Input:  chat_history = [{role: "user", tokens: 9000}, {role: "assistant", tokens: 100}]
  Total:  9100 > 8000 → eviction runs
  Reversed iteration:
    1. assistant (100): running=0, 0+100 ≤ 8000 → add. truncated=[assistant], running=100
    2. user (9000): running=100, 100+9000=9100 > 8000, AND truncated is non-empty → break
  After loop: truncated = [{role: "assistant", tokens: 100}]
  DT-P3-07: truncated[0]["role"] == "assistant" → pop(0)
  Result:   chat_history = [], chat_history_tokens = 0
  ```
  P3-02's ≥1 message guarantee is violated. The mechanic's diagnostic context is completely lost.

- **Fix:** Move the DT-P3-07 assistant-strip check *before* the P3-02 re-check, or add a guard: if stripping the assistant message would empty the array, keep it and let the Qwen2.5 chat template handle the anomaly (a leading assistant message is unusual but not fatal — Qwen2.5 handles it via its default template behavior):
  ```python
  if truncated and truncated[0]["role"] == "assistant":
      if len(truncated) > 1:  # Only strip if it won't empty the history
          chat_history_tokens_removed = len(TOKENIZER.encode(truncated[0]["content"]))
          truncated.pop(0)
          running -= chat_history_tokens_removed
      else:
          logger.warning("Skipping assistant-strip: would empty chat history (P3-02 guard)")
  ```

---

### FINDING-P4-04: DOMPurify Strips Automotive Diagnostic Content Containing Angle Brackets

- **Dimension:** 3 (Frontend State Machine Consistency) / Scenario T
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** Automotive FSM documents commonly use angle-bracket notation for electrical references: `<B+>` (battery positive), `<GND>` (ground), `<S>` (switch), `<M>` (motor), etc. When Qwen2.5 outputs these in `mechanic_instructions`, DOMPurify interprets them as HTML tags. DOMPurify's default behavior strips unrecognized/malformed tags, causing silent content loss. The mechanic sees "Check voltage at pin  with multimeter" instead of "Check voltage at pin \<B+\> with multimeter."

  This is a **life-safety-adjacent content loss** — missing terminal designations in electrical diagnostic instructions could lead the mechanic to probe the wrong wire.

- **Proof (Scenario T trace):**
  ```
  LLM output: mechanic_instructions: "Check voltage at pin <B+> with multimeter. If >14V, replace regulator."
  DOMPurify.sanitize() parses "<B+>" as malformed HTML tag → strips it.
  innerHTML result: "Check voltage at pin  with multimeter. If >14V, replace regulator."
  ```
  Note: `>14V` survives because `>` is valid text content (only `<` starts a tag). But the `<B+>` designation is lost entirely. The mechanic has no idea which pin to probe.

- **Fix:** Configure DOMPurify to escape angle brackets in text content rather than strip them, or sanitize before DOMPurify by pre-escaping known automotive patterns:
  ```javascript
  // Option A: Use textContent instead of innerHTML for mechanic_instructions
  // (safest — no HTML parsing at all, but loses any intended formatting)
  instructions.textContent = gus.mechanic_instructions;

  // Option B: Pre-escape angle brackets before DOMPurify
  function escapeAngles(text) {
    return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  instructions.innerHTML = DOMPurify.sanitize(escapeAngles(gus.mechanic_instructions));

  // Option C: Configure DOMPurify to ALLOW_UNKNOWN_PROTOCOLS and use
  // RETURN_DOM_FRAGMENT with custom tag handling (most complex)
  ```
  **Recommendation:** Option A (`textContent`) for `mechanic_instructions` and `diagnostic_reasoning`. The LLM's JSON output schema specifies plain text, not HTML. Using `innerHTML` was never necessary — `textContent` is both XSS-safe and content-preserving. This eliminates the need for DOMPurify on these two fields entirely while keeping DOMPurify for any fields that genuinely need HTML rendering.

---

### FINDING-P4-05: Chat `embed_text()` Bypasses `EMBED_SEMAPHORE` — Priority Inversion During Ingestion

- **Dimension:** 2 (Fix Interaction Matrix)
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** P3-04's `EMBED_SEMAPHORE(8)` rate-limits TEI requests during ingestion, but the chat handler's `embed_text()` call (line 919) does not acquire the semaphore. During bulk ingestion (2 concurrent jobs × hundreds of chunks), all 8 semaphore permits may be held by ingestion tasks. A simultaneous chat request sends an unthrottled 9th embed request to TEI. If TEI is at capacity, the chat embed may time out (30s timeout on persistent client) or get a slow response, while ingestion tasks — which are background, lower-priority work — monopolize TEI.

- **Proof:**
  ```
  Ingestion task A: 200 chunks, iterating embed loop. Holds EMBED_SEMAPHORE permits (up to 8 concurrent).
  Ingestion task B: 200 chunks, also iterating.
  At any instant: up to 8 embed requests in-flight via EMBED_SEMAPHORE.
  
  Mechanic sends chat query → chat handler → embed_text(user_query).
  This call does NOT acquire EMBED_SEMAPHORE.
  TEI receives 9th concurrent request. TEI's internal queue depth exceeded → slow response or 503.
  Chat embed_text() blocks for up to 30s → mechanic sees long wait.
  ```

- **Fix:** Either (a) reserve one EMBED_SEMAPHORE permit for chat by reducing ingestion to `EMBED_SEMAPHORE(7)` and acquiring a permit in the chat path, or (b) give chat a separate semaphore with higher priority. The simpler fix:
  ```python
  # In chat.py, before embed_text call:
  from backend.ingestion.pipeline import EMBED_SEMAPHORE
  
  async with EMBED_SEMAPHORE:
      query_dense, query_sparse = await embed_text(user_query)
  ```
  This ensures chat competes fairly with ingestion rather than bypassing the rate limit. For true priority, reduce EMBED_SEMAPHORE to 7 and use a separate `CHAT_EMBED_SEMAPHORE(1)` that always has a reservation.

---

### FINDING-P4-06: `generate_response()` Creates Per-Call httpx Client (P3-05 Pattern Not Applied)

- **Dimension:** 1 (Phase 3 Fix Code Review)
- **Severity:** SIGNIFICANT
- **Classification:** [CORRECTIVE]
- **Description:** P3-05 replaced per-call `httpx.AsyncClient` instantiation in `embed_text()` with a persistent singleton to prevent ephemeral port exhaustion during bulk ingestion. However, `generate_response()` in `llm.py` (line 1318) still creates a new `httpx.AsyncClient` per call:
  ```python
  async with httpx.AsyncClient(timeout=120.0) as client:
  ```
  For single-user chat, this is less critical than the embed case (sequential requests, not concurrent). However, each client creation/teardown cycle leaves a TCP socket in TIME_WAIT state for ~60 seconds. During rapid-fire diagnostic sessions, dozens of TIME_WAIT sockets accumulate against the vLLM port.

- **Proof:** Mechanic sends 10 queries in 5 minutes. Each creates+destroys an httpx client. 10 TIME_WAIT sockets on port 8000. Not catastrophic for single-user, but inconsistent with the P3-05 rationale and would become a problem if chat were ever made concurrent (multi-user upgrade path).

- **Fix:** Apply the P3-05 persistent client pattern to `llm.py`:
  ```python
  _llm_client: httpx.AsyncClient | None = None

  async def _get_llm_client() -> httpx.AsyncClient:
      global _llm_client
      if _llm_client is None or _llm_client.is_closed:
          _llm_client = httpx.AsyncClient(timeout=120.0)
      return _llm_client
  ```

---

### FINDING-P4-07: `ensure_qdrant_collection()` Silently Fails — No Retry, No Block

- **Dimension:** 6 (Docker Infrastructure)
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** P3-03's startup hook catches all exceptions from `get_collection()` and falls through to `create_collection()`. But if `create_collection()` itself fails (Qdrant still initializing, TCP connected but persistence engine not ready), the exception propagates out of the `except` block. FastAPI's `@app.on_event("startup")` does not treat startup hook exceptions as fatal — the app launches anyway. All subsequent `/api/chat` requests hit a non-existent collection → `PHASE_ERROR` on every query until the operator manually restarts.

- **Proof:**
  ```
  Timeline:
  1. Qdrant container starts. Healthcheck passes (TCP port 6333 accepting connections).
  2. Backend container starts (depends_on: service_healthy).
  3. @app.on_event("startup") fires.
  4. get_collection("fsm_corpus") → Qdrant returns 503 (persistence loading) → exception caught.
  5. create_collection() → Qdrant returns 503 → exception NOT caught → propagates.
  6. FastAPI logs the error but continues startup.
  7. First /api/chat request → hybrid_search → client.query_points("fsm_corpus") → 404 → PHASE_ERROR.
  ```

- **Fix:** Add retry logic with backoff to the startup hook:
  ```python
  @app.on_event("startup")
  async def ensure_qdrant_collection():
      """Create collection if it doesn't exist. Retry on transient failure."""
      import asyncio
      for attempt in range(5):
          try:
              qdrant_client.get_collection("fsm_corpus")
              logger.info("Qdrant collection 'fsm_corpus' verified.")
              return
          except Exception:
              try:
                  create_collection(qdrant_client)
                  logger.info("Qdrant collection 'fsm_corpus' created.")
                  return
              except Exception as e:
                  logger.warning(f"Qdrant not ready (attempt {attempt+1}/5): {e}")
                  await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1, 2, 4, 8, 16s
      logger.critical("FATAL: Could not verify/create Qdrant collection after 5 attempts.")
      raise SystemExit("Qdrant collection setup failed — aborting startup.")
  ```

---

### FINDING-P4-08: Persistent httpx Client Does Not Detect Server-Side TCP Resets

- **Dimension:** 1 (Phase 3 Fix Code Review) / Scenario R
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** P3-05's `_get_client()` checks `_http_client.is_closed`, but this only detects explicit `.aclose()` calls. If TEI restarts (container crash + Docker restart), the server closes its end of the TCP connection. The persistent `httpx.AsyncClient` still holds a reference to the pooled connection. On the next embed request, httpx attempts to write to the dead socket.

  httpx's behavior on a dead connection: it detects the broken pipe at the transport layer and raises `httpx.ConnectError` or `httpx.RemoteProtocolError`. This IS caught by the embed error handler (`except Exception as e` on line 920) and returns PHASE_ERROR. The singleton survives — the next request creates a new connection in the pool automatically (httpx's connection pool handles this). So the failure is **transient** (one failed request, then recovery).

  However, if the TEI crash occurred during a bulk ingestion with 8 in-flight embed requests, all 8 fail simultaneously. The EMBED_SEMAPHORE releases 8 permits. The next 8 chunks all retry — but wait, there is no retry logic. Each failed embed means that chunk is silently skipped (the error propagates up to `ingest_pdf()`, which doesn't catch per-chunk embed failures).

- **Proof (Scenario R trace):**
  ```
  1. TEI crashes. Docker restarts TEI container (~30s to reload model).
  2. Persistent _http_client holds dead pooled connections.
  3. Next embed_text() call → httpx writes to dead socket → ConnectError raised.
  4. Chat path: caught by except block → PHASE_ERROR. Mechanic retries → TEI is back → success. ✓
  5. Ingestion path: ConnectError raised inside embed_text() → not caught in ingest_pdf()'s
     for-loop → propagates to ingest_pdf_background() → entire PDF marked as failed.
     All remaining chunks for that PDF are skipped.
  ```

- **Fix:** Add per-chunk error handling in the embed loop of `ingest_pdf()`:
  ```python
  for i, chunk in enumerate(chunks):
      chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{pdf_path}_{i}"))
      try:
          async with EMBED_SEMAPHORE:
              dense, sparse = await embed_text(chunk["text"])
      except Exception as e:
          logger.warning(f"Embed failed for chunk {i} of {pdf_path}: {e} — skipping chunk")
          continue  # Skip this chunk, don't fail the entire PDF
      # ... rest of indexing
  ```
  Additionally, consider adding a retry (1-2 attempts with backoff) before skipping.

---

### FINDING-P4-09: `validate_ledger.py` Uses Independent Tokenizer Instance (Not P3-13 Shared Module)

- **Dimension:** 5 (Residual Hidden Code Risk)
- **Severity:** MINOR
- **Classification:** [CORRECTIVE]
- **Description:** P3-13 created `backend/shared/tokenizer.py` as the single shared tokenizer instance. But `validate_ledger.py` (lines 1553–1565) instantiates its own `AutoTokenizer` from a different path (`MODEL_PATH` env var with fallback to `./storage/models/...`). The runtime tokenizer uses `/app/models/...` (container path). Both resolve to the same Qwen2.5-32B-Instruct-AWQ model, so token counts should match. However, the validator runs on the **host** (not in a container), and the runtime runs **in the container**. If the host's `transformers` library version differs from the container's, tokenization behavior could diverge, causing the validator to approve a ledger that's slightly over-budget at runtime (or vice versa).

- **Proof:** Host runs `transformers==4.38.0`. Container has `transformers==4.40.0`. A hypothetical tokenizer vocabulary change between versions causes a 2550-token ledger (at the cap) to count as 2548 on the host but 2552 in the container. The validator approves; the runtime slightly over-budgets the ledger. The effect is a ~2-token reduction in RAG budget — negligible. Risk is low but violates the P3-13 "single instance" design principle.

- **Fix:** Update `validate_ledger.py` to import from the shared module when running in-container, falling back to local instantiation for host usage:
  ```python
  try:
      from backend.shared.tokenizer import TOKENIZER
  except ImportError:
      # Running on host — instantiate locally
      TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True, local_files_only=True)
  ```

---

### FINDING-P4-10: P3-12 Passes Valid-but-Wrong-Schema JSON to Frontend

- **Dimension:** 1 (Phase 3 Fix Code Review) / 5 (Residual Hidden Code Risk)
- **Severity:** MINOR
- **Classification:** [ADDITIVE]
- **Description:** P3-12's server-side JSON validation uses `json.loads(response)` — checking syntactic validity only. If the LLM outputs valid JSON with wrong schema (e.g., `{"answer": "yes"}` instead of the DAG schema), it passes validation. The frontend's `parseGusResponse()` then receives an object missing `current_state`, `mechanic_instructions`, etc. The `renderGusResponse()` function checks each field with falsy guards (`if (gus.mechanic_instructions)`, `if (gus.source_citations)`), so missing fields are silently skipped — no crash. The state badge shows "undefined" (from `gus.current_state` being undefined), the text input is shown (fallthrough), and the mechanic sees a blank response with an "undefined" badge.

  This is ugly but not dangerous. The mechanic's instinct is to retry the query. However, for a "ZERO-TOLERANCE / LIFE-SAFETY ADJACENT" system, displaying "undefined" is unprofessional.

- **Fix:** Add a minimal schema check after `json.loads()`:
  ```python
  try:
      parsed = json.loads(response)
      if not isinstance(parsed, dict) or "current_state" not in parsed:
          raise ValueError("Missing required 'current_state' field")
  except (json.JSONDecodeError, ValueError):
      logger.warning(f"LLM returned invalid response schema: {response[:200]}")
      response = json.dumps({
          "current_state": "PHASE_ERROR",
          "mechanic_instructions": "The AI produced an unexpected response format. Please rephrase your question.",
          # ... standard PHASE_ERROR fields
      })
  ```

---

### FINDING-P4-11: P3-13 Tokenizer Import-Time Crash Gives Unhelpful Error

- **Dimension:** 1 (Phase 3 Fix Code Review)
- **Severity:** MINOR
- **Classification:** [ADDITIVE]
- **Description:** P3-13's `backend/shared/tokenizer.py` runs `AutoTokenizer.from_pretrained()` at module import time. If the model files are missing or corrupted (e.g., volume mount not configured, model not pre-downloaded), this raises `OSError` or `ValueError` during import. Since both `parser.py` and `context_builder.py` import from this module, and these are imported during FastAPI app setup, the error manifests as an `ImportError` with a nested `OSError` traceback pointing deep into the `transformers` library. P2-12 established the pattern of checking for missing files and raising `SystemExit` with a clear message — P3-13 doesn't follow this pattern.

- **Proof:**
  ```
  Model files missing at /app/models/Qwen2.5-32B-Instruct-AWQ.
  Import of backend.shared.tokenizer fails with:
    OSError: /app/models/Qwen2.5-32B-Instruct-AWQ is not a directory or does not exist.
  Import of backend.routes.chat fails with:
    ImportError: cannot import name 'TOKENIZER' from 'backend.shared.tokenizer'
  FastAPI startup fails with confusing traceback — operator has no clear guidance.
  ```

- **Fix:** Add a pre-check with clear error message matching the P2-12 pattern:
  ```python
  # backend/shared/tokenizer.py
  import os
  from transformers import AutoTokenizer

  _MODEL_PATH = "/app/models/Qwen2.5-32B-Instruct-AWQ"
  if not os.path.isdir(_MODEL_PATH):
      raise SystemExit(
          f"Fatal: tokenizer model directory not found at {_MODEL_PATH}. "
          f"Ensure model weights are pre-downloaded to ./storage/models/."
      )

  TOKENIZER = AutoTokenizer.from_pretrained(
      _MODEL_PATH, trust_remote_code=True, local_files_only=True,
  )
  ```

---

## SCENARIO TRACES

---

### Scenario P: Oversized Message Kept by P3-02 + User Query at Cap

**Input:**
```
max_context = 32768
system_prompt = 900
ledger = 2550
response_budget = 2000
chat_history = [{role: "user", content: <9000 tokens>}]  (P3-02 forces keep)
user_query = 9999 tokens (under DT-P3-03 cap of 10000)
```

**Trace:**
1. Eviction loop: 9000 > 8000 → iterates. P3-02 guard keeps the single message. `chat_history_tokens = 9000`.
2. DT-P3-07: first message is "user" → no strip.
3. DT-P3-03: 9999 < 10000 → passes.
4. `build_context()` receives `chat_history_tokens=9000`, internally caps to `8000`.
5. `available = 32768 - 900 - 2550 - 2000 - 8000 - 9999 = 9319`.
6. Context builder fills 9319 tokens of RAG context.
7. Actual tokens to vLLM: `900 + 2550 + 9319 + 9000 + 9999 = 31768` input.
8. `max_tokens=2000` → vLLM sees request for 33768 total context.
9. **vLLM rejects: 33768 > max_model_len=32768.** HTTP 400.
10. Caught by LLM error handler → PHASE_ERROR to mechanic.

**Prediction:** Functional failure (PHASE_ERROR), not crash. But the mechanic has no way to recover other than starting a new conversation. See FINDING-P4-02 for root cause and fix.

**Does MIN_RAG_FLOOR activate?** No. `available = 9319 > MIN_RAG_FLOOR(5000)`. MIN_RAG_FLOOR is unreachable with current caps: minimum `available = 32768 - 900 - 2550 - 2000 - 8000 - 10000 = 9318`, always above 5000.

---

### Scenario Q: PHASE_ERROR Accumulation in Chat History

**Input:**
```
User sends 10001-token query → DT-P3-03 rejects (PHASE_ERROR).
Frontend adds PHASE_ERROR response to chat_history.
User retries with 9999-token query.
Prior chat_history had 8000 tokens of existing conversation.
```

**Trace:**
1. DT-P3-03 rejects 10001-token query. Returns PHASE_ERROR JSON (~200 tokens).
2. Frontend adds the PHASE_ERROR to chat_history as `{role: "assistant", content: <~200 tokens>}`.
3. User retries. chat_history now has: prior messages (~8000 tokens) + PHASE_ERROR (~200 tokens) = ~8200 tokens.
4. Eviction loop: 8200 > 8000.
   - Reversed: PHASE_ERROR (200 tokens) → add first. `truncated=[PHASE_ERROR], running=200`.
   - Recent messages added in reverse until `running + next > 8000`.
   - Oldest messages evicted.
5. The PHASE_ERROR message IS evictable — it has no special protection. If it's the oldest, it gets evicted. If it's recent (which it is, being the most recent assistant message), it stays.
6. After eviction: ~8000 tokens retained, including the PHASE_ERROR.
7. DT-P3-07: if PHASE_ERROR ends up first → it's an assistant message → stripped. Otherwise preserved.
8. P3-11 DAG recovery: LLM sees PHASE_ERROR in history. System prompt says "After PHASE_ERROR, RESET to last valid phase." LLM correctly resets to the last valid phase from the remaining history.

**Prediction:** System recovers correctly. The PHASE_ERROR is either evicted (no effect) or seen by the LLM (which applies P3-11 recovery rules). No crash, no permanent corruption.

---

### Scenario R: Persistent httpx Client After TEI Restart

**Trace:**
1. TEI crashes. Docker `restart: always` restarts it. TEI takes ~30s to reload BGE-M3.
2. Persistent `_http_client` holds dead pooled TCP connections.
3. Chat request: `embed_text()` → httpx attempts POST on dead connection → transport error detected → `httpx.ConnectError` raised.
4. Error handler catches exception → PHASE_ERROR returned to mechanic.
5. httpx internally evicts the dead connection from its pool.
6. Mechanic retries after TEI is back up → `embed_text()` → httpx opens new connection → success.

**Prediction:** One transient PHASE_ERROR, then automatic recovery. The `_http_client` singleton does NOT need to be reset — httpx's connection pool self-heals. The `_get_client()` check for `is_closed` only matters if someone explicitly called `.aclose()`, which doesn't happen in this scenario.

**Concern:** httpx's default `keepalive_expiry=5.0` means idle connections are dropped after 5 seconds. If the dead connection was idle for >5s, it's already purged — no error at all. If the embed was in-flight when TEI crashed, the 30s timeout fires → exception → PHASE_ERROR. Both paths are handled.

---

### Scenario S: Race Between Ingestion and First Chat

**Trace:**
1. `ensure_qdrant_collection()` creates `fsm_corpus` at startup.
2. V9 daemon fires `/api/ingest` for first PDF → HTTP 202, background task starts.
3. Background task: `parse_and_chunk()` → takes 1-3 minutes for OCR.
4. Meanwhile, mechanic sends first chat query.
5. `hybrid_search()` → `client.query_points("fsm_corpus", ...)` → collection exists but has 0 points.
6. `results.points` is empty → function returns `[]`.
7. `build_context()` receives empty chunks → context is empty string.
8. `generate_response()` sends empty RETRIEVED DOCUMENTS section.
9. System prompt ZERO-RETRIEVAL SAFEGUARD activates → LLM outputs RETRIEVAL_FAILURE.
10. Frontend renders: "No matching documentation found. Please verify the vehicle details."

**Prediction:** Correct behavior. The mechanic is informed that no documentation is available. No crash. Once ingestion completes, subsequent queries find the indexed chunks.

**Sub-scenario:** Ingestion has partially completed (10 of 200 chunks indexed). Chat query arrives.
- Qdrant supports concurrent reads/writes — `query_points` during `upsert` is safe.
- FusionQuery operates on whatever points exist at query time (read snapshot).
- Results may be suboptimal (only 10 chunks to search) but functionally correct.

---

### Scenario T: DOMPurify Sanitization of Valid Diagnostic Content

**Trace:** See FINDING-P4-04 for full analysis.

**Prediction:** DOMPurify strips `<B+>`, `<GND>`, `<S>`, and similar angle-bracket automotive notations. Mechanic sees truncated instructions with missing terminal designations. This is content loss in life-safety-adjacent diagnostic instructions. DOMPurify's default `ALLOWED_TAGS` whitelist does not include arbitrary tags like `B+`, so they are stripped.

**Additional angle-bracket patterns common in automotive FSMs:**
- `<B+>` — battery positive terminal
- `<B->` — battery negative / ground
- `<S>` — switch terminal
- `<M>` — motor terminal
- `<30>`, `<15>`, `<50>` — DIN terminal designations
- `<R/W>` — wire color codes (Red/White)
- `>14V`, `<12V` — threshold comparisons (the `>` survives, the `<12V` is stripped)

The `<12V` case is particularly dangerous: DOMPurify sees `<12V>` as a tag if followed by `>` anywhere. The mechanic could see "If voltage " instead of "If voltage <12V, replace battery" — completely losing the diagnostic threshold.

---

## DIMENSION CONFIDENCE SCORES & VERDICTS

---

### Dimension 1: Phase 3 Fix Code Review
**Confidence:** 90%
**Findings:** P4-01 (CRITICAL), P4-06 (SIGNIFICANT), P4-08 (SIGNIFICANT), P4-10 (MINOR), P4-11 (MINOR)
**Assessment:** The new code introduced in Phase 3 has several defects. P4-01 (missing asyncio import) is the most severe — it renders chat non-functional. P4-06 and P4-08 are consistency gaps in the persistent client pattern.

### Dimension 2: Fix Interaction Matrix
**Confidence:** 92%
**Findings:** P4-02 (CRITICAL), P4-03 (SIGNIFICANT), P4-05 (SIGNIFICANT)
**Assessment:** The eviction trilogy (P3-02 + DT-P3-07 + P2-02) has two interaction defects: budget overflow (P4-02) and empty-history bypass (P4-03). The embed semaphore has a priority inversion (P4-05). These are the third-order effects that Phase 4 was designed to catch.

### Dimension 3: Frontend State Machine Consistency
**Confidence:** 75%
**Findings:** P4-04 (SIGNIFICANT), P4-10 (MINOR, shared with Dim 1)
**Assessment:** The frontend is largely consistent after 52 fixes. The major remaining risk is DOMPurify's content-stripping behavior (P4-04). The `renderGusResponse()` function handles missing fields gracefully via falsy checks. `buildUserMessage()` behavior with PHASE_ERROR as `lastResponse` remains unverifiable from the document — see Residual Risk.

### Dimension 4: Numerical Verification
**Confidence:** 95%
**Findings:** P4-02 (CRITICAL, shared with Dim 2)
**Assessment:** Budget math is correct for nominal scenarios. The overflow only occurs in the specific P3-02 oversized-message edge case. MIN_RAG_FLOOR is unreachable with current caps. All three scenarios (P, Q, R) traced to completion.

### Dimension 5: Residual Hidden Code Risk
**Confidence:** 70%
**Findings:** P4-09 (MINOR), P4-10 (MINOR, shared)

| Component | Risk Rating | Justification |
|:----------|:-----------|:-------------|
| `parseGusResponse()` | **LOW** | Forward-scanning JSON parser. P3-12 ensures syntactically valid JSON reaches it. Wrong-schema JSON degrades to blank response (P4-10), not crash. |
| `buildUserMessage()` | **HIGH** | Unverifiable from document. Its behavior with PHASE_ERROR as `lastResponse` determines whether DAG recovery works. If it lacks a default case for unknown states, it could inject conflicting `required_next_state`. |
| `load_ledger()` | **LOW** | Reads from disk every request, but single-user air-gapped system means no concurrent writes. Partial read during manual edit is theoretically possible but operationally negligible. |
| `validate_ledger.py` | **MEDIUM** | Uses independent tokenizer (P4-09). Low probability of divergence with same model, but violates P3-13 design principle. |

### Dimension 6: Docker Infrastructure
**Confidence:** 85%
**Findings:** P4-07 (SIGNIFICANT)
**Assessment:** The startup sequence is fragile: `ensure_qdrant_collection()` doesn't retry/block on failure (P4-07). TEI restart scenario recovers gracefully (Scenario R). Container restart cleans up in-process state (semaphores, httpx clients).

---

## OVERALL VERDICT

### **CONDITIONAL PASS**

The system is functional for the happy path but has two CRITICAL defects that must be fixed before deployment:

**Required fixes (blocking deployment):**
1. **P4-01:** Add `import asyncio` to `chat.py` — without this, chat is completely non-functional.
2. **P4-02:** Fix budget overflow when P3-02 keeps oversized messages — either truncate the actual message content or let the real token count flow through budget math.

**Strongly recommended fixes (not blocking but high-impact):**
3. **P4-04:** Switch `mechanic_instructions` and `diagnostic_reasoning` to `textContent` instead of `innerHTML` to prevent DOMPurify from stripping automotive angle-bracket content. This is a life-safety-adjacent content loss.
4. **P4-07:** Add retry logic to `ensure_qdrant_collection()` startup hook.
5. **P4-03:** Guard DT-P3-07 against emptying chat history.

---

## RESIDUAL RISK (Unverifiable from Document)

1. **`buildUserMessage()` with PHASE_ERROR:** The function's implementation is not shown. Its behavior with non-standard `current_state` values (PHASE_ERROR, RETRIEVAL_FAILURE) determines whether DAG recovery works or enters an undefined state. **Recommendation:** Include the full implementation in the architecture document for audit, or write unit tests covering PHASE_ERROR → recovery transitions.

2. **`parseGusResponse()` extraction logic:** Described as "forward-scanning brute-force" but not shown. If it extracts the first `{...}` object greedily, it works. If it has schema expectations, malformed-but-valid JSON may fail. **Risk:** Low (P3-12 and P4-10 mitigate).

3. **Qdrant FusionQuery behavior with single prefetch:** When sparse vectors are unavailable (DT-8 fallback), only the dense prefetch is sent. Whether Qdrant's RRF fusion degrades correctly to single-signal ranking (effectively just dense cosine similarity) is undocumented. **Risk:** Low (Qdrant documentation confirms single-prefetch is valid).

4. **vLLM behavior at exactly 32768 tokens:** Whether vLLM counts tokens identically to the Qwen2.5 AutoTokenizer (used in budget math) depends on whether vLLM uses the same tokenizer internally. Any off-by-one difference in token counting could cause silent truncation or 400 errors at the boundary. **Risk:** Low (vLLM uses the model's bundled tokenizer, which is the same AutoTokenizer).

---

## INTEGRITY CHECKLIST

- [x] No finding overlaps with the 52 items in the cumulative fix changelog
- [x] Every finding includes a concrete execution trace
- [x] No `[SUBTRACTIVE]` finding without proof of breakage (zero SUBTRACTIVE findings)
- [x] All scenario traces (P through T) complete with predicted outcomes
- [x] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [x] Budget math independently computed for all edge-case scenarios

**Total Phase 4 findings: 11** (2 CRITICAL, 6 SIGNIFICANT, 3 MINOR)
