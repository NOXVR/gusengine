#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
SLUG="1975-mercedes-benz-450sl"

# Simple direct query
echo "=== Sending query ==="
RESPONSE=$(curl -s -X POST "$BASE/workspace/$SLUG/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "K-Jetronic fuel injector removal procedure", "mode": "chat"}')

echo "$RESPONSE" > /tmp/wm_test.json
echo "Response saved, size: $(wc -c < /tmp/wm_test.json)"

/home/ubuntu/diagnostic_engine/venv/bin/python3 << 'PYEOF'
import json, re

with open("/tmp/wm_test.json") as f:
    content = f.read()

if not content.strip():
    print("EMPTY RESPONSE - API may be busy")
    exit(1)

raw = json.loads(content)
text = raw.get("textResponse", "")
sources = raw.get("sources", [])

print(f"textResponse: {len(text)} chars")
print(f"sources: {len(sources)} chunks")

# Check each source chunk for watermarks
for i, s in enumerate(sources):
    title = s.get("title", "?")
    # sources might have different field names for content
    content = ""
    for key in ["text", "content", "pageContent", "chunkContent"]:
        if key in s:
            content = s[key]
            break
    tags = re.findall(r'\[\[ABSOLUTE_PAGE: \d+\]\]', content)
    print(f"\n  Chunk [{i+1}]: {title}")
    print(f"    Keys: {list(s.keys())}")
    print(f"    Content length: {len(content)}")
    print(f"    Watermarks: {tags[:5]}")
    if content:
        print(f"    First 150 chars: {content[:150]}")

# Also try to parse Gus JSON for citations
if text:
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        parsed = json.loads(text[start:end])
        citations = parsed.get("source_citations", [])
        print(f"\n=== GUS CITATIONS ({len(citations)}) ===")
        for c in citations:
            print(f"  page: {c.get('page','?')} | source: {c.get('source','?')}")
    except:
        print(f"\nCould not parse Gus JSON from response")
        print(f"Response preview: {text[:300]}")
PYEOF
