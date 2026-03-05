#!/usr/bin/env python3
"""V8 Ledger Token Validator.
Validates MASTER_LEDGER.md token count against the 1500-token cap
with a 15% safety margin for Anthropic tokenizer divergence.
Returns bool for composability; exit code set by __main__.
"""

import tiktoken, sys

# HARD CAP: 1500 tokens for the pinned ledger
# SAFETY MARGIN: 15% reduction for GPT-4 vs Anthropic tokenizer divergence
RAW_CAP = 1500
SAFETY_FACTOR = 0.85
ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 1275

# V9 RECOVERY (I-2): Minimum RAG budget floor check.
# Restored from VFINAL Phase 10 (lines 500-521).
# Ensures the remaining token budget never falls below a safe floor
# for RAG retrieval, even if the ledger is under the hard cap.
MIN_RAG_BUDGET = 2000

def validate(path):
    # V2 FIX: Pin encoding directly instead of model-based lookup
    enc = tiktoken.get_encoding("cl100k_base")
    with open(path, 'r') as f:
        content = f.read()
    count = len(enc.encode(content))
    remaining = 4000 - 750 - count  # 4000 total - 750 system prompt (V9: +150 from R-1–R-4) - ledger

    print(f"Ledger tokens (cl100k_base estimate): {count}")
    print(f"Adjusted cap (15% safety margin): {ADJUSTED_CAP}")
    print(f"Budget remaining (RAG + response): {remaining}")
    print(f"Minimum RAG budget floor: {MIN_RAG_BUDGET}")

    if count > ADJUSTED_CAP:
        print(f"REJECTED: Ledger tokens ({count}) exceed safety-adjusted cap ({ADJUSTED_CAP}).")
        print("Archive oldest entries and retry.")
        return False
    if remaining < MIN_RAG_BUDGET:
        print(f"⚠ WARNING: RAG budget dangerously low ({remaining} tokens, minimum: {MIN_RAG_BUDGET}).")
        print("Reduce ledger size or increase LLM context limit.")
        return False
    print("APPROVED.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_ledger.py <path_to_ledger.md>")
        sys.exit(1)
    result = validate(sys.argv[1])
    sys.exit(0 if result else 1)
