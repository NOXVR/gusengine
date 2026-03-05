#!/bin/bash
set -euo pipefail

ENGINE_DIR="$HOME/diagnostic_engine"
VENV="$ENGINE_DIR/venv/bin/python3"

echo "=== File listing ==="
ls -la "$ENGINE_DIR"/*.py "$ENGINE_DIR"/*.sh

echo ""
echo "=== Python import checks ==="
$VENV -c "import requests; import tiktoken; import fitz; import re; print('All imports OK')"

echo ""
echo "=== Syntax checks ==="
$VENV -c "import py_compile; py_compile.compile('$ENGINE_DIR/validate_ledger.py', doraise=True); print('validate_ledger.py: OK')"
$VENV -c "import py_compile; py_compile.compile('$ENGINE_DIR/sync_ingest.py', doraise=True); print('sync_ingest.py: OK')"
$VENV -c "import py_compile; py_compile.compile('$ENGINE_DIR/verify_ingestion.py', doraise=True); print('verify_ingestion.py: OK')"
$VENV -c "import py_compile; py_compile.compile('$ENGINE_DIR/sync_ledger.py', doraise=True); print('sync_ledger.py: OK')"
$VENV -c "import py_compile; py_compile.compile('$ENGINE_DIR/vmdk_extractor.py', doraise=True); print('vmdk_extractor.py: OK')"
bash -n "$ENGINE_DIR/update_ledger.sh" && echo "update_ledger.sh: OK"

echo ""
echo "=== All checks passed ==="
