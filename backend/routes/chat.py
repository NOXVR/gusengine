# backend/routes/chat.py
# V10 SPEC: Full chat orchestration — DAG, ledger, budget, JSON validation
# V10 FIREWALL: Vehicle-scoped collection routing, identity swap, scoped ledger
# V11 MULTI-PASS: Internal self-verification before response delivery
import asyncio
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
    stripped = re.sub(r'<think>.*?</think>', '', raw.strip(), flags=re.DOTALL)
    stripped = re.sub(r'^```(?:json)?\s*\n?', '', stripped.strip())
    stripped = re.sub(r'\n?```\s*$', '', stripped)
    return stripped


def _extract_json(raw: str) -> dict | None:
    """Parse JSON from LLM output, with balanced-brace recovery."""
    stripped = _strip_llm_fences(raw)
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
    return None


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
            max_tokens=2000,
        )
    except Exception as e:
        logger.warning(f"V11 verification call failed ({type(e).__name__}), skipping verification")
        return None
    elapsed = time.monotonic() - t0

    result = _extract_json(raw_response)
    if result is None:
        logger.warning(f"V11 verification returned non-JSON, skipping: {raw_response[:200]}")
        return None

    passed = result.get("verification_passed", True)
    revision_required = result.get("revision_required", False)
    checks = result.get("checks", {})

    # Log check results
    check_summary = []
    for check_name, check_data in checks.items():
        if isinstance(check_data, dict):
            status = "PASS" if check_data.get("passed", True) else "FAIL"
            check_summary.append(f"{check_name}={status}")
    summary_str = ", ".join(check_summary) if check_summary else "no-checks-parsed"

    logger.info(
        f"V11 VERIFY: passed={passed}, revision={revision_required}, "
        f"checks=[{summary_str}], latency={elapsed:.1f}s"
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

    # AUDIT FIX (H09/H10/H13): Comprehensive error handling for embed → search → generate
    try:
        # Step 3: Embed user query for retrieval
        # AUDIT FIX (P4-05 + P7-05): Acquire EMBED_SEMAPHORE with timeout
        from backend.ingestion.pipeline import _get_embed_semaphore
        _embed_sem = await _get_embed_semaphore()
        try:
            await asyncio.wait_for(_embed_sem.acquire(), timeout=5.0)
        except asyncio.TimeoutError:
            raise RuntimeError("Embedding service at capacity — all permits held by ingestion")
        try:
            query_dense, query_sparse = await embed_text(user_query)
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
        # AUDIT FIX (P3-08 + P6-05): Dispatch to dedicated search pool
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            _SEARCH_POOL,
            lambda: hybrid_search(
                qdrant_search_client, query_dense, query_sparse,
                top_k=60,  # AUDIT FIX (DT-P9-05): top_k=60
                collection_name=active_collection,  # V10 FIREWALL
            ),
        )
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
    }

