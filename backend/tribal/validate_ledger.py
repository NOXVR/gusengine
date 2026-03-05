# backend/tribal/validate_ledger.py
# V10: Uses native AutoTokenizer instead of tiktoken
# Validates MASTER_LEDGER.md token count against the cap before appending entries.
import os

try:
    from backend.shared.tokenizer import TOKENIZER, count_tokens
except (ImportError, RuntimeError):
    # Running on host or standalone — instantiate locally
    from transformers import AutoTokenizer
    MODEL_PATH = os.environ.get(
        "TOKENIZER_MODEL_PATH",
        "./storage/models/Qwen2.5-32B-Instruct-AWQ"
    )
    TOKENIZER = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True,
        local_files_only=True,
    )
    def count_tokens(text: str) -> int:
        return len(TOKENIZER.encode(text))

RAW_CAP = 3000
SAFETY_FACTOR = 0.85
ADJUSTED_CAP = int(RAW_CAP * SAFETY_FACTOR)  # = 2550


def validate(content: str) -> tuple[bool, int]:
    """Validate ledger content against token cap.
    Returns (approved: bool, token_count: int).
    """
    token_count = count_tokens(content)
    return (token_count <= ADJUSTED_CAP, token_count)


def validate_file(path: str) -> tuple[bool, int]:
    """Validate a ledger file on disk."""
    with open(path, 'r') as f:
        content = f.read()
    return validate(content)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: validate_ledger.py <path_to_ledger.md>")
        sys.exit(1)
    approved, count = validate_file(sys.argv[1])
    print(f"Ledger tokens: {count}")
    print(f"Adjusted cap (15% safety): {ADJUSTED_CAP}")
    if approved:
        print("APPROVED.")
    else:
        print(f"REJECTED: Ledger tokens ({count}) exceed cap ({ADJUSTED_CAP}).")
    sys.exit(0 if approved else 1)
