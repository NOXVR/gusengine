#!/bin/bash
# Citation accuracy test — send K-Jetronic query and verify page numbers
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"

# Create fresh thread
echo "=== Creating fresh thread ==="
THREAD_SLUG=$(curl -s -X POST "$BASE/workspace/$SLUG/thread/new" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -c "import sys,json; print(json.load(sys.stdin)['thread']['slug'])")
echo "Thread: $THREAD_SLUG"

echo ""
echo "=== Sending K-Jetronic query ==="
curl -s -X POST "$BASE/workspace/$SLUG/thread/$THREAD_SLUG/chat" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"message": "1975 Mercedes 450SL K-Jetronic warm control pressure regulator leaking fuel from diaphragm. What is the diagnostic procedure?", "mode": "chat"}' > /tmp/citation_test.json

python3 << 'PYEOF'
import json, re

with open("/tmp/citation_test.json") as f:
    raw = json.load(f)

text = raw.get("textResponse", "")
sources = raw.get("sources", [])

print(f"Response length: {len(text)} chars")
print(f"AnythingLLM chunks returned: {len(sources)}")

# Parse Gus JSON
try:
    start = text.index("{")
    end = text.rindex("}") + 1
    parsed = json.loads(text[start:end])
    
    print(f"\ncurrent_state: {parsed.get('current_state')}")
    print(f"requires_input: {parsed.get('requires_input')}")
    
    citations = parsed.get("source_citations", [])
    print(f"\n=== SOURCE CITATIONS ({len(citations)}) ===")
    
    has_real_pages = False
    has_unknown = False
    for i, c in enumerate(citations):
        page = c.get("page", "MISSING")
        source = c.get("source", "MISSING")
        context = c.get("context", "")
        print(f"  [{i+1}] page: {page}")
        print(f"      source: {source}")
        print(f"      context: {context[:100]}")
        if page != "unknown" and page != "MISSING":
            has_real_pages = True
        else:
            has_unknown = True
    
    print()
    if has_real_pages and not has_unknown:
        print("CITATION TEST: PASS — All pages are real numbers")
    elif has_real_pages:
        print("CITATION TEST: PARTIAL — Some pages are real, some unknown")
    else:
        print("CITATION TEST: FAIL — All pages are unknown")
        
except Exception as e:
    print(f"JSON parse error: {e}")
    print(f"Raw response: {text[:500]}")

# Also check if chunks contain watermarks
print(f"\n=== CHUNK WATERMARK CHECK ===")
for i, s in enumerate(sources[:4]):
    title = s.get("title", "?")
    content = s.get("text", s.get("content", s.get("pageContent", "")))
    tags = re.findall(r'\[\[ABSOLUTE_PAGE: \d+\]\]', content)
    print(f"  [{i+1}] {title}")
    print(f"      Watermark tags in chunk: {tags[:5]}")
PYEOF
