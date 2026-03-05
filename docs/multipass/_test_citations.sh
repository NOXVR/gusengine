#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"
SLUG="1975-mercedes-benz-450sl"

echo "=== Sending PHASE_B transition message ==="
RESPONSE=$(curl -s -X POST "$BASE/workspace/$SLUG/chat" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "{\"completed_state\": \"PHASE_A_TRIAGE\", \"required_next_state\": \"PHASE_B_FUNNEL\", \"selected_option\": \"[A] 1970s-1980s Mercedes-Benz with mechanical fuel injection (K-Jetronic / CIS)\", \"instruction\": \"User physically verified: [A]. You MUST transition to PHASE_B_FUNNEL. Do NOT repeat PHASE_A_TRIAGE.\"}",
    "mode": "chat"
  }')

echo "$RESPONSE" | python3 << 'PYEOF'
import sys, json
raw = json.load(sys.stdin)
text = raw.get("textResponse", "")
print("=== RAW RESPONSE TEXT ===")
print(text)
print("")

# Try to parse JSON from response
try:
    # Find the JSON object
    start = text.index("{")
    end = text.rindex("}") + 1
    parsed = json.loads(text[start:end])
    print("=== PARSED JSON ===")
    print(json.dumps(parsed, indent=2))
    print("")
    print("=== CITATION ANALYSIS ===")
    citations = parsed.get("source_citations", [])
    print(f"Number of citations: {len(citations)}")
    for i, c in enumerate(citations):
        print(f"  [{i+1}] source: {c.get('source', 'MISSING')}")
        print(f"       page: {c.get('page', 'MISSING')}")
        print(f"       context: {c.get('context', 'MISSING')}")
except Exception as e:
    print(f"Parse error: {e}")

# Also show sources field if present
sources = raw.get("sources", [])
if sources:
    print("")
    print("=== ANYTHINGLLM SOURCES (chunks retrieved) ===")
    for i, s in enumerate(sources[:5]):
        title = s.get("title", "?")
        chunk = s.get("chunkSource", "?")
        print(f"  [{i+1}] {title} | {chunk}")
PYEOF
