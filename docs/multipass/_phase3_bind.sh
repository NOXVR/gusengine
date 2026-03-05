#!/bin/bash
set -euo pipefail

ENGINE_DIR="$HOME/diagnostic_engine"

# Phase 3 per V9 spec lines 304-316
# Remove any existing INTERNAL_API_KEY line
sed -i '/^INTERNAL_API_KEY=/d' "$ENGINE_DIR/.env"

# Add the key
echo "INTERNAL_API_KEY=S14RWKG-6DC451B-KY6VXQB-SYV33BQ" >> "$ENGINE_DIR/.env"
chmod 600 "$ENGINE_DIR/.env"

# Extract and verify
INTERNAL_KEY=$(grep INTERNAL_API_KEY "$ENGINE_DIR/.env" | tail -1 | cut -d '=' -f2-)

if [ -z "$INTERNAL_KEY" ]; then
    echo "FATAL: API key is empty. Re-check your paste."
    exit 1
fi

echo "API Key bound: ${INTERNAL_KEY:0:8}..."
echo ""
echo "=== Final .env ==="
cat "$ENGINE_DIR/.env"
echo ""
echo "=== Phase 3 complete ==="
