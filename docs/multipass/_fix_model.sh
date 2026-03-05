#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

echo "=== Updating Anthropic model to claude-sonnet-4-6 ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "AnthropicModelPref": "claude-sonnet-4-6"
  }')
echo "$RESULT"

echo ""
echo "=== Verifying ==="
curl -s "$BASE/system" -H "$AUTH" | python3 -c "
import sys, json
s = json.load(sys.stdin)['settings']
print('LLMProvider:', s.get('LLMProvider'))
print('AnthropicModelPref:', s.get('AnthropicModelPref'))
"

echo ""
echo "=== Restarting container to pick up new model ==="
docker restart diagnostic_rag_engine
sleep 8

echo ""
echo "=== Container status ==="
docker ps --format 'table {{.Names}}\t{{.Status}}'
docker logs diagnostic_rag_engine --tail 5 2>&1

echo ""
echo "=== Done ==="
