# backend/routes/ledger.py
# V10: API endpoints for Master Ledger tribal knowledge management
import json
import os
import logging
from datetime import datetime
from fastapi import APIRouter, Request

from backend.shared.tokenizer import count_tokens

logger = logging.getLogger(__name__)

router = APIRouter()

LEDGER_PATH = os.environ.get("LEDGER_PATH", "/app/config/MASTER_LEDGER.md")
LEDGER_MAX_TOKENS = int(os.environ.get("LEDGER_MAX_TOKENS", "2550"))


def _read_ledger() -> str:
    """Read the current ledger content."""
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r') as f:
            return f.read()
    return ""


def _format_entry(body: dict) -> str:
    """Format a ledger entry from the API request body.

    Supports two entry types:
    - 'contextual': auto-populated subsystems/citations from a Gus response
    - 'global': fully manual entry
    """
    symptom = body.get("symptom", "").strip()
    override = body.get("override", "").strip()
    verification = body.get("verification", "").strip()
    oem_diagnosis = body.get("oem_diagnosis", "").strip()

    # Contextual metadata (auto-populated from Gus response)
    subsystems = body.get("subsystems", [])
    citations = body.get("citations", [])

    if not symptom or not override:
        return ""

    lines = [f"\n## FAULT SIGNATURE: {symptom}"]

    if subsystems:
        lines.append(f"- **RELATED SUBSYSTEMS:** {', '.join(subsystems)}")

    if citations:
        # Format citations as concise FSM references
        refs = []
        for c in citations:
            if isinstance(c, dict):
                src = c.get("source", "")
                page = c.get("page", "")
                ctx = c.get("context", "")
                ref = src
                if page:
                    ref += f" (p. {page})"
                if ctx:
                    ref += f" — {ctx}"
                refs.append(ref)
            elif isinstance(c, str):
                refs.append(c)
        if refs:
            lines.append(f"- **FSM REFERENCE:** {'; '.join(refs)}")

    if oem_diagnosis:
        lines.append(f"- **OEM FSM DIAGNOSIS:** {oem_diagnosis}")

    lines.append(f"- **MASTER TECH OVERRIDE:** {override}")

    if verification:
        lines.append(f"- **VERIFICATION TEST:** {verification}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append(f"- *Added: {timestamp}*")

    return "\n".join(lines) + "\n"


@router.get("/api/ledger")
async def get_ledger():
    """Return current ledger content and token metrics."""
    content = _read_ledger()
    token_count = count_tokens(content) if content else 0
    return {
        "content": content,
        "tokens": token_count,
        "cap": LEDGER_MAX_TOKENS,
        "remaining": max(0, LEDGER_MAX_TOKENS - token_count),
    }


@router.post("/api/ledger")
async def add_ledger_entry(request: Request):
    """Add a new Fault Signature entry to the Master Ledger.

    Validates that the entry won't exceed the token cap before appending.
    """
    body = await request.json()

    entry_text = _format_entry(body)
    if not entry_text:
        return {"status": "rejected", "message": "Symptom and override are required."}

    current = _read_ledger()
    proposed = current + entry_text

    proposed_tokens = count_tokens(proposed)
    if proposed_tokens > LEDGER_MAX_TOKENS:
        current_tokens = count_tokens(current) if current else 0
        entry_tokens = count_tokens(entry_text)
        return {
            "status": "rejected",
            "message": f"Entry would exceed token cap. Ledger: {current_tokens}, Entry: {entry_tokens}, Cap: {LEDGER_MAX_TOKENS}. Archive old entries first.",
            "tokens": current_tokens,
            "entry_tokens": entry_tokens,
            "cap": LEDGER_MAX_TOKENS,
        }

    # Append the entry
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, 'a') as f:
        f.write(entry_text)

    logger.info(f"Ledger entry added: {body.get('symptom', '')[:60]} ({proposed_tokens} total tokens)")

    return {
        "status": "accepted",
        "message": "Entry added to Master Ledger.",
        "tokens": proposed_tokens,
        "cap": LEDGER_MAX_TOKENS,
        "remaining": LEDGER_MAX_TOKENS - proposed_tokens,
    }
