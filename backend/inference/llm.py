# backend/inference/llm.py
# V10 SPEC: vLLM inference client (OpenAI-compatible API)
import asyncio
import os
import logging
import threading
import httpx

logger = logging.getLogger(__name__)

# AUDIT FIX (P10-18): Read VLLM_BASE_URL from env var.
# Supports both local vLLM and remote APIs (Gemini, OpenAI, etc.)
VLLM_BASE_URL = os.environ.get("VLLM_BASE_URL", "http://vllm:8000/v1")
# AUDIT FIX (P7-08): Read model name from environment so operator can swap models.
VLLM_MODEL = os.environ.get("VLLM_MODEL", "Qwen2.5-32B-Instruct-AWQ")
# API key for remote LLM providers (Gemini, OpenAI, etc.). Empty = no auth (local vLLM).
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")

# AUDIT FIX (P4-06): Persistent httpx client singleton.
_llm_client: httpx.AsyncClient | None = None

# AUDIT FIX (P8-05 + DT-P9-01): Asyncio lock for LLM pool flush serialization.
# DT-P9-01: Deferred initialization — asyncio.Lock() at module scope crashes on
# Python 3.10+ because no event loop exists during import.
_llm_client_lock: asyncio.Lock | None = None
# AUDIT FIX (P10-04): Thread-safe double-checked locking.
_llm_lock_init = threading.Lock()


async def _get_llm_lock() -> asyncio.Lock:
    global _llm_client_lock
    if _llm_client_lock is None:
        with _llm_lock_init:
            if _llm_client_lock is None:
                _llm_client_lock = asyncio.Lock()
    return _llm_client_lock


async def _flush_llm_client():
    """AUDIT FIX (P8-05): Serialized LLM pool flush, matching P7-13 TEI pattern."""
    lock = await _get_llm_lock()
    async with lock:
        global _llm_client
        if _llm_client is not None and not _llm_client.is_closed:
            await _llm_client.aclose()
            _llm_client = None


async def _get_llm_client() -> httpx.AsyncClient:
    # AUDIT FIX (P10-03): Lock-protect client initialization.
    lock = await _get_llm_lock()
    async with lock:
        global _llm_client
        if _llm_client is None or _llm_client.is_closed:
            # AUDIT FIX (P7-12): Explicit pool limits + split timeout.
            # 120s read timeout for long 32K inferences;
            # 10s connect timeout for fast-fail on dead vLLM container.
            headers = {}
            if LLM_API_KEY:
                headers["Authorization"] = f"Bearer {LLM_API_KEY}"
            _llm_client = httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=10.0),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
                headers=headers,
            )
        return _llm_client


async def generate_response(
    system_prompt: str,
    context: str,
    user_message: str,
    chat_history: list[dict],
    max_tokens: int = 8192,
    temperature: float = 0.1,
) -> str:
    """Call vLLM with assembled prompt.

    Temperature 0.1 for near-deterministic diagnostic output.
    Qwen2.5 has strong instruction-following for JSON output.
    """
    # TRIAD FIX (OP-8): Append context to single system message.
    # Multiple system-role messages may misbehave with Qwen2.5's chat template.
    system_content = system_prompt
    # AUDIT FIX (P2-05): ALWAYS include the RETRIEVED DOCUMENTS header.
    # Without it, the system prompt's ZERO-RETRIEVAL SAFEGUARD condition
    # ("section is empty") never matches ("section is absent"), and the LLM
    # hallucinates a diagnostic instead of emitting RETRIEVAL_FAILURE.
    if context:
        system_content += f"\n\nRETRIEVED DOCUMENTS:\n\n{context}"
    else:
        # AUDIT FIX (P3-07): Empty section so the system prompt's
        # ZERO-RETRIEVAL SAFEGUARD trigger ("section is empty") matches.
        system_content += "\n\nRETRIEVED DOCUMENTS:\n\n"

    messages = [
        {"role": "system", "content": system_content},
    ]

    # Add chat history
    messages.extend(chat_history)

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    client = await _get_llm_client()
    # AUDIT FIX (P7-12): Pool flush on connection failure, matching GP7-05 pattern.
    try:
        payload = {
            "model": VLLM_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            # SCHEMA FIX: Force JSON output mode for remote LLM providers (Gemini, GPT-4o).
            # Without this, Gemini 2.5 Flash intermittently returns prose instead of JSON,
            # causing PHASE_ERROR "unexpected response format" for every query.
            "response_format": {"type": "json_object"},
        }
        # AUDIT FIX (P10-21): Stop sequence only needed for local Qwen models.
        # Qwen2.5 can emit \n\n\n inside JSON string values, truncating mid-JSON.
        # Remote APIs (Gemini, GPT-4o, Claude) handle this natively.
        if not LLM_API_KEY:
            payload["stop"] = ["\n\n\n\n\n"]
        response = await client.post(
            f"{VLLM_BASE_URL}/chat/completions",
            json=payload,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    # AUDIT FIX (P11-07): Added RuntimeError to catch use-after-close.
    except (httpx.ConnectError, httpx.ReadTimeout, RuntimeError) as e:
        logger.warning(f"vLLM connection failure ({type(e).__name__}) — flushing httpx pool")
        await _flush_llm_client()
        raise
