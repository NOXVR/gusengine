#!/bin/bash
# Phase 7: Configure LLM settings via AnythingLLM API
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

echo "=== 1. Check current system settings ==="
curl -s "$BASE/admin/system-preferences" -H "$AUTH" 2>&1 | head -5
echo ""

echo "=== 2. Try /system endpoint ==="
curl -s "$BASE/system" -H "$AUTH" 2>&1 | python3 -m json.tool 2>/dev/null | head -30
echo ""

echo "=== 3. Try /system/env-dump ==="
curl -s "$BASE/system/env-dump" -H "$AUTH" 2>&1 | python3 -m json.tool 2>/dev/null | head -40
echo ""

echo "=== 4. List available API routes ==="
curl -s "$BASE" -H "$AUTH" 2>&1 | head -10
echo ""

echo "=== 5. Try updating LLM provider ==="
curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "LLMProvider": "anthropic",
    "AnthropicApiKey": "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",
    "AnthropicModelPref": "claude-3-5-sonnet-latest",
    "AnthropicTokenLimit": 4000
  }' 2>&1 | python3 -m json.tool 2>/dev/null
echo ""

echo "=== Done ==="
