#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"

echo "=== Adding remaining 210 watermarked docs ==="
ADDS=$(cat /tmp/remaining_adds.json)
RESULT=$(curl -s -X POST "$BASE/workspace/$SLUG/update-embeddings" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"adds\": $ADDS, \"deletes\": []}")

python3 -c "
import json
raw = json.loads('''$RESULT''')
ws = raw.get('workspace', {})
docs = ws.get('documents', [])
print(f'Docs now: {len(docs)}')
" 2>/dev/null || python3 << 'PYEOF'
import json
with open("/dev/stdin") as f:
    pass
# Fallback: just check workspace directly
import urllib.request
req = urllib.request.Request(
    "http://127.0.0.1:3001/api/v1/workspace/1975-mercedes-benz-450sl",
    headers={"Authorization": "Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ"})
resp = json.loads(urllib.request.urlopen(req).read())
ws = resp.get("workspace", resp)
if isinstance(ws, list):
    ws = ws[0]
docs = ws.get("documents", [])
print(f"Docs now: {len(docs)}")
PYEOF
