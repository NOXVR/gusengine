#!/bin/bash
# Phase 7 FIX: Remaining settings + verify all
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

# ── FIX: Text Splitter (try different env var names) ──
echo "=== Fix 1: Text Splitter ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "TextSplitterPreference": "markdown-header",
    "TextSplitterChunkSize": "400",
    "TextSplitterChunkOverlap": "20"
  }')
echo "$RESULT"
echo ""

# ── FIX: Mistral OCR (fixed -X POST typo) ──
echo "=== Fix 2: Mistral OCR ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "DocumentProcessor": "mistral-ocr",
    "MistralApiKey": "9236104a-518a-44e3-9814-dfacb75201a9"
  }')
echo "$RESULT"
echo ""

# ── Configure workspace ──
echo "=== Step 3: Workspace settings ==="
WORKSPACE_SLUG="1975-mercedes-benz-450sl"
RESULT=$(curl -s -X POST "$BASE/workspace/$WORKSPACE_SLUG/update" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "similarityThreshold": 0.50,
    "topN": 4,
    "chatMode": "chat",
    "openAiHistory": 4
  }')
echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -30
echo ""

# ── FULL VERIFICATION ──
echo "=== VERIFICATION: Full system state ==="
curl -s "$BASE/system" -H "$AUTH" | python3 -c "
import sys, json
data = json.load(sys.stdin)
s = data.get('settings', {})
print('=== LLM Provider ===')
print(f'  LLMProvider:        {s.get(\"LLMProvider\")}')
print(f'  LLMModel:           {s.get(\"LLMModel\")}')
print()
print('=== Embedding ===')
print(f'  EmbeddingEngine:    {s.get(\"EmbeddingEngine\")}')
print(f'  EmbeddingModelPref: {s.get(\"EmbeddingModelPref\")}')
print(f'  VoyageAiApiKey:     {s.get(\"VoyageAiApiKey\")}')
print()
print('=== All Settings (for audit) ===')
for k in sorted(s.keys()):
    v = s[k]
    if v and v != 'false' and v is not False:
        print(f'  {k}: {v}')
"
echo ""

echo "=== Workspace details ==="
curl -s "$BASE/workspace/$WORKSPACE_SLUG" -H "$AUTH" | python3 -c "
import sys, json
data = json.load(sys.stdin)
ws = data.get('workspace', [])
if isinstance(ws, list) and ws:
    ws = ws[0]
elif isinstance(ws, dict):
    pass
else:
    print('No workspace data found')
    sys.exit(0)
for k in sorted(ws.keys()):
    if k not in ('documents',):
        print(f'  {k}: {ws[k]}')
" 2>/dev/null
echo ""

echo "=== Done ==="
