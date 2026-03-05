#!/bin/bash
set -e

# V8 Validated Ledger Update Script
# Gates MASTER_LEDGER.md behind validate_ledger.py before upload.
# Uses sync_ledger.py (Python/requests) for consistent venv execution.

LEDGER_PATH="$1"
ENGINE_DIR="$HOME/diagnostic_engine"
VENV_PYTHON="$ENGINE_DIR/venv/bin/python3"

if [ -z "$LEDGER_PATH" ]; then
    echo "Usage: ./update_ledger.sh /path/to/MASTER_LEDGER.md"
    exit 1
fi

if [ ! -f "$LEDGER_PATH" ]; then
    echo "FATAL: File not found: $LEDGER_PATH"
    exit 1
fi

echo "=== V8 Ledger Validator ==="
echo "Validating token count..."

# GATE: Validate BEFORE upload. If this fails, nothing is uploaded.
if ! $VENV_PYTHON "$ENGINE_DIR/validate_ledger.py" "$LEDGER_PATH"; then
    echo ""
    echo "REJECTED: Ledger exceeds token cap. Edit the file and retry."
    exit 1
fi

echo ""
echo "Token validation PASSED. Uploading to workspace..."

# Upload via sync_ledger.py (uses Python requests through venv, bypasses Nginx)
$VENV_PYTHON "$ENGINE_DIR/sync_ledger.py" "$LEDGER_PATH"

echo ""
echo "=== LEDGER UPDATED SUCCESSFULLY ==="
echo "IMPORTANT: Open the AnythingLLM Web UI and click the PUSHPIN icon"
echo "on the ledger document to pin it to the workspace context."
