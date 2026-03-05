#!/bin/bash
# Check if watermarks appear in the actual embedded document chunks
API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"

echo "=== Checking if [[ABSOLUTE_PAGE:]] appears in embedded chunks ==="

# Get a document that's already ingested and search its content
# Use the document endpoint to list available docs
curl -s "$BASE/documents" -H "Authorization: Bearer $API_KEY" | python3 << 'PYEOF'
import sys, json

data = json.load(sys.stdin)
docs = data.get("localFiles", {}).get("items", [])
print(f"Total document folders: {len(docs)}")

# Look at first few document items to find embedded content
count = 0
for folder in docs[:3]:
    items = folder.get("items", [])
    for item in items[:2]:
        name = item.get("name", "?")
        print(f"\n--- Document: {name} ---")
        # Try to get the cached content
        cached = item.get("cached", False)
        print(f"  cached: {cached}")
        count += 1
if count == 0:
    print("No documents found in API response")
PYEOF

echo ""
echo "=== Direct chunk text search via vector DB ==="
# Send a query that should return chunks, then check if chunks contain watermarks
curl -s -X POST "$BASE/workspace/1975-mercedes-benz-450sl/chat" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me page 1 of the engine views document 00.1-100", "mode": "chat"}' | python3 << 'PYEOF'
import sys, json

raw = json.load(sys.stdin)
text = raw.get("textResponse", "")
sources = raw.get("sources", [])

print(f"Response length: {len(text)} chars")
print(f"Sources (chunks) returned: {len(sources)}")

for i, s in enumerate(sources[:5]):
    title = s.get("title", "?")
    content = s.get("text", s.get("content", ""))
    has_watermark = "[[ABSOLUTE_PAGE:" in content
    # Find all watermark tags in the content
    import re
    tags = re.findall(r'\[\[ABSOLUTE_PAGE: \d+\]\]', content)
    print(f"\n  [{i+1}] {title}")
    print(f"      Has watermark: {has_watermark}")
    print(f"      Watermark tags found: {tags}")
    if content:
        print(f"      Content preview (first 200 chars): {content[:200]}")
    else:
        print(f"      (no text/content field in source object)")
        print(f"      Available keys: {list(s.keys())}")
PYEOF
