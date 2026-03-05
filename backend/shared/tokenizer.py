# backend/shared/tokenizer.py
# Thread-safe tokenizer singleton for Qwen2.5 models
# V10 SPEC: Eager-load at import time. Fail fast if model path missing.
import os
import threading
from transformers import AutoTokenizer

# AUDIT FIX (P4-11 + DT-P5-06): Pre-check model directory with clear error message.
# Without this, a missing volume mount produces a confusing ImportError
# traceback deep in the transformers library.
# DT-P5-06: RuntimeError is properly catchable (SystemExit bypasses except).
_MODEL_PATH = os.environ.get(
    "TOKENIZER_MODEL_PATH",
    "/app/models/Qwen2.5-32B-Instruct-AWQ"
)
if not os.path.isdir(_MODEL_PATH):
    raise RuntimeError(
        f"Fatal: tokenizer model directory not found at {_MODEL_PATH}. "
        f"Ensure model weights are pre-downloaded to ./storage/models/."
    )

TOKENIZER = AutoTokenizer.from_pretrained(
    _MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True,
)

# AUDIT FIX (P6-06): Thread-safe token counting wrapper.
# TOKENIZER.encode() is called from multiple async contexts that may run on
# different threads via asyncio.to_thread(): chat handler, build_context(),
# parse_and_chunk(), and eviction loop. HuggingFace provides NO thread-safety
# guarantee for trust_remote_code tokenizers (Qwen2.5 loads custom Python code).
# A threading.Lock prevents potential state corruption in the custom tokenization.
_TOKENIZER_LOCK = threading.Lock()

def count_tokens(text: str) -> int:
    """Thread-safe token counting."""
    with _TOKENIZER_LOCK:
        return len(TOKENIZER.encode(text))
