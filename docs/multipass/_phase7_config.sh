#!/bin/bash
# Phase 7: Configure ALL settings via AnythingLLM API
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

# ── STEP 1: Set LLM Provider (Anthropic) with Token Limit ──
echo "=== Step 1: Configuring Anthropic LLM ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "LLMProvider": "anthropic",
    "AnthropicApiKey": "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",
    "AnthropicModelPref": "claude-3-5-sonnet-latest"
  }')
echo "$RESULT"
echo ""

# ── STEP 2: Set Embedding Provider (Voyage AI) ──
echo "=== Step 2: Configuring Voyage AI Embedding ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "EmbeddingEngine": "voyageai",
    "VoyageAiApiKey": "pa-egIyOGpS5JoT45_hAnvHerJNOEg3oCXm4cF16i79Bnh",
    "EmbeddingModelPref": "voyage-3-large"
  }')
echo "$RESULT"
echo ""

# ── STEP 3: Set Text Splitter / Chunk Size ──
echo "=== Step 3: Configuring Text Splitter (400 tokens) ==="
RESULT=$(curl -s -X POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "TextSplitter": "markdown-header",
    "TextSplitterChunkSize": 400
  }')
echo "$RESULT"
echo ""

# ── STEP 4: Set Document Processing (Mistral OCR) ──
echo "=== Step 4: Configuring Mistral OCR ==="
RESULT=$(curl -s -x POST "$BASE/system/update-env" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "MistralApiKey": "9236104a-518a-44e3-9814-dfacb75201a9"
  }')
echo "$RESULT"
echo ""

# ── STEP 5: Verify settings took effect ──
echo "=== Step 5: Verifying current configuration ==="
curl -s "$BASE/system" -H "$AUTH" | python3 -c "
import sys, json
data = json.load(sys.stdin)
s = data.get('settings', {})
checks = {
    'LLMProvider': ('anthropic', s.get('LLMProvider')),
    'LLMModel': ('claude-3-5-sonnet', s.get('LLMModel', '')),
    'EmbeddingEngine': ('voyageai', s.get('EmbeddingEngine')),
    'EmbeddingModelPref': ('voyage-3-large', s.get('EmbeddingModelPref')),
    'VoyageAiApiKey': (True, s.get('VoyageAiApiKey')),
}
for key, (expected, actual) in checks.items():
    if isinstance(expected, bool):
        ok = bool(actual) == expected
    elif isinstance(expected, str):
        ok = expected in str(actual)
    else:
        ok = str(actual) == str(expected)
    status = '✅' if ok else '❌'
    print(f'  {status} {key}: {actual} (expected: {expected})')
"
echo ""

# ── STEP 6: Configure workspace settings ──
echo "=== Step 6: Configuring workspace settings ==="
WORKSPACE_SLUG="1975-mercedes-benz-450sl"
RESULT=$(curl -s -X POST "$BASE/workspace/$WORKSPACE_SLUG/update" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "similarityThreshold": 0.50,
    "topN": 4,
    "chatMode": "chat",
    "chatModel": "claude-3-5-sonnet-latest",
    "openAiHistory": 4
  }')
echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -20
echo ""

echo "=== Phase 7 API Configuration Complete ==="
