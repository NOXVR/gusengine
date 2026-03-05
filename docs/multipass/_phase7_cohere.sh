#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

echo "=== Setting Cohere Reranking ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "CohereApiKey": "UABuVMuUH7fLCMhB4OH4MoJUGfGK7BmrGXxho9t3",
    "CohereModelPref": "rerank-english-v3.0"
  }')
echo "$RESULT"
echo ""

echo "=== Verifying Cohere is set ==="
curl -s "$BASE/system" -H "$AUTH" | python3 -c "
import sys, json
data = json.load(sys.stdin)
s = data.get('settings', {})
print(f'CohereApiKey: {s.get(\"CohereApiKey\", \"NOT FOUND\")}')
print(f'CohereModelPref: {s.get(\"CohereModelPref\", \"NOT FOUND\")}')
# Also check if there's a reranking-specific key
for k in sorted(s.keys()):
    kl = k.lower()
    if 'cohere' in kl or 'rerank' in kl:
        print(f'{k}: {s[k]}')
"

echo ""
echo "=== Done ==="
