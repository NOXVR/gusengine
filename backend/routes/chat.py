# backend/routes/chat.py
# V10 SPEC: Full chat orchestration — DAG, ledger, budget, JSON validation
# V10 FIREWALL: Vehicle-scoped collection routing, identity swap, scoped ledger
# V11 MULTI-PASS: Internal self-verification before response delivery
# V12 COGNITIVE QUERY EXPANSION: Pre-retrieval mechanic reasoning
import asyncio
import hashlib
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor  # AUDIT FIX (P6-05)
import logging
from fastapi import APIRouter, Request
from backend.embedding.client import embed_text
from backend.search.hybrid_search import hybrid_search
from backend.search.context_builder import build_context
from backend.shared.tokenizer import TOKENIZER, count_tokens, _TOKENIZER_LOCK
from backend.inference.llm import generate_response
from backend.shared.clients import qdrant_search_client
from backend.routes.vehicle import get_vehicle, get_default_vehicle_id, get_all_vehicles
from backend.routes.vehicle_linter import lint_vehicle_mismatch

logger = logging.getLogger(__name__)

# AUDIT FIX (P6-05): Dedicated thread pool for chat-path search.
# The default ThreadPoolExecutor is shared with ingestion's index_chunk() calls.
# This dedicated pool guarantees chat search always has threads available.
_SEARCH_POOL = ThreadPoolExecutor(max_workers=4, thread_name_prefix="chat-search")

# AUDIT FIX (P9-02): Read budget env vars. Docker Compose or RunPod sets these.
_MAX_CONTEXT_TOKENS = int(os.environ.get("MAX_CONTEXT_TOKENS", "32768"))
_SYSTEM_PROMPT_TOKENS = int(os.environ.get("SYSTEM_PROMPT_TOKENS", "900"))
_RESPONSE_BUDGET_TOKENS = int(os.environ.get("RESPONSE_BUDGET_TOKENS", "2000"))

router = APIRouter()

# AUDIT FIX (P2-12): Explicit startup failure instead of confusing ImportError
_PROMPT_PATH = os.environ.get("SYSTEM_PROMPT_PATH", "/app/config/system_prompt.txt")
if os.path.exists(_PROMPT_PATH):
    with open(_PROMPT_PATH) as f:
        _BASE_SYSTEM_PROMPT = f.read()
else:
    logger.critical(f"SYSTEM PROMPT NOT FOUND: {_PROMPT_PATH}")
    raise SystemExit(f"Fatal: system prompt missing at {_PROMPT_PATH}")

# AUDIT FIX (P8-09): Verify system prompt token count at startup.
_actual_prompt_tokens = count_tokens(_BASE_SYSTEM_PROMPT)
_configured_prompt_tokens = int(os.environ.get("SYSTEM_PROMPT_TOKENS", "900"))
if _actual_prompt_tokens > _configured_prompt_tokens:
    logger.critical(
        f"System prompt ({_actual_prompt_tokens} tokens) exceeds configured budget "
        f"({_configured_prompt_tokens}). Update SYSTEM_PROMPT_TOKENS env var."
    )
    raise SystemExit(f"System prompt exceeds token budget: {_actual_prompt_tokens} > {_configured_prompt_tokens}")

# V10 FIREWALL: For backward compat, keep SYSTEM_PROMPT as a public name
SYSTEM_PROMPT = _BASE_SYSTEM_PROMPT

# V11 MULTI-PASS: Load verification prompt for internal self-check.
# Feature flag: ENABLE_VERIFICATION=true enables Pass 2 verification.
_ENABLE_VERIFICATION = os.environ.get("ENABLE_VERIFICATION", "true").lower() == "true"
_VERIFICATION_PROMPT_PATH = os.environ.get(
    "VERIFICATION_PROMPT_PATH", "/app/config/verification_prompt.txt"
)
_VERIFICATION_PROMPT = ""
if os.path.exists(_VERIFICATION_PROMPT_PATH):
    with open(_VERIFICATION_PROMPT_PATH) as f:
        _VERIFICATION_PROMPT = f.read()
    logger.info(
        f"V11 MULTI-PASS: Verification prompt loaded ({count_tokens(_VERIFICATION_PROMPT)} tokens), "
        f"enabled={_ENABLE_VERIFICATION}"
    )
else:
    if _ENABLE_VERIFICATION:
        logger.warning(
            f"V11 MULTI-PASS: Verification enabled but prompt not found at "
            f"{_VERIFICATION_PROMPT_PATH} — falling back to single-pass"
        )
        _ENABLE_VERIFICATION = False

# V12 COGNITIVE QUERY EXPANSION: Load expansion prompt for pre-retrieval reasoning.
# Feature flag: ENABLE_QUERY_EXPANSION=true enables Pass 0 query expansion.
_ENABLE_QUERY_EXPANSION = os.environ.get("ENABLE_QUERY_EXPANSION", "true").lower() == "true"
_EXPANSION_PROMPT_PATH = os.environ.get(
    "QUERY_EXPANSION_PROMPT_PATH", "/app/config/query_expansion_prompt.txt"
)
_EXPANSION_PROMPT = ""
if os.path.exists(_EXPANSION_PROMPT_PATH):
    with open(_EXPANSION_PROMPT_PATH) as f:
        _EXPANSION_PROMPT = f.read()
    logger.info(
        f"V12 EXPANSION: Query expansion prompt loaded ({count_tokens(_EXPANSION_PROMPT)} tokens), "
        f"enabled={_ENABLE_QUERY_EXPANSION}"
    )
else:
    if _ENABLE_QUERY_EXPANSION:
        logger.warning(
            f"V12 EXPANSION: Enabled but prompt not found at "
            f"{_EXPANSION_PROMPT_PATH} — falling back to single-query"
        )
        _ENABLE_QUERY_EXPANSION = False

# Ledger loading
# V10 FIREWALL: LEDGER_DIR is the base directory; vehicle-scoped filenames are resolved at runtime.
LEDGER_DIR = os.path.dirname(os.environ.get("LEDGER_PATH", "/app/config/MASTER_LEDGER.md"))


def _build_vehicle_prompt(vehicle: dict) -> str:
    """Swap the identity line in the system prompt for the active vehicle.

    V10 FIREWALL: The base prompt is vehicle-agnostic except for line 1
    (YOUR IDENTITY). At request time, we replace it with the vehicle's
    identity string from the registry.
    """
    lines = _BASE_SYSTEM_PROMPT.split("\n")
    # Line 1 is the YOUR IDENTITY line — replace it
    if lines and lines[0].startswith("YOUR IDENTITY:"):
        lines[0] = f"YOUR IDENTITY: {vehicle['identity']}"
    else:
        # Fallback: prepend identity if format changed
        lines.insert(0, f"YOUR IDENTITY: {vehicle['identity']}")
    return "\n".join(lines)


def load_ledger(vehicle: dict | None = None) -> str:
    """Load pinned ledger for injection into system prompt context.

    V10 FIREWALL: If a vehicle is provided, load its scoped ledger file.
    Falls back to the default MASTER_LEDGER.md for backward compat.
    """
    if vehicle:
        ledger_path = os.path.join(LEDGER_DIR, vehicle.get("ledger_filename", "MASTER_LEDGER.md"))
    else:
        ledger_path = os.path.join(LEDGER_DIR, "MASTER_LEDGER.md")
    if os.path.exists(ledger_path):
        with open(ledger_path, 'r') as f:
            return f.read()
    return ""


def _make_phase_error(instructions: str, reasoning: str) -> dict:
    """Helper to build consistent PHASE_ERROR responses."""
    return {"response": json.dumps({
        "current_state": "PHASE_ERROR",
        "mechanic_instructions": instructions,
        "diagnostic_reasoning": reasoning,
        "requires_input": False,
        "answer_path_prompts": [],
        "source_citations": [],
        "intersecting_subsystems": [],
    })}


def _strip_llm_fences(raw: str) -> str:
    """Strip markdown fences and <think> blocks from LLM output."""
    # Normalize line endings — LLM may return \r\n, \r, or \n
    s = raw.replace('\r\n', '\n').replace('\r', '\n').strip()
    s = re.sub(r'<think>.*?</think>', '', s, flags=re.DOTALL)
    # Strip opening fence: ```json or ``` at start
    s = re.sub(r'^```(?:json)?\s*\n?', '', s.strip())
    # Strip closing fence: ``` (may not be at absolute end if LLM appends text)
    s = re.sub(r'\n```\s*(?:\n.*)?$', '', s, flags=re.DOTALL)
    return s.strip()


def _extract_json(raw: str) -> dict | None:
    """Parse JSON from LLM output, with balanced-brace recovery and truncation handling."""
    stripped = _strip_llm_fences(raw)
    if not stripped:
        return None

    # Direct parse
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, dict):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    # Balanced-brace extraction (P5-03)
    for i in range(len(stripped)):
        if stripped[i] == '{':
            depth = 0
            for j in range(i, len(stripped)):
                if stripped[j] == '{':
                    depth += 1
                elif stripped[j] == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            parsed = json.loads(stripped[i:j + 1])
                            if isinstance(parsed, dict):
                                return parsed
                        except (json.JSONDecodeError, ValueError):
                            pass
                        break

    # V11 FIX: Handle truncated JSON (max_tokens cut off mid-response).
    # Find the first '{' and try to close unclosed braces/brackets.
    first_brace = stripped.find('{')
    if first_brace >= 0:
        fragment = stripped[first_brace:]
        # Count unclosed braces and brackets
        open_braces = fragment.count('{') - fragment.count('}')
        open_brackets = fragment.count('[') - fragment.count(']')
        # Strip any trailing incomplete string (cut after last comma or colon)
        # Find last complete key-value pair
        repair = fragment.rstrip()
        # Remove trailing partial content after last comma
        for trim_char in [',', ':', '"']:
            last_pos = repair.rfind(trim_char)
            if last_pos > 0:
                test = repair[:last_pos].rstrip()
                # Close it up
                closure = ']' * max(0, open_brackets) + '}' * max(0, open_braces)
                try:
                    parsed = json.loads(test + closure)
                    if isinstance(parsed, dict):
                        logger.info(f"V11 FIX: Recovered truncated JSON (trimmed at '{trim_char}', added {len(closure)} closers)")
                        return parsed
                except (json.JSONDecodeError, ValueError):
                    continue

    return None


async def _expand_queries(user_query: str) -> tuple[list[str], dict]:
    """V12 COGNITIVE QUERY EXPANSION: Generate subsystem-targeted search queries.

    Pass 0: Before touching the vector DB, ask the LLM to reason about what
    physical systems could produce the reported symptoms, then generate
    5 targeted search queries — one per subsystem.

    IMPORTANT: This uses a DEDICATED LLM call — NOT generate_response().
    generate_response() injects "RETRIEVED DOCUMENTS:" sections and forces
    response_format: json_object. Both corrupt the expansion output:
    - json_object mode constrains output to {} objects — bare JSON arrays [] are rejected
    - The empty RETRIEVED DOCUMENTS section triggers diagnostic-mode reasoning
    The expansion needs a clean prompt → JSON array response, nothing else.

    Returns tuple of:
      - list: original query + expanded queries (6 total)
      - dict: metadata about the expansion (method, query_count, queries)
    Falls back to [user_query] if expansion fails.
    """
    if not _ENABLE_QUERY_EXPANSION or not _EXPANSION_PROMPT:
        return [user_query], {"method": "disabled", "query_count": 1, "queries": [user_query]}

    t0 = time.monotonic()
    try:
        # Direct LLM call — bypass generate_response() entirely
        from backend.inference.llm import _get_llm_client, _flush_llm_client, VLLM_BASE_URL, VLLM_MODEL
        client = await _get_llm_client()
        payload = {
            "model": VLLM_MODEL,
            "messages": [
                {"role": "system", "content": _EXPANSION_PROMPT},
                {"role": "user", "content": user_query},
            ],
            "max_tokens": 512,
            "temperature": 0.3,
            # NO response_format — we need a bare JSON array, not a json_object
        }
        response = await client.post(f"{VLLM_BASE_URL}/chat/completions", json=payload)
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.warning(f"V12 EXPANSION: LLM call failed ({type(e).__name__}), using original query")
        return [user_query], {"method": "llm_error", "error": str(e), "query_count": 1, "queries": [user_query]}
    elapsed = time.monotonic() - t0
    logger.info(f"V12 EXPANSION raw ({elapsed:.1f}s, {len(raw)} chars): {raw[:500]}")

    # Normalize line endings before any parsing
    raw_clean = raw.replace('\r\n', '\n').replace('\r', '\n')

    # Parse the JSON array of queries — multiple extraction strategies
    stripped = _strip_llm_fences(raw_clean)

    # Build candidate strings to try parsing
    candidates = [stripped]

    # Strategy 2: Balanced-bracket extraction — walk from first '[' counting
    # depth to find the exact matching ']'. rfind(']') fails when the LLM
    # appends commentary containing brackets after the JSON array.
    bracket_start = stripped.find("[")
    if bracket_start >= 0:
        depth = 0
        in_string = False
        escape_next = False
        for i in range(bracket_start, len(stripped)):
            c = stripped[i]
            if escape_next:
                escape_next = False
                continue
            if c == '\\':
                escape_next = True
                continue
            if c == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    candidates.append(stripped[bracket_start:i + 1])
                    break

    for candidate in candidates:
        try:
            queries = json.loads(candidate)
            if isinstance(queries, list) and len(queries) >= 3 and all(isinstance(q, str) for q in queries):
                all_queries = [user_query] + queries[:5]
                method = "balanced_bracket" if candidate != stripped else "json_parse"
                logger.info(
                    f"V12 EXPANSION ({method}): Generated {len(queries)} queries in {elapsed:.1f}s: "
                    + " | ".join(q[:60] for q in queries[:5])
                )
                return all_queries, {"method": method, "query_count": len(all_queries), "queries": all_queries, "time": round(elapsed, 1)}
        except (json.JSONDecodeError, ValueError):
            continue

    # Strategy 3: Regex fallback — extract quoted strings directly.
    # Handles cases where trailing commas or minor formatting breaks JSON.
    quoted = re.findall(r'"([^"]{10,})"', stripped)
    if len(quoted) >= 3:
        queries = quoted[:5]
        all_queries = [user_query] + queries
        logger.info(
            f"V12 EXPANSION (regex_fallback): Extracted {len(queries)} queries in {elapsed:.1f}s: "
            + " | ".join(q[:60] for q in queries)
        )
        return all_queries, {"method": "regex_fallback", "query_count": len(all_queries), "queries": all_queries, "time": round(elapsed, 1)}

    logger.warning(f"V12 EXPANSION: Failed to parse queries ({elapsed:.1f}s), using original: {raw[:500]}")
    return [user_query], {"method": "fallback_original", "query_count": 1, "queries": [user_query], "time": round(elapsed, 1), "raw_preview": raw[:200]}


async def _verify_diagnostic(
    draft_json: str,
    user_query: str,
    context: str,
) -> dict | None:
    """V11 MULTI-PASS: Run internal verification against the diagnostic draft.

    Pass 2: Feeds the draft back to the LLM with the verification prompt.
    Returns the verification result dict, or None if verification is disabled
    or the verification call fails.
    """
    if not _ENABLE_VERIFICATION or not _VERIFICATION_PROMPT:
        return None

    # Build the verification input: draft + original complaint + RAG context
    verification_input = (
        f"CUSTOMER COMPLAINT:\n{user_query}\n\n"
        f"DIAGNOSTIC DRAFT (Gus's Pass 1 output):\n{draft_json}\n\n"
        f"RAG CONTEXT (retrieved FSM documents):\n{context}"
    )

    t0 = time.monotonic()
    try:
        raw_response = await generate_response(
            system_prompt=_VERIFICATION_PROMPT,
            context="",  # Context is embedded in the user message
            user_message=verification_input,
            chat_history=[],  # No history for verification pass
            max_tokens=4096,  # V11 FIX: 2000 was truncating the 4-check output
        )
    except Exception as e:
        logger.warning(f"V11 verification call failed ({type(e).__name__}), skipping verification")
        return None
    elapsed = time.monotonic() - t0

    logger.info(
        f"V11 VERIFY raw response: len={len(raw_response)}, "
        f"starts='{raw_response[:80]}...', ends='...{raw_response[-80:]}'"
    )

    result = _extract_json(raw_response)
    if result is None:
        logger.warning(
            f"V11 verification returned non-JSON (len={len(raw_response)}), "
            f"skipping: {raw_response[:300]}"
        )
        return None

    passed = result.get("verification_passed", True)
    revision_required = result.get("revision_required", False)
    checks = result.get("checks", {})

    # Log the full structure of what the LLM returned for debugging
    logger.info(f"V11 VERIFY response keys: {list(result.keys())}")

    # Log individual check results — handle various LLM response formats
    check_summary = []
    if isinstance(checks, dict) and checks:
        for check_name, check_data in checks.items():
            if isinstance(check_data, dict):
                check_passed = check_data.get("passed", True)
                status = "PASS" if check_passed else "FAIL"
                check_summary.append(f"{check_name}={status}")
                # Log details for failed checks
                if not check_passed:
                    details = {k: v for k, v in check_data.items() if k != "passed"}
                    logger.warning(f"V11 CHECK FAILED [{check_name}]: {json.dumps(details, default=str)[:500]}")
                else:
                    logger.info(f"V11 CHECK PASSED [{check_name}]")
            else:
                # LLM returned a non-dict value for this check
                check_summary.append(f"{check_name}={check_data}")
                logger.info(f"V11 CHECK [{check_name}]: {check_data}")
    else:
        logger.warning(
            f"V11 VERIFY: 'checks' field missing or not a dict. "
            f"Type={type(checks).__name__}, raw_keys={list(result.keys())}"
        )

    summary_str = ", ".join(check_summary) if check_summary else "no-checks-found"

    # Log revision instructions if any
    rev_instructions = result.get("revision_instructions", "")
    rev_note = f", revision_note='{rev_instructions[:100]}'" if rev_instructions else ""

    logger.info(
        f"V11 VERIFY SUMMARY: passed={passed}, revision={revision_required}, "
        f"checks=[{summary_str}], latency={elapsed:.1f}s{rev_note}"
    )
    return result


async def _revise_diagnostic(
    system_prompt: str,
    context: str,
    user_query: str,
    chat_history: list[dict],
    verification_result: dict,
    max_tokens: int,
) -> str | None:
    """V11 MULTI-PASS: Pass 3 — regenerate with verification feedback.

    Appends the verification findings to the RAG context so the model
    knows what it got wrong on the first pass.
    """
    revision_instructions = verification_result.get("revision_instructions", "")
    if not revision_instructions:
        return None

    # Build revision context: original RAG + what went wrong
    checks = verification_result.get("checks", {})
    failed_checks = []
    for check_name, check_data in checks.items():
        if isinstance(check_data, dict) and not check_data.get("passed", True):
            failed_checks.append(f"- {check_name}: {json.dumps(check_data, indent=2)}")

    revision_context = (
        f"{context}\n\n"
        f"--- INTERNAL VERIFICATION FEEDBACK (DO NOT SHOW TO USER) ---\n"
        f"Your previous diagnostic draft FAILED internal verification.\n"
        f"You MUST correct the following issues:\n\n"
        f"{revision_instructions}\n\n"
        f"Failed checks:\n{''.join(failed_checks)}\n\n"
        f"Generate a CORRECTED diagnostic response that addresses ALL flagged issues.\n"
        f"--- END VERIFICATION FEEDBACK ---"
    )

    t0 = time.monotonic()
    try:
        response = await generate_response(
            system_prompt=system_prompt,
            context=revision_context,
            user_message=user_query,
            chat_history=chat_history,
            max_tokens=max_tokens,
        )
    except Exception as e:
        logger.error(f"V11 revision call failed ({type(e).__name__}), returning original draft")
        return None
    elapsed = time.monotonic() - t0
    logger.info(f"V11 REVISE: Pass 3 completed in {elapsed:.1f}s")
    return response


@router.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_query = body.get("message", body.get("query", ""))
    if not user_query or not isinstance(user_query, str) or not user_query.strip():
        return _make_phase_error(
            "Please enter a symptom or question to begin diagnosis.",
            "Empty or missing query."
        )

    # V10 FIREWALL: Resolve active vehicle from request (default: Mercedes)
    vehicle_id = body.get("vehicle_id", get_default_vehicle_id())
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        return _make_phase_error(
            f"Unknown vehicle: {vehicle_id}. Select a valid vehicle from the dropdown.",
            f"Vehicle ID '{vehicle_id}' not found in registry."
        )
    active_collection = vehicle["collection"]
    logger.info(f"Chat request for vehicle '{vehicle_id}' → collection '{active_collection}'")

    # AUDIT FIX (P7-15): Validate chat_history schema before processing.
    raw_history = body.get("chat_history", [])
    if not isinstance(raw_history, list):
        raw_history = []
    chat_history = []
    for m in raw_history:
        if (isinstance(m, dict)
            and isinstance(m.get("content"), str)
            and m.get("content").strip()            # AUDIT FIX (P8-07)
            and m.get("role") in ("user", "assistant")):
            chat_history.append(m)
        else:
            logger.warning(f"Malformed chat_history entry dropped: {type(m)}")

    # Step 1: Load vehicle-scoped ledger (may be empty if file missing — degrades gracefully)
    ledger_text = load_ledger(vehicle)
    ledger_tokens = count_tokens(ledger_text) if ledger_text else 0

    # AUDIT FIX (P7-11): Runtime ledger cap enforcement.
    LEDGER_MAX_TOKENS = int(os.environ.get("LEDGER_MAX_TOKENS", "2550"))
    if ledger_tokens > LEDGER_MAX_TOKENS:
        logger.warning(
            f"Ledger ({ledger_tokens} tokens) exceeds cap ({LEDGER_MAX_TOKENS}). "
            f"Truncating to cap. Run validate_ledger.py to resize."
        )
        with _TOKENIZER_LOCK:
            ledger_text = TOKENIZER.decode(TOKENIZER.encode(ledger_text)[:LEDGER_MAX_TOKENS])
        # AUDIT FIX (P8-04): Re-count after decode — round-trip can change token count
        ledger_tokens = count_tokens(ledger_text)
        if ledger_tokens > LEDGER_MAX_TOKENS:
            with _TOKENIZER_LOCK:
                ledger_text = TOKENIZER.decode(TOKENIZER.encode(ledger_text)[:LEDGER_MAX_TOKENS - 10])
            ledger_tokens = count_tokens(ledger_text)

    # Step 2: Compute chat history token cost
    chat_history_tokens = sum(
        count_tokens(m["content"]) for m in chat_history
    )

    # AUDIT FIX (P2-02): Physically truncate chat_history array to match budget cap.
    MAX_CHAT_HISTORY_TOKENS = 8000
    # AUDIT FIX (P8-03): Cap message count to prevent framing token overflow.
    MAX_CHAT_HISTORY_MESSAGES = 40
    if len(chat_history) > MAX_CHAT_HISTORY_MESSAGES:
        chat_history = chat_history[-MAX_CHAT_HISTORY_MESSAGES:]
        chat_history_tokens = sum(count_tokens(m["content"]) for m in chat_history)
    # AUDIT FIX (DT-P10-04): Strip leading orphan assistant messages GLOBALLY.
    while chat_history and chat_history[0]["role"] == "assistant":
        removed = count_tokens(chat_history[0]["content"])
        chat_history.pop(0)
        chat_history_tokens -= removed
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        truncated = []
        running = 0
        for msg in reversed(chat_history):
            msg_tokens = count_tokens(msg["content"])
            if running + msg_tokens > MAX_CHAT_HISTORY_TOKENS and truncated:
                break
            truncated.insert(0, msg)
            running += msg_tokens
        # AUDIT FIX (DT-P3-07 + P6-02): Strip ALL leading orphan assistant messages
        while truncated and truncated[0]["role"] == "assistant":
            chat_history_tokens_removed = count_tokens(truncated[0]["content"])
            truncated.pop(0)
            running -= chat_history_tokens_removed
        chat_history = truncated
        chat_history_tokens = running

    # AUDIT FIX (P6-01): Hard budget enforcement after eviction.
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        return _make_phase_error(
            "Your conversation history is too large. Please start a new diagnostic session.",
            f"Chat history ({chat_history_tokens} tokens) exceeds {MAX_CHAT_HISTORY_TOKENS}-token limit after eviction."
        )

    # AUDIT FIX (DT-P6-02): Query length validation moved ABOVE embed call.
    user_query_tokens = count_tokens(user_query)
    MAX_USER_QUERY_TOKENS = 8000
    if user_query_tokens > MAX_USER_QUERY_TOKENS:
        return _make_phase_error(
            "Your message is too long for me to process. Please shorten your question or paste smaller sections of diagnostic data.",
            f"User query ({user_query_tokens} tokens) exceeds {MAX_USER_QUERY_TOKENS}-token safety limit."
        )

    # VEHICLE MISMATCH FIREWALL: Pre-LLM query linter.
    # Runs BEFORE embedding/search/LLM — zero cost if mismatch detected.
    # [BYPASS_VEHICLE_CHECK] prefix = user acknowledged the mismatch and chose to continue.
    bypass_vehicle_check = user_query.startswith("[BYPASS_VEHICLE_CHECK]")
    if bypass_vehicle_check:
        user_query = user_query.replace("[BYPASS_VEHICLE_CHECK]", "").strip()
        logger.info("Vehicle mismatch bypass acknowledged by user")
    
    if not bypass_vehicle_check:
        mismatch = lint_vehicle_mismatch(user_query, vehicle, get_all_vehicles())
        if mismatch:
            logger.warning(f"Vehicle mismatch firewall triggered: {mismatch['detail']}")
            return {"response": json.dumps({
                "current_state": "VEHICLE_MISMATCH",
                "mechanic_instructions": mismatch["warning"],
                "diagnostic_reasoning": mismatch["detail"],
                "detected_vehicle": mismatch["detected"],
                "detected_terms": mismatch["detected_terms"],
                "active_vehicle": mismatch["active"],
                "requires_input": False,
                "answer_path_prompts": [],
                "source_citations": [],
                "intersecting_subsystems": [],
            })}

    # V12 COGNITIVE QUERY EXPANSION: Generate expanded search queries (Pass 0)
    search_queries, expansion_info = await _expand_queries(user_query)
    expansion_active = len(search_queries) > 1

    # AUDIT FIX (H09/H10/H13): Comprehensive error handling for embed → search → generate
    try:
        # Step 3: Embed queries for retrieval
        # AUDIT FIX (P4-05 + P7-05): Acquire EMBED_SEMAPHORE with timeout
        from backend.ingestion.pipeline import _get_embed_semaphore
        _embed_sem = await _get_embed_semaphore()
        try:
            await asyncio.wait_for(_embed_sem.acquire(), timeout=5.0)
        except asyncio.TimeoutError:
            raise RuntimeError("Embedding service at capacity — all permits held by ingestion")
        try:
            # V12: Parallel embedding of all queries
            embed_tasks = [embed_text(q) for q in search_queries]
            embed_results = await asyncio.gather(*embed_tasks)
        finally:
            _embed_sem.release()
    except Exception as e:
        logger.error(f"Embedding failed: {e}", exc_info=True)
        return _make_phase_error(
            "The search system is temporarily unavailable. Please try again in a moment.",
            f"Embedding service error: {type(e).__name__}"
        )

    try:
        # Step 4: Hybrid search (dense + sparse with RRF fusion)
        # V12: Run parallel searches for each expanded query
        loop = asyncio.get_event_loop()
        per_query_top_k = 20 if expansion_active else 60

        async def _search_one(dense, sparse, query_text):
            return await loop.run_in_executor(
                _SEARCH_POOL,
                lambda: hybrid_search(
                    qdrant_search_client, dense, sparse,
                    top_k=per_query_top_k,
                    collection_name=active_collection,  # V10 FIREWALL
                ),
            )

        search_tasks = [
            _search_one(er[0], er[1], sq)  # embed_text returns (dense, sparse) tuple
            for er, sq in zip(embed_results, search_queries)
        ]
        all_search_results = await asyncio.gather(*search_tasks)

        # V12: Deduplicate and merge results across all queries
        if expansion_active:
            seen_hashes = set()
            merged = []
            per_query_counts = []
            for i, query_results in enumerate(all_search_results):
                count = 0
                for chunk in query_results:
                    chunk_hash = hashlib.md5(chunk["text"][:200].encode()).hexdigest()
                    if chunk_hash not in seen_hashes:
                        seen_hashes.add(chunk_hash)
                        merged.append(chunk)
                        count += 1
                per_query_counts.append(count)
            # Sort by score descending, take top 60
            merged.sort(key=lambda c: c["score"], reverse=True)
            results = merged[:60]
            logger.info(
                f"V12 EXPANSION SEARCH: {len(search_queries)} queries → "
                f"{sum(per_query_counts)} unique chunks (per-query: {per_query_counts}), "
                f"merged to {len(results)}"
            )
        else:
            results = all_search_results[0] if all_search_results else []
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        return _make_phase_error(
            "The document search system is temporarily unavailable. Please try again in a moment.",
            f"Search error: {type(e).__name__}"
        )

    # Step 5: Build RAG context within token budget
    # AUDIT FIX (P3-01): build_context() returns tuple[str, list[dict]].
    # AUDIT FIX (P7-03): build_context() raises ValueError if budget exhausted.
    try:
        context, used_chunks = build_context(
            results,
            max_context_tokens=_MAX_CONTEXT_TOKENS,
            system_prompt_tokens=_SYSTEM_PROMPT_TOKENS,
            response_budget=_RESPONSE_BUDGET_TOKENS,
            ledger_tokens=ledger_tokens,
            chat_history_tokens=chat_history_tokens,
            user_query_tokens=user_query_tokens,
            chat_history_message_count=len(chat_history),
        )
    except ValueError as e:
        logger.warning(f"Context budget exhausted: {e}")
        return _make_phase_error(
            "Your conversation history is too large for me to include enough reference material. Please start a new diagnostic session.",
            str(e)
        )

    # LAYER 1 FIX: Backend RETRIEVAL_FAILURE enforcement.
    # The LLM should NEVER decide whether retrieval failed — the backend decides.
    # If Qdrant returned chunks but none survived context budgeting, or if search
    # returned nothing, we short-circuit here BEFORE calling the LLM.
    if not used_chunks:
        logger.warning(
            f"RETRIEVAL_FAILURE (backend-enforced): search returned {len(results)} chunks, "
            f"0 survived context budgeting for query: {user_query[:100]}"
        )
        return {
            "response": json.dumps({
                "current_state": "RETRIEVAL_FAILURE",
                "mechanic_instructions": (
                    "I don't have FSM documentation covering this specific topic for your vehicle. "
                    "This means either the Factory Service Manual doesn't include a procedure for this, "
                    "or the search couldn't find a strong enough match. "
                    "Try rephrasing with more specific symptoms — describe what you hear, see, or feel."
                ),
                "diagnostic_reasoning": (
                    f"Hybrid search returned {len(results)} raw chunks but 0 survived "
                    f"context budgeting. This indicates a genuine FSM content gap for this topic."
                ),
                "requires_input": False,
                "answer_path_prompts": [],
                "source_citations": [],
                "intersecting_subsystems": [],
            }),
            "rag_context": {
                "chunk_count": 0,
                "total_tokens_used": 0,
                "sources": [],
            },
        }

    # Step 6: Assemble system prompt WITH ledger (injection point)
    # V10 FIREWALL: Swap identity line for the active vehicle
    system_prompt = _build_vehicle_prompt(vehicle)
    if ledger_text:
        system_prompt += f"\n\nMASTER_LEDGER.md:\n{ledger_text}"

    # CUSTOMER VEHICLE: Inject modification context if this is a VIN-scoped vehicle
    customer_vin = vehicle.get("_customer_vin")
    if customer_vin:
        from backend.db import format_modifications_context
        mod_context = format_modifications_context(customer_vin)
        if mod_context:
            system_prompt += f"\n\n---\nSOURCE: Vehicle Modification Records (NOT from FSM or Master Ledger)\n{mod_context}\nWhen answering from this data, cite 'Vehicle Modification Records' as the source, NOT the Master Ledger or FSM."
            logger.info(f"Injected modification context for VIN {customer_vin}")

    # SCHEMA RETRY: If first attempt fails JSON validation, retry once.
    # This handles rare edge cases where Gemini's json_object mode still misfires.
    _MAX_LLM_ATTEMPTS = 2
    t0_pass1 = time.monotonic()
    response = None
    parsed = None
    for _attempt in range(1, _MAX_LLM_ATTEMPTS + 1):
        try:
            # Step 7: Generate LLM response (Pass 1 — diagnostic draft)
            raw_response = await generate_response(
                system_prompt=system_prompt,
                context=context,
                user_message=user_query,
                chat_history=chat_history,
                max_tokens=_RESPONSE_BUDGET_TOKENS,
            )
        except Exception as e:
            logger.error(f"LLM generation failed: {e}", exc_info=True)
            return _make_phase_error(
                "The AI engine is temporarily unavailable. Please try again in a moment.",
                f"LLM error: {type(e).__name__}"
            )

        # AUDIT FIX (P3-12 + P4-10 + DT-P4-06): Validate LLM output is valid JSON.
        parsed = _extract_json(raw_response)
        if parsed and "current_state" in parsed:
            response = json.dumps(parsed)  # Canonical JSON string
            break  # Valid JSON — exit retry loop

        if _attempt < _MAX_LLM_ATTEMPTS:
            logger.warning(
                f"LLM schema validation failed (attempt {_attempt}/{_MAX_LLM_ATTEMPTS}), "
                f"retrying: {raw_response[:200]}"
            )
            continue  # Retry

        # All attempts exhausted — return error
        logger.warning(f"LLM returned invalid/malformed response after {_MAX_LLM_ATTEMPTS} attempts: {raw_response[:200]}")
        response = json.dumps({
            "current_state": "PHASE_ERROR",
            "mechanic_instructions": "The AI produced an unexpected response format. Please rephrase your question.",
            "diagnostic_reasoning": "LLM output failed schema validation — may indicate prompt compliance failure.",
            "requires_input": False,
            "answer_path_prompts": [],
            "source_citations": [],
            "intersecting_subsystems": [],
        })
        parsed = None

    pass1_elapsed = time.monotonic() - t0_pass1
    logger.info(f"V11 Pass 1 (draft): {pass1_elapsed:.1f}s")

    # ═══════════════════════════════════════════════════════════════════
    # V11 MULTI-PASS: Internal self-verification (Pass 2 + optional Pass 3)
    # Only runs for PHASE_A_TRIAGE — follow-up turns are already narrowed.
    # ═══════════════════════════════════════════════════════════════════
    if (
        _ENABLE_VERIFICATION
        and parsed
        and parsed.get("current_state") == "PHASE_A_TRIAGE"
    ):
        logger.info("V11 MULTI-PASS: Running Pass 2 verification on PHASE_A_TRIAGE draft")

        # Pass 2: Verify the draft
        verification = await _verify_diagnostic(
            draft_json=response,
            user_query=user_query,
            context=context,
        )

        if verification and verification.get("revision_required", False):
            logger.warning(
                f"V11 MULTI-PASS: Verification FAILED — triggering Pass 3 revision. "
                f"Instructions: {verification.get('revision_instructions', '')[:200]}"
            )

            # Pass 3: Revise with verification feedback
            revised_response = await _revise_diagnostic(
                system_prompt=system_prompt,
                context=context,
                user_query=user_query,
                chat_history=chat_history,
                verification_result=verification,
                max_tokens=_RESPONSE_BUDGET_TOKENS,
            )

            if revised_response:
                revised_parsed = _extract_json(revised_response)
                if revised_parsed and "current_state" in revised_parsed:
                    response = json.dumps(revised_parsed)
                    parsed = revised_parsed
                    logger.info("V11 MULTI-PASS: Using Pass 3 revised response")
                else:
                    logger.warning("V11 MULTI-PASS: Pass 3 returned invalid JSON, keeping Pass 1 draft")
            else:
                logger.warning("V11 MULTI-PASS: Pass 3 failed, keeping Pass 1 draft")
        elif verification:
            logger.info("V11 MULTI-PASS: Verification PASSED — using Pass 1 draft as-is")

    # Return response with RAG context metadata for forensic analysis.
    # rag_context is a backward-compatible addition — frontend can ignore it.
    rag_sources = []
    for chunk in used_chunks:
        rag_sources.append({
            "source": chunk.get("source", ""),
            "page_numbers": chunk.get("page_numbers", []),
            "headings": chunk.get("headings", []),
        })
    return {
        "response": response,
        "rag_context": {
            "chunk_count": len(used_chunks),
            "total_tokens_used": sum(c.get("token_count", 0) for c in used_chunks),
            "sources": rag_sources,
        },
        "expansion_info": expansion_info,
    }

