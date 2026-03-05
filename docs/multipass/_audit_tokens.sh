#!/bin/bash
API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
curl -s "http://127.0.0.1:3001/api/v1/system" -H "Authorization: Bearer $API_KEY" | python3 << 'PYEOF'
import sys, json
s = json.load(sys.stdin)["settings"]
for k, v in sorted(s.items()):
    kl = k.lower()
    if any(x in kl for x in ["token","limit","splitter","chunk","text","max","ocr","document"]):
        print(f"  {k}: {v!r}")
PYEOF
