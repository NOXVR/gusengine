#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"

echo "Waiting 10s for server to stabilize..."
sleep 10

echo "Sending query via workspace chat (not thread)..."
RESPONSE=$(curl -s --max-time 120 -X POST "$BASE/workspace/$SLUG/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the procedure for checking valve timing on the M117 engine?", "mode": "chat"}')

echo "$RESPONSE" > /tmp/citation_test2.json
SIZE=$(wc -c < /tmp/citation_test2.json)
echo "Response size: $SIZE bytes"

if [ "$SIZE" -lt 10 ]; then
    echo "ERROR: Empty or too-small response"
    cat /tmp/citation_test2.json
    exit 1
fi

/home/ubuntu/diagnostic_engine/venv/bin/python3 << 'PYEOF'
import json, re

with open("/tmp/citation_test2.json") as f:
    raw = json.load(f)

text = raw.get("textResponse", "")
sources = raw.get("sources", [])
print(f"Response: {len(text)} chars")
print(f"Sources: {len(sources)} chunks\n")

print("=== CHUNK WATERMARK CHECK ===")
all_have_tags = True
for i, s in enumerate(sources):
    content = s.get("text", "")
    tags = re.findall(r'\[\[ABSOLUTE_PAGE: (\d+)\]\]', content)
    title = s.get("title", "?")
    has_tag = len(tags) > 0
    if not has_tag:
        all_have_tags = False
    print(f"  [{i+1}] {title[:60]}")
    print(f"      Watermark: {'YES' if has_tag else 'NO'} — pages: {list(set(tags))}")

print(f"\nAll chunks have watermarks: {'YES' if all_have_tags else 'NO'}")

print("\n=== GUS RESPONSE ===")
try:
    start = text.index("{")
    end = text.rindex("}") + 1
    parsed = json.loads(text[start:end])
    citations = parsed.get("source_citations", [])
    state = parsed.get("current_state", "?")
    print(f"State: {state}")
    print(f"Citations: {len(citations)}")
    for c in citations:
        print(f"  page: {c.get('page','?')} | source: {c.get('source','?')[:50]}")
    
    has_real = any(str(c.get("page","")).isdigit() for c in citations)
    has_unknown = any(c.get("page") == "unknown" for c in citations)
    if has_real and not has_unknown:
        print("\nVERDICT: PASS — ALL citations have real page numbers")
    elif has_real:
        print("\nVERDICT: PARTIAL — some real, some unknown")
    elif len(citations) == 0:
        print("\nVERDICT: NO CITATIONS (may be triage state)")
    else:
        print("\nVERDICT: FAIL — all unknown")
except Exception as e:
    print(f"Parse error: {e}")
    print(f"Raw: {text[:500]}")
PYEOF
