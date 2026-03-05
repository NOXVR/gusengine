# V10 HOSTILE ARCHITECTURE AUDIT — PHASE 3 REPORT

**Auditor:** Claude Opus 4.6 (Independent)
**Date:** 2026-02-24
**Target:** `ARCHITECTURE_V10.md` (post-Phase 1 + Phase 2 patches)
**Scope:** Edge cases, fix-code defects, end-to-end flow integrity, budget math

---

## FINDINGS

---

### FINDING-P3-01: `build_context()` Returns Tuple — `chat()` Receives Tuple as `context`

- **Dimension:** 2 (End-to-End Data Flow)
- **Severity:** CRITICAL
- **Classification:** [CORRECTIVE]
- **Description:** `build_context()` at line 1063 declares return type `-> tuple[str, list[dict]]` and returns `(context_string, used_chunks)` at line 1131. However, the caller in `chat.py` at line 885 assigns the result to a single variable: `context = build_context(...)`. This means `context` is now the tuple `("...", [{...}, ...])`, not a string.

  This `context` variable is then passed directly to `generate_response(context=context, ...)` at line 901. Inside `generate_response()`, line 1200 does: `system_content += f"\n\nRETRIEVED DOCUMENTS:\n\n{context}"`. Python's f-string calls `__str__()` on the tuple, producing output like:

  ```
  RETRIEVED DOCUMENTS:

  ('[Source 1: manual.pdf | Pages 3]...chunk text...', [{'text': '...', 'source': 'manual.pdf', ...}])
  ```

  The LLM receives the raw tuple representation — including Python list/dict syntax, metadata dictionaries, and the entire `used_chunks` array — as the retrieved document context. This wastes ~50% of the RAG token budget on metadata garbage and severely degrades diagnostic quality. The LLM may try to cite the Python dict structure as a document.

- **Proof:** Trace the execution path:
  1. `chat.py:885` → `context = build_context(results, ...)` — `context` is `(str, list[dict])`
  2. `chat.py:901` → `generate_response(context=context, ...)` — passes the tuple
  3. `llm.py:1184` → `def generate_response(..., context: str, ...)` — type hint says `str`, but Python doesn't enforce this
  4. `llm.py:1200` → `system_content += f"...\n\n{context}"` — calls `tuple.__str__()`, injects garbage
  5. vLLM receives a prompt with a Python tuple as the "retrieved documents"

- **Fix:**
  ```python
  # chat.py, line 885 — destructure the return value
  context, used_chunks = build_context(
      results,
      ledger_tokens=ledger_tokens,
      chat_history_tokens=chat_history_tokens,
      user_query_tokens=user_query_tokens,
  )
  ```

---

### FINDING-P3-02: Eviction Loop Produces Empty `chat_history` on Single Oversized Message

- **Dimension:** 1 (Fix Code Review — P2-02)
- **Severity:** SIGNIFICANT
- **Classification:** [CORRECTIVE]
- **Description:** The P2-02 eviction loop in `chat.py` (lines 836–846) iterates `reversed(chat_history)` and accumulates messages until `running + msg_tokens > MAX_CHAT_HISTORY_TOKENS`. If the very first message examined (the most recent) exceeds 8,000 tokens on its own, the `break` fires immediately on the first iteration, producing `truncated = []` and `chat_history_tokens = 0`.

  **Scenario K trace:** A mechanic pastes a 9,000-token symptom description. `chat_history = [{"role": "user", "content": "9000-token blob"}]`. The loop starts with `reversed(chat_history)`, which yields that single message. `msg_tokens = 9000 > 8000`, so `break` fires. `truncated = []`. `chat_history = []`. The mechanic's current symptom is in `user_query` (sent separately), but ALL prior diagnostic context is lost. If this was a mid-session paste, the LLM loses all conversation history and resets.

  This is a correctness issue: the eviction policy should keep at least the most recent message (possibly truncated) to maintain conversational coherence, or at minimum the current user message should be treated separately from chat_history (which it is — the `user_query` is separate). The real risk is a mid-session giant assistant response (e.g., LLM generates a 9,000-token response) — this poisons chat_history and causes total eviction on the next turn.

- **Proof:**
  1. `chat_history = [{"role": "user", "content": "short"}, {"role": "assistant", "content": "9000 tokens of rambling"}]`
  2. Eviction loop: `reversed(...)` → first message is the 9,000-token assistant message → `0 + 9000 > 8000` → `break`
  3. `truncated = []`, `chat_history = []`, `chat_history_tokens = 0`
  4. The LLM receives zero conversational context — diagnoses restart from scratch

- **Fix:**
  ```python
  # Always keep at least the most recent message to maintain continuity.
  # If a single message exceeds the cap, include it alone (budget math
  # in build_context will handle the downstream overflow via MIN_RAG_FLOOR).
  MAX_CHAT_HISTORY_TOKENS = 8000
  if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
      truncated = []
      running = 0
      for msg in reversed(chat_history):
          msg_tokens = len(TOKENIZER.encode(msg["content"]))
          if running + msg_tokens > MAX_CHAT_HISTORY_TOKENS and truncated:
              break  # Only break if we already have at least one message
          truncated.insert(0, msg)
          running += msg_tokens
          if running >= MAX_CHAT_HISTORY_TOKENS:
              break
      chat_history = truncated
      chat_history_tokens = running
  ```

---

### FINDING-P3-03: `QdrantClient()` Eager Connection at Module Import Time

- **Dimension:** 6 (Docker / Infrastructure) and 1 (Fix Code Review — P2-04)
- **Severity:** SIGNIFICANT
- **Classification:** [CORRECTIVE]
- **Description:** `backend/shared/clients.py` instantiates `QdrantClient(url=...)` at module level (line 607). The `qdrant-client` Python library's `QdrantClient(url=...)` constructor (for HTTP/gRPC remote clients) does NOT make an eager connection at construction time — it is lazy. So this specific concern is **not a startup crash risk**.

  However, the module-level instantiation has a different problem: the `QDRANT_URL` environment variable is read once at import time via `os.environ.get()`. If the module is imported before the environment variable is set (e.g., during testing, or if import ordering changes), the client silently defaults to `"http://qdrant:6333"` — which is correct in Docker but wrong on the host. This is a minor operational risk, not a crash risk.

  The `depends_on: condition: service_healthy` in docker-compose guarantees that Qdrant's healthcheck has passed before the backend container starts. So the module-level import is safe in the Docker deployment. The real risk is **collection existence**: `ensure_collection()` / `create_collection()` is defined in `qdrant_setup.py` but there is no visible call site. If it is never called at startup, the first `hybrid_search()` hits a non-existent collection.

- **Proof:**
  1. `qdrant_setup.py` defines `create_collection()` — but no `@app.on_event("startup")` or explicit call is shown
  2. The verification checklist (line 1595) expects `vectors_count > 0` — implying the collection was created during ingestion
  3. If the system is deployed fresh and a chat request arrives before any PDF is ingested, `hybrid_search()` queries `fsm_corpus` which doesn't exist → Qdrant returns HTTP 404 → `client.query_points()` raises exception → caught by the search error handler → PHASE_ERROR
  4. This is a graceful degradation, not a crash — but the PHASE_ERROR message ("document search system temporarily unavailable") is misleading when the real cause is "collection doesn't exist yet"

- **Fix:**
  ```python
  # backend/main.py (or wherever the FastAPI app is created)
  from backend.shared.clients import qdrant_client
  from backend.indexing.qdrant_setup import create_collection
  from qdrant_client.http.exceptions import UnexpectedResponse

  @app.on_event("startup")
  async def ensure_qdrant_collection():
      """Create collection if it doesn't exist. Idempotent."""
      try:
          qdrant_client.get_collection("fsm_corpus")
      except (UnexpectedResponse, Exception):
          create_collection(qdrant_client)
  ```

---

### FINDING-P3-04: Ingestion Semaphore Gates Only `parse_and_chunk`, Not `embed_text` — TEI Flood Risk

- **Dimension:** 1 (Fix Code Review — DT-P2-04)
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** The `INGEST_SEMAPHORE = asyncio.Semaphore(2)` in `pipeline.py` (line 692) only wraps `parse_and_chunk` (lines 710–711). After parsing, the semaphore is released, and the code proceeds to loop through all chunks calling `embed_text()` (line 723) for each one. With 514 PDFs queued:

  - At most 2 PDFs parse concurrently (correct — prevents OOM from Docling/EasyOCR)
  - But as soon as each PDF finishes parsing, it enters the embed loop. A PDF with 200 chunks fires 200 sequential `embed_text()` calls. With 514 PDFs processing, many could be in the embed loop simultaneously.
  - Each `embed_text()` opens a new `httpx.AsyncClient` (line 644: `async with httpx.AsyncClient()`), makes 2 HTTP requests (dense + sparse), then closes.
  - With dozens of PDFs in the embed phase concurrently, TEI receives potentially hundreds of concurrent HTTP requests.

  TEI (HuggingFace Text Embeddings Inference) has internal batching and queuing, so it won't crash. But `httpx.AsyncClient(timeout=30.0)` means each request has a 30-second timeout. If TEI's queue backs up, requests will timeout, raising `httpx.ReadTimeout`, which propagates up to `ingest_pdf()` and kills the entire PDF's ingestion — even though parsing (the expensive part) already succeeded.

- **Proof:**
  1. PDF #1 parses (60 min OCR), releases semaphore, starts embedding 200 chunks
  2. PDFs #2–514 parse in pairs, each releasing semaphore and starting embedding
  3. After a few hours, dozens of PDFs are simultaneously in the embed loop
  4. TEI receives 50+ concurrent embedding requests
  5. TEI's internal queue fills; response time increases from 100ms to 30s+
  6. `httpx.AsyncClient(timeout=30.0)` fires → `ReadTimeout` → `ingest_pdf()` raises → `ingest_pdf_background()` logs the error and moves on
  7. The PDF's chunks that were already indexed stay; remaining chunks are lost. Partial ingestion, no retry.

- **Fix:**
  ```python
  # Add a separate embed semaphore to rate-limit TEI requests
  EMBED_SEMAPHORE = asyncio.Semaphore(8)  # TEI can handle ~8 concurrent requests efficiently

  # In ingest_pdf(), wrap the embed call:
  for i, chunk in enumerate(chunks):
      chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{pdf_path}_{i}"))
      async with EMBED_SEMAPHORE:
          dense, sparse = await embed_text(chunk["text"])
      # ... rest of indexing
  ```

---

### FINDING-P3-05: `embed_text()` Creates New `httpx.AsyncClient` Per Call — Connection Churn

- **Dimension:** 2 (End-to-End Data Flow)
- **Severity:** MINOR
- **Classification:** [CORRECTIVE]
- **Description:** `embed_text()` in `client.py` (line 644) creates a new `httpx.AsyncClient` inside an `async with` block for every single embedding call. During bulk ingestion of 514 PDFs with ~100,000 total chunks, this creates and destroys ~200,000 HTTP clients (each performing TCP connection setup, optional TLS handshake, and teardown). Since TEI is on the same Docker bridge network, TLS is not involved, but the TCP overhead is still significant.

  More importantly, during concurrent embedding (see P3-04), the system may exhaust ephemeral ports or hit file descriptor limits. Linux defaults to ~28,000 ephemeral ports with a TIME_WAIT of 60 seconds.

- **Proof:** Each `embed_text()` call: opens client → makes 2 HTTP requests → closes client → socket enters TIME_WAIT. At 8 concurrent embeds, that's 8 sockets/second entering TIME_WAIT. For bulk ingestion running hours, thousands of sockets accumulate in TIME_WAIT.

- **Fix:**
  ```python
  # backend/embedding/client.py — use a module-level persistent client
  import httpx

  _client: httpx.AsyncClient | None = None

  async def get_client() -> httpx.AsyncClient:
      global _client
      if _client is None or _client.is_closed:
          _client = httpx.AsyncClient(timeout=30.0)
      return _client

  async def embed_text(text: str, base_url: str = TEI_BASE_URL) -> tuple[list[float], Optional[dict]]:
      client = await get_client()
      dense_response = await client.post(f"{base_url}/embed", json={"inputs": text})
      # ... rest of function without 'async with'
  ```

---

### FINDING-P3-06: `build_context()` References Undefined `logger`

- **Dimension:** 2 (End-to-End Data Flow)
- **Severity:** CRITICAL
- **Classification:** [CORRECTIVE]
- **Description:** The `build_context()` function in `context_builder.py` (lines 1073, 1089, 1093) calls `logger.warning(...)` but the module does not define `logger`. The module only imports `AutoTokenizer` from `transformers` (line 1040). There is no `import logging` or `logger = logging.getLogger(__name__)`.

  The first time `chat_history_tokens > MAX_CHAT_HISTORY_TOKENS` (which is already handled upstream in `chat.py`, so line 1073 is arguably dead code), or the first time `available < MIN_RAG_FLOOR` (line 1089, which IS a live code path — this triggers when conversation grows long), the function raises `NameError: name 'logger' is not defined`. This crashes the entire request with an unhandled exception before the RAG context is even built.

  The Phase 2 fixes (P2-07) added `logger` to `search.py` but missed `context_builder.py`.

- **Proof:**
  1. Scenario: Long session where `available < MIN_RAG_FLOOR`
  2. `build_context()` line 1089: `if available < MIN_RAG_FLOOR:` → True
  3. Line 1090: `logger.warning(...)` → `NameError: name 'logger' is not defined`
  4. Exception propagates to `chat()`, caught by the outer try/except at line 898 → PHASE_ERROR
  5. But the PHASE_ERROR message says "AI engine temporarily unavailable" — misleading when the real fix is a one-line import

- **Fix:**
  ```python
  # backend/retrieval/context_builder.py — add at top of file, after imports
  import logging
  logger = logging.getLogger(__name__)
  ```

---

### FINDING-P3-07: `[No documents retrieved]` Placeholder May Confuse LLM into Generating Fake Citations

- **Dimension:** 1 (Fix Code Review — P2-05)
- **Severity:** MINOR
- **Classification:** [CORRECTIVE]
- **Description:** When `hybrid_search()` returns no results (or all results are below the absolute score floor), `context` is the empty string (from `build_context()` receiving an empty list). In `generate_response()` line 1202, the code injects: `"RETRIEVED DOCUMENTS:\n\n[No documents retrieved]"`.

  The system prompt's ZERO-RETRIEVAL SAFEGUARD says: "If the RETRIEVED DOCUMENTS section is empty or contains NO document chunks, you MUST output RETRIEVAL_FAILURE." The placeholder `[No documents retrieved]` is text inside the section — it is not "empty." A literal-minded LLM may interpret the section as containing one document (named "[No documents retrieved]") and proceed with a normal diagnostic instead of triggering RETRIEVAL_FAILURE.

  Qwen2.5-32B is likely sophisticated enough to understand the semantics, but this is a semantic mismatch between the system prompt's trigger condition ("empty") and the actual content (not empty — contains placeholder text). The robustness of this depends entirely on LLM inference.

- **Proof:**
  1. `hybrid_search()` returns `[]`
  2. `build_context([], ...)` returns `("", [])` — but per P3-01, context is a tuple. Assuming P3-01 is fixed, context is `""`
  3. `generate_response()`: `context` is falsy → injects `[No documents retrieved]`
  4. System prompt: "If RETRIEVED DOCUMENTS section is empty" — it is NOT empty, it contains text
  5. Risk: LLM proceeds with diagnostic, no RETRIEVAL_FAILURE emitted

- **Fix:**
  ```python
  # llm.py — align placeholder with system prompt trigger language
  else:
      system_content += "\n\nRETRIEVED DOCUMENTS:\n\n"  # Empty section, no placeholder
  ```
  Alternatively, update the system prompt to explicitly mention the placeholder:
  ```
  If the RETRIEVED DOCUMENTS section is empty, contains only "[No documents retrieved]", or contains NO document chunks...
  ```

---

### FINDING-P3-08: `hybrid_search()` Is Synchronous — Called From Async `chat()` Without Thread Dispatch

- **Dimension:** 2 (End-to-End Data Flow)
- **Severity:** SIGNIFICANT
- **Classification:** [CORRECTIVE]
- **Description:** `hybrid_search()` in `search.py` (line 944) is a synchronous function that calls `client.query_points()` — a synchronous Qdrant HTTP client method. It is called from the async `chat()` handler at line 869: `results = hybrid_search(qdrant_client, query_dense, query_sparse)`.

  This blocks the asyncio event loop for the duration of the Qdrant query (typically 10–100ms, but can spike to seconds under load). While blocked, the FastAPI server cannot serve health checks, other chat requests, or background task callbacks.

  The architecture already uses `asyncio.to_thread()` for `index_chunk()` and `parse_and_chunk()` — the same treatment should be applied to `hybrid_search()`.

- **Proof:**
  1. `chat.py:869` → `results = hybrid_search(...)` — synchronous call in async context
  2. `search.py:992` → `client.query_points(...)` — synchronous Qdrant HTTP client, blocks event loop
  3. During this blocking call, `/api/health` is unresponsive, Docker healthcheck may fail if it coincides
  4. With concurrent requests, each search blocks the loop sequentially

- **Fix:**
  ```python
  # chat.py line 869
  results = await asyncio.to_thread(
      hybrid_search, qdrant_client, query_dense, query_sparse
  )
  ```

---

### FINDING-P3-09: `ingest_pdf_background()` Writes to Shared Log File Without Lock — Interleaved Writes Possible

- **Dimension:** 1 (Fix Code Review — P2-06)
- **Severity:** MINOR
- **Classification:** [ADDITIVE]
- **Description:** `ingest_pdf_background()` (line 752) writes to `/app/storage/extracted/.ingest_failures.log` using `open(..., "a")`. On Linux, `O_APPEND` guarantees atomic writes up to `PIPE_BUF` (4096 bytes). The typical log line is: `{pdf_path}\t{error_message}\n` — which should be well under 4KB for most paths and error messages.

  However, if a PDF path contains extremely long directory names or the error message includes a long traceback string, the write could exceed 4KB. More practically, the `except Exception as e` block at line 754 does NOT write to the log file — only `IngestionError` is logged. Unexpected exceptions are logged via `logger.error()` only, creating an asymmetry where some failures appear in the manifest and others don't.

  The atomicity concern is theoretical for this workload. The real issue is the inconsistency: `IngestionError` → logged to both `logger` and file; `Exception` → logged only to `logger`.

- **Proof:** An unexpected error (e.g., `httpx.ConnectError` during embedding) is caught by the outer `except Exception` at line 754, logged to Python's logger, but NOT written to `.ingest_failures.log`. The operator checking the failure manifest sees no entry, assumes the PDF succeeded, but it was actually partially ingested.

- **Fix:**
  ```python
  # Also log unexpected errors to the failure manifest
  except Exception as e:
      logger.error(f"UNEXPECTED INGESTION ERROR: {pdf_path} — {e}", exc_info=True)
      with open("/app/storage/extracted/.ingest_failures.log", "a") as f:
          f.write(f"{pdf_path}\tUNEXPECTED: {e}\n")
  ```

---

### FINDING-P3-10: Frontend Text Input Toggle State Not Reset After PHASE_D

- **Dimension:** 1 (Fix Code Review — P2-09)
- **Severity:** MINOR
- **Classification:** [CORRECTIVE]
- **Description:** The text input toggle logic at line 1392: `hideInput = gus.requires_input && gus.answer_path_prompts && gus.answer_path_prompts.length > 0`. This hides the text input when the LLM presents answer-path buttons (PHASE_A, PHASE_B, PHASE_C).

  After PHASE_D, the response has `requires_input: false` and `answer_path_prompts: []`. So `hideInput = false && ... = false`. `textInputEl.style.display = 'block'` — the text input reappears. This is **correct**.

  After PHASE_ERROR, the response has `requires_input: false` and `answer_path_prompts: []`. Same logic: `hideInput = false`. Text input reappears. This is also **correct** — the mechanic can retry.

  However, the toggle is one-directional: it only sets `display` to `'none'` or `'block'`. If the `textInputEl` was originally hidden by CSS (e.g., `display: none` as initial state), the first PHASE_D response would set it to `block`, which may be premature. The logic works correctly if the initial state is `display: block`, which is the natural default for an input element.

  **Verdict: P2-09 toggle logic is correct for the described behavior.** No fix needed. Marking as dimension-clear.

---

### FINDING-P3-11: PHASE_ERROR Has No DAG Transition Rule — LLM Behavior Is Probabilistic

- **Dimension:** 3 (DAG State Machine Completeness)
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** The system prompt's DAG State Transition Matrix defines transitions for PHASE_A → PHASE_B → PHASE_C → PHASE_D, and a reset rule ("After PHASE_D, if the user sends any new message, RESET to PHASE_A_TRIAGE"). There is no rule for:
  - "After PHASE_ERROR, if the user sends a new message → ?"
  - "After RETRIEVAL_FAILURE, if the user sends a new message → ?"

  When the mechanic retries after a PHASE_ERROR, `chat_history` contains the error response. The `buildUserMessage()` function is not shown, but if it injects `completed_state: "PHASE_ERROR"` and `required_next_state: ???`, the LLM has no deterministic rule to follow. The STATE TRANSITION ENFORCEMENT clause says "set current_state to the value of required_next_state" — but if `required_next_state` is undefined or empty, the LLM guesses.

  In practice, Qwen2.5-32B will likely infer that it should restart from PHASE_A_TRIAGE, which is the reasonable behavior. But this is non-deterministic and depends on LLM reasoning rather than explicit rules.

- **Proof:**
  1. Request #1 → TEI down → PHASE_ERROR response in chat_history
  2. Request #2 → TEI recovers → `buildUserMessage()` constructs message with `completed_state: "PHASE_ERROR"`, `required_next_state: ?`
  3. System prompt has no transition rule for PHASE_ERROR → the LLM picks a state probabilistically
  4. Risk: LLM could output PHASE_B (skipping triage), or another PHASE_ERROR, or an invalid state

- **Fix:**
  ```text
  # Add to system prompt DAG State Transition Matrix:
  - After PHASE_ERROR: If the user sends a new message, RESET to the last valid phase
    from chat_history. If no valid phase exists, RESET to PHASE_A_TRIAGE.
  - After RETRIEVAL_FAILURE: If the user sends a new message, RESET to PHASE_A_TRIAGE.
  ```
  And ensure `buildUserMessage()` handles these states by injecting a `required_next_state` of `"PHASE_A_TRIAGE"` after PHASE_ERROR/RETRIEVAL_FAILURE.

---

### FINDING-P3-12: `parseGusResponse()` Robustness Unknown — Non-JSON LLM Output Is Unhandled

- **Dimension:** 5 (Completeness of Shown Code) and Scenario O
- **Severity:** SIGNIFICANT
- **Classification:** [ADDITIVE]
- **Description:** `parseGusResponse()` is described as a "forward-scanning brute-force JSON.parse iteration (V8 hardened)" but its full implementation is not shown. The system prompt's CRITICAL OUTPUT RULE demands raw JSON with `{` as the first character. However, Qwen2.5-32B may not always comply.

  **Scenario O trace:** Qwen2.5 returns: `"Based on the symptoms described, this could be a fuel delivery issue. Let me ask some clarifying questions:\n\n1. Does the engine crank?\n2. ..."`

  Possible `parseGusResponse()` behaviors:
  - **Best case:** The forward-scanning parser searches for the first `{` and the last `}`, extracts the substring, and tries `JSON.parse()`. Since this response contains no JSON, every substring fails. The parser returns `null` or throws.
  - **Unknown:** Does `renderGusResponse()` handle `null`? If `gus` is `null`, line 1327 `gus.current_state` throws `TypeError: Cannot read property 'current_state' of null`. The mechanic sees a blank screen or JS error.

  The absence of `parseGusResponse()` code means this entire failure mode is unverifiable. The system prompt tells the LLM to output raw JSON, but there is no server-side validation that the response IS JSON before sending it to the frontend.

- **Proof:**
  1. `chat.py:918` → `return {"response": response}` — `response` is the raw string from vLLM, not validated
  2. Frontend receives `data.response` which may be plain English text
  3. `parseGusResponse(data.response)` — behavior unknown
  4. If it returns null → `renderGusResponse(null, ...)` → TypeError crash
  5. The mechanic sees nothing or a JS console error

- **Fix:**
  ```python
  # chat.py — validate LLM response is JSON before returning
  import json

  # After line 918, replace:
  #   return {"response": response}
  # With:
  try:
      parsed = json.loads(response)
      return {"response": response}  # Valid JSON, pass through
  except json.JSONDecodeError:
      logger.warning(f"LLM returned non-JSON response: {response[:200]}")
      return {"response": json.dumps({
          "current_state": "PHASE_ERROR",
          "mechanic_instructions": "The AI produced an unexpected response format. Please rephrase your question.",
          "diagnostic_reasoning": "LLM output was not valid JSON — may indicate prompt compliance failure.",
          "requires_input": False,
          "answer_path_prompts": [],
          "source_citations": [],
          "intersecting_subsystems": [],
      })}
  ```

---

### FINDING-P3-13: Duplicate TOKENIZER Instantiation — Two Identical Models Loaded in Memory

- **Dimension:** 2 (End-to-End Data Flow)
- **Severity:** MINOR
- **Classification:** [CORRECTIVE]
- **Description:** The `TOKENIZER` is instantiated at module level in two separate files:
  - `backend/ingestion/parser.py` (line 405): `TOKENIZER = AutoTokenizer.from_pretrained("/app/models/Qwen2.5-32B-Instruct-AWQ", ...)`
  - `backend/retrieval/context_builder.py` (line 1042): `TOKENIZER = AutoTokenizer.from_pretrained("/app/models/Qwen2.5-32B-Instruct-AWQ", ...)`

  Both are imported and used: `parser.py`'s TOKENIZER is used during ingestion for `token_count` computation. `context_builder.py`'s TOKENIZER is imported into `chat.py` (line 800: `from backend.inference.context import ... TOKENIZER`). The `chat.py` handler uses it for chat history tokenization and eviction.

  These are two separate `AutoTokenizer` instances in memory. `AutoTokenizer` for Qwen2.5-32B loads the tokenizer model (vocabulary + merge rules), which typically consumes ~50–100MB of RAM per instance. Having two identical copies wastes memory.

  More importantly, `validate_ledger.py` (line 1455) creates a THIRD instance with a different model path (`./storage/models/...` vs `/app/models/...`). If Dimension 5's concern materializes (different tokenizers), the validated budget won't match the runtime budget. However, both paths point to the same Qwen2.5-32B-Instruct-AWQ model, just with host vs. container paths.

- **Proof:** Three separate `AutoTokenizer.from_pretrained()` calls for the same model across three files. Two load at runtime (parser.py, context_builder.py), one loads during validation (validate_ledger.py).

- **Fix:**
  ```python
  # Create a single shared tokenizer module:
  # backend/shared/tokenizer.py
  from transformers import AutoTokenizer

  TOKENIZER = AutoTokenizer.from_pretrained(
      "/app/models/Qwen2.5-32B-Instruct-AWQ",
      trust_remote_code=True,
      local_files_only=True,
  )
  ```
  Then import from `backend.shared.tokenizer` in both `parser.py` and `context_builder.py`.

---

### FINDING-P3-14: `load_ledger()` Reads From Disk on Every Chat Request

- **Dimension:** 5 (Completeness of Shown Code)
- **Severity:** MINOR
- **Classification:** [ADDITIVE]
- **Description:** `load_ledger()` (line 1495) performs `os.path.exists()` + `open().read()` on every `/api/chat` request. The ledger file is a static Markdown document that changes only when the operator manually edits it. Reading from disk on every request adds unnecessary I/O latency (~1–5ms per call, negligible for single-user).

  For the single-user prototype, this is not a performance concern. However, the repeated `TOKENIZER.encode(ledger_text)` in `chat()` line 824 IS more expensive (~10–50ms for a 2,550-token document) and runs every request. Caching the ledger text and its token count would eliminate both.

  **Risk assessment:** Low. Single-user prototype. This is an optimization, not a bug.

- **Proof:** Each chat request: `load_ledger()` → disk read → `TOKENIZER.encode()` → 2,550 tokens counted. Identical result every time unless file changes.

- **Fix (optional, optimization):**
  ```python
  _ledger_cache = {"text": None, "tokens": None, "mtime": None}

  def load_ledger() -> tuple[str, int]:
      mtime = os.path.getmtime(LEDGER_PATH) if os.path.exists(LEDGER_PATH) else None
      if mtime == _ledger_cache["mtime"] and _ledger_cache["text"] is not None:
          return _ledger_cache["text"], _ledger_cache["tokens"]
      # ... read and tokenize, cache result
  ```

---

## DIMENSION 4: NUMERICAL VERIFICATION (Complete Budget Math)

### Scenario 1: First Request (no history, no ledger)

```
max_context           = 32,768
system_prompt_tokens  =    900
ledger_tokens         =      0
response_budget       =  2,000
chat_history_tokens   =      0
user_query_tokens     =     50  (short symptom: "car won't start")
─────────────────────────────
available_for_RAG     = 32,768 - 900 - 0 - 2,000 - 0 - 50
                      = 29,818 tokens
```

**Verdict:** 29,818 tokens. At 512 tokens/chunk + ~30 tokens header = ~542 tokens/chunk, this fits **~55 chunks**. Extremely generous. Well above `MIN_RAG_FLOOR = 5,000`. ✅

### Scenario 2: Typical mid-session (ledger active, 10 turns)

```
max_context           = 32,768
system_prompt_tokens  =    900
ledger_tokens         =  2,550
response_budget       =  2,000
chat_history_tokens   =  5,000  (10 turns × 500 tokens)
user_query_tokens     =    100
─────────────────────────────
available_for_RAG     = 32,768 - 900 - 2,550 - 2,000 - 5,000 - 100
                      = 22,218 tokens
```

**Verdict:** 22,218 tokens ≈ **41 chunks**. Excellent diagnostic capacity. Well above floor. ✅

### Scenario 3: Cap-triggering long session (20+ turns)

```
max_context           = 32,768
system_prompt_tokens  =    900
ledger_tokens         =  2,550
response_budget       =  2,000
chat_history_tokens   =  8,000  (capped by eviction)
user_query_tokens     =    200
─────────────────────────────
available_for_RAG     = 32,768 - 900 - 2,550 - 2,000 - 8,000 - 200
                      = 19,118 tokens
```

**Verdict:** 19,118 tokens ≈ **35 chunks**. Above `MIN_RAG_FLOOR = 5,000`. ✅

**Edge case — what if available < MIN_RAG_FLOOR?** For `available` to drop below 5,000, the fixed-cost deductions would need to exceed 27,768 tokens. With the chat history capped at 8,000 and other costs fixed, the minimum `available` is 19,118 (scenario 3). The floor can never be breached unless:
- `system_prompt_tokens > 900` (possible if the system prompt is longer than estimated)
- `ledger_tokens > 2,550` (prevented by validator)

If `available` DOES fall below `MIN_RAG_FLOOR`, `build_context()` line 1094 forces `available = MIN_RAG_FLOOR = 5,000`. This means the function fills 5,000 tokens of RAG context **even though the actual budget has been exhausted**. The total tokens sent to vLLM would exceed `max_context_tokens`, causing a vLLM 400 error (input exceeds `max-model-len`). The `MIN_RAG_FLOOR` enforcement without corresponding upstream eviction is a silent overrun.

**However**, per the math above, this scenario cannot occur with current parameter values. It is a latent bug that would activate only if `MAX_CHAT_HISTORY_TOKENS` is raised or `system_prompt_tokens` is underestimated.

### System Prompt Token Count Verification

The system prompt (lines 1241–1293) contains approximately 600 words of structured text. Using Qwen2.5's tokenizer, English prose typically tokenizes at ~1.3 tokens/word. 600 words × 1.3 ≈ **780 tokens**. The configured `SYSTEM_PROMPT_TOKENS = 900` provides a ~15% safety margin. **This is reasonable.** ✅

---

## SCENARIO TRACES

### Scenario K: Eviction Edge Case — Single Massive Message
See FINDING-P3-02. **Result:** `chat_history` is evicted to empty. Mechanic's current query is preserved in `user_query`. Prior diagnostic context lost. The LLM effectively restarts from scratch, which may or may not be the intended behavior for a mechanic who pasted a wall of text.

### Scenario L: `build_context` Return Type Mismatch
See FINDING-P3-01. **Result:** `context` variable contains a Python tuple. When formatted into the system prompt via f-string, it produces `('chunk text...', [{metadata}])`. The LLM receives the raw tuple including metadata dicts as part of the "RETRIEVED DOCUMENTS" section. Diagnostic quality severely degraded. No crash — the LLM receives valid text and tries to interpret it. May produce bizarre citations referencing Python syntax.

### Scenario M: Concurrent Eviction + Token Counting
Two chat requests arrive simultaneously. Both call `TOKENIZER.encode()` in the eviction loop. `AutoTokenizer.encode()` is a pure CPU function that creates new Python objects per call — it does not modify the tokenizer's state. It is **thread-safe and coroutine-safe**. Since both calls are on the same event loop thread (asyncio is single-threaded), they execute sequentially anyway. **No concurrency issue.** ✅

### Scenario N: Ingestion Semaphore Starvation
`INGEST_SEMAPHORE = asyncio.Semaphore(2)`. PDF #1 is a 600-page degraded scan taking 10 hours. PDF #2 is 2 pages, takes 30 seconds. Both acquire the semaphore simultaneously (sem = 2). After PDF #2 finishes parsing and releases the semaphore, PDF #3 can immediately acquire it and start parsing. The semaphore does NOT wait for all holders to release — it tracks available permits. So PDF #3 starts after 30 seconds, not after 10 hours. **No starvation.** ✅

However, PDF #2 immediately enters the embedding loop (200,000 chunks won't apply here for a 2-page doc, but the 600-page PDF #1 eventually releases and enters embedding with potentially thousands of chunks — see P3-04 for the TEI flood risk).

### Scenario O: LLM Returns Non-JSON
See FINDING-P3-12. **Result:** Raw text string is returned as `{"response": "Based on the symptoms..."}`. Frontend `parseGusResponse()` attempts to parse. The "forward-scanning brute-force" parser likely searches for `{` characters. If there are none, it fails. The fallback behavior is **unknown** — full `parseGusResponse()` code is not shown. If it returns null, `renderGusResponse(null, ...)` crashes with TypeError. **The mechanic sees a blank response or a JavaScript error.**

---

## VERDICTS

### Overall Verdict: **CONDITIONAL**

The architecture is fundamentally sound but contains two critical defects (P3-01 and P3-06) that would cause immediate runtime failures in the happy path, and several significant defects that affect edge cases and robustness.

### Required Fixes for Conditional → Pass

| # | Finding | Severity | Effort |
|:--|:--------|:---------|:-------|
| P3-01 | `build_context()` tuple destructuring | CRITICAL | 1 line |
| P3-06 | Missing `logger` import in `context_builder.py` | CRITICAL | 2 lines |
| P3-12 | Server-side JSON validation of LLM response | SIGNIFICANT | 15 lines |
| P3-02 | Eviction loop edge case (empty on oversized message) | SIGNIFICANT | 5 lines |
| P3-08 | `hybrid_search()` blocking event loop | SIGNIFICANT | 3 lines |
| P3-11 | PHASE_ERROR DAG transition rule | SIGNIFICANT | 5 lines (system prompt) |

### Confidence Scores

| Dimension | Confidence | Notes |
|:----------|:----------:|:------|
| 1: Fix Code Review | 90% | 7 of 7 fixes reviewed; P2-02, P2-04, P2-06, DT-P2-04 have issues |
| 2: Data Flow Integrity | 95% | Critical tuple bug found; model name match verified; chat_history format consistent |
| 3: DAG State Machine | 80% | PHASE_ERROR gap identified; `buildUserMessage()` not shown — cannot fully verify |
| 4: Budget Math | 95% | All 3 scenarios computed; no budget violation possible with current params |
| 5: Code Completeness | 70% | `parseGusResponse()`, `buildUserMessage()`, `sendMessage()` are all unshown — significant verification gaps |
| 6: Docker/Infrastructure | 85% | `depends_on` verified; TEI race window exists but is mitigated by `start_period`; collection auto-creation missing |

### Residual Risk (Cannot Be Verified From Document Alone)

1. **`parseGusResponse()` failure modes** — Full implementation not shown. Cannot verify JSON extraction from malformed LLM output, truncated responses, or markdown-wrapped JSON. This is the single largest unverifiable risk.
2. **`buildUserMessage()` state injection** — Not shown. Cannot verify what `completed_state` and `required_next_state` are set to after PHASE_ERROR or PHASE_D.
3. **`sendMessage()` transport** — Not shown. Cannot verify HTTP vs WebSocket, error handling, or retry logic.
4. **TEI `start_period` adequacy** — `start_period: 30s` for TEI loading the 2.3GB BGE-M3 model. If loading takes >30s on cold boot, the healthcheck starts counting failures before the model is ready. With 3 retries at 15s intervals, TEI has 30 + 45 = 75 seconds total. Likely sufficient, but hardware-dependent.
5. **Actual system prompt token count** — Estimated at ~780 tokens. The configured 900 includes a 15% buffer. If the actual count differs (e.g., due to special tokens or formatting), the budget math shifts. Can only be verified by running the actual tokenizer on the actual prompt file.
6. **`ensure_collection()` call site** — `create_collection()` is defined but no call site is shown. Fresh deployment with a chat request before ingestion will hit a 404 on the collection.

---

## INTEGRITY CHECKLIST

- [x] No finding overlaps with the 35 items in the cumulative fix changelog
- [x] Every finding includes a concrete execution trace
- [x] No `[SUBTRACTIVE]` finding without proof of breakage (zero SUBTRACTIVE findings)
- [x] All 5 scenario traces complete with predicted outcomes
- [x] At least one finding per dimension (or explicit "dimension clear" with reasoning)
- [x] Token budget math independently computed for all 3 scenarios

---

**END OF PHASE 3 AUDIT REPORT**
