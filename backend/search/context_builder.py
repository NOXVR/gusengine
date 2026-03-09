# backend/search/context_builder.py
# V10 SPEC: Greedy token-capped context injection with full budget system
import logging
from backend.shared.tokenizer import count_tokens

logger = logging.getLogger(__name__)

# AUDIT FIX (H11): Runtime RAG budget floor — prevents long conversations from
# silently pushing RAG context to zero or negative.
MIN_RAG_FLOOR = 5000  # Minimum tokens reserved for RAG context at runtime
MAX_CHAT_HISTORY_TOKENS = 8000  # AUDIT FIX (H12): Hard cap on chat history
# AUDIT FIX (P8-03): Dynamic ChatML framing computation replaces static FRAMEWORK_OVERHEAD.
# vLLM wraps each message with <|im_start|>role\n...<|im_end|>\n (~5 tokens each).
TOKENS_PER_MESSAGE_FRAME = 5
# AUDIT FIX (P11-13): Pre-compute separator tokens at module scope to avoid
# per-request _TOKENIZER_LOCK acquisition.
SEPARATOR = "\n\n---\n\n"
SEPARATOR_TOKENS = count_tokens(SEPARATOR)


def build_context(
    chunks: list[dict],
    max_context_tokens: int = 32768,
    system_prompt_tokens: int = 900,
    ledger_tokens: int = 0,
    response_budget: int = 2000,
    chat_history_tokens: int = 0,
    user_query_tokens: int = 0,  # AUDIT FIX (P2-01): user message budget
    chat_history_message_count: int = 0,  # AUDIT FIX (P8-03): for dynamic framing
) -> tuple[str, list[dict]]:
    """Greedily fill context window with highest-scoring chunks.

    AUDIT FIX (Opus + Gemini DT): Use native AutoTokenizer for EXACT
    token counts. Do NOT use tiktoken or linear regression.

    Returns:
        (context_string, used_chunks) — formatted context and metadata
    """
    # AUDIT FIX (H12): Cap chat history to prevent unbounded growth
    if chat_history_tokens > MAX_CHAT_HISTORY_TOKENS:
        logger.warning(
            f"Chat history ({chat_history_tokens} tokens) exceeds cap "
            f"({MAX_CHAT_HISTORY_TOKENS}). Truncating to cap."
        )
        chat_history_tokens = MAX_CHAT_HISTORY_TOKENS

    # AUDIT FIX (P8-03): Dynamic framing overhead based on actual message count.
    # +2 accounts for the system message and the current user message (always present).
    framework_overhead = (chat_history_message_count + 2) * TOKENS_PER_MESSAGE_FRAME

    # AUDIT FIX (P9-08): Budget the literal injection strings that connect sections.
    # "\n\nMASTER_LEDGER.md:\n" ≈ 6 tokens + "\n\nRETRIEVED DOCUMENTS:\n\n" ≈ 7 tokens.
    INJECTION_OVERHEAD = 15  # Conservative ceiling for connecting strings

    available = (max_context_tokens
                 - system_prompt_tokens
                 - ledger_tokens
                 - response_budget
                 - chat_history_tokens
                 - user_query_tokens       # AUDIT FIX (P2-01)
                 - framework_overhead      # AUDIT FIX (P8-03): dynamic
                 - INJECTION_OVERHEAD)     # AUDIT FIX (P9-08): connecting strings

    # AUDIT FIX (H11 + P7-03): Enforce minimum RAG budget floor at runtime.
    # P7-03: CHANGED from silent override to rejection. The original
    # `available = MIN_RAG_FLOOR` fabricated tokens out of thin air.
    if available < MIN_RAG_FLOOR:
        raise ValueError(
            f"Context budget exhausted: available={available} tokens, "
            f"floor={MIN_RAG_FLOOR}. Reduce chat history or ledger size."
        )

    # Typical (with ledger, no chat, 2 messages, ~50 token query):
    #   32768 - 900 - 2550 - 2000 - 50 - 10 - 15 = 27,243 tokens for RAG
    # This is ~16.4× the V9 budget of 1,600 tokens

    # LAYER 2 FIX: Source-balanced interleaving.
    # Instead of pure score-order (which lets one keyword-dense FSM section
    # monopolize the context window), round-robin from each source PDF.
    # This ensures the LLM sees procedures from multiple FSM sections.
    from collections import defaultdict
    by_source = defaultdict(list)
    for chunk in chunks:
        by_source[chunk["source"]].append(chunk)
    # Each source's chunks are already in score order from hybrid_search
    interleaved = []
    max_depth = max((len(v) for v in by_source.values()), default=0)
    for depth in range(max_depth):
        for source_key in by_source:
            if depth < len(by_source[source_key]):
                interleaved.append(by_source[source_key][depth])

    used_tokens = 0
    used_chunks = []
    context_parts = []

    for i, chunk in enumerate(interleaved):
        # Use pre-computed token count from ingestion
        chunk_tokens = chunk["token_count"]

        # Format chunk with provenance header
        header = f"[Source {i+1}: {chunk['source']}"
        if chunk["page_numbers"]:
            pages = ", ".join(str(p) for p in chunk["page_numbers"])
            header += f" | Pages {pages}"
        if chunk["headings"]:
            header += f" | {' > '.join(chunk['headings'])}"
        header += "]"

        # AUDIT FIX: Compute actual header token cost instead of hardcoded 20.
        header_tokens = count_tokens(header + "\n")  # AUDIT FIX (P8-12)
        separator_cost = SEPARATOR_TOKENS if context_parts else 0  # AUDIT FIX (P5-11)
        total_cost = chunk_tokens + header_tokens + separator_cost

        if used_tokens + total_cost > available:
            break

        context_parts.append(f"{header}\n{chunk['text']}")
        used_tokens += total_cost
        used_chunks.append(chunk)

    context_string = SEPARATOR.join(context_parts)
    return context_string, used_chunks
