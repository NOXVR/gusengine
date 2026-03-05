#!/bin/bash
API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
curl -s "$BASE/workspace/1975-mercedes-benz-450sl" -H "Authorization: Bearer $API_KEY" > /tmp/ws.json
python3 << 'PYEOF'
import json
with open("/tmp/ws.json") as f:
    raw = json.load(f)
if isinstance(raw, dict) and "workspace" in raw:
    d = raw["workspace"]
    if isinstance(d, list):
        d = d[0] if d else {}
elif isinstance(raw, list):
    d = raw[0] if raw else {}
else:
    d = raw
skip = {"openAiPrompt", "documents"}
for k in sorted(d.keys()):
    if k in skip:
        continue
    print(f"  {k}: {d[k]!r}")
PYEOF
