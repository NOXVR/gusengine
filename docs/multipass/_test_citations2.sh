#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"

# Create a new thread to get clean context
echo "=== Creating new thread ==="
THREAD=$(curl -s -X POST "$BASE/workspace/$SLUG/thread/new" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{}')
echo "$THREAD"
THREAD_SLUG=$(echo "$THREAD" | python3 -c "import sys,json; print(json.load(sys.stdin).get('thread',{}).get('slug',''))" 2>/dev/null || echo "")
echo "Thread slug: $THREAD_SLUG"

if [ -z "$THREAD_SLUG" ]; then
    echo "Failed to create thread, using main chat"
    # Try direct chat with a specific K-Jet symptom that should force citations
    echo ""
    echo "=== Sending direct K-Jetronic query ==="
    RESPONSE=$(curl -s -X POST "$BASE/workspace/$SLUG/chat" \
      -H "$AUTH" \
      -H "Content-Type: application/json" \
      -d '{"message": "1975 Mercedes 450SL K-Jetronic warm control pressure regulator leaking fuel from diaphragm. What is the diagnostic procedure and torque spec for replacement?", "mode": "chat"}')
    echo "$RESPONSE" > /tmp/gus_response.json
else
    echo ""
    echo "=== Sending K-Jetronic query in new thread ==="
    RESPONSE=$(curl -s -X POST "$BASE/workspace/$SLUG/thread/$THREAD_SLUG/chat" \
      -H "$AUTH" \
      -H "Content-Type: application/json" \
      -d '{"message": "1975 Mercedes 450SL K-Jetronic warm control pressure regulator leaking fuel from diaphragm. What is the diagnostic procedure and torque spec for replacement?", "mode": "chat"}')
    echo "$RESPONSE" > /tmp/gus_response.json
fi

echo ""
echo "=== RAW RESPONSE ==="
python3 << 'PYEOF'
import json

with open("/tmp/gus_response.json") as f:
    content = f.read()

if not content.strip():
    print("EMPTY RESPONSE")
    exit(0)

raw = json.loads(content)
text = raw.get("textResponse", "NO textResponse FIELD")
print("--- textResponse ---")
print(text[:3000])
print("")

# Parse Gus JSON
try:
    start = text.index("{")
    end = text.rindex("}") + 1
    parsed = json.loads(text[start:end])
    print("--- PARSED ---")
    print(f"current_state: {parsed.get('current_state')}")
    print(f"requires_input: {parsed.get('requires_input')}")
    citations = parsed.get("source_citations", [])
    print(f"source_citations count: {len(citations)}")
    for i, c in enumerate(citations):
        print(f"  [{i+1}] source: {c.get('source','?')}, page: {c.get('page','?')}, context: {c.get('context','?')}")
    prompts = parsed.get("answer_path_prompts", [])
    print(f"answer_path_prompts count: {len(prompts)}")
    for p in prompts:
        print(f"  - {p[:80]}")
except Exception as e:
    print(f"JSON parse error: {e}")

# Show AnythingLLM source chunks
sources = raw.get("sources", [])
print(f"\n--- ANYTHINGLLM RETRIEVED CHUNKS: {len(sources)} ---")
for i, s in enumerate(sources[:8]):
    title = s.get("title", "?")
    chunk = s.get("chunkSource", "?")
    print(f"  [{i+1}] {title}")
    print(f"       chunk: {chunk}")
PYEOF
