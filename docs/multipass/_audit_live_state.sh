#!/bin/bash
set -euo pipefail

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"
AUTH="Authorization: Bearer $API_KEY"

echo "================================================================"
echo "PHASE 7-10 AEROSPACE VALIDATION AUDIT — LIVE STATE DUMP"
echo "================================================================"

echo ""
echo "=== 1. RAW WORKSPACE API RESPONSE (first 3000 chars) ==="
curl -s "$BASE/workspace/1975-mercedes-benz-450sl" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
# Navigate the response structure
if isinstance(raw, dict) and 'workspace' in raw:
    d = raw['workspace']
    if isinstance(d, list):
        d = d[0] if d else {}
elif isinstance(raw, list):
    d = raw[0] if raw else {}
else:
    d = raw

keys = ['name','slug','similarityThreshold','topN','chatMode','chatModel',
        'openAiTemp','openAiHistory','chatProvider','agentProvider','agentModel']
for k in keys:
    print(f'  {k}: {d.get(k)!r}')
prompt = d.get('openAiPrompt','') or ''
print(f'  systemPrompt length: {len(prompt)} chars')
print(f'  systemPrompt first 120 chars: {prompt[:120]!r}')
print(f'  systemPrompt last 80 chars: {prompt[-80:]!r}')
"

echo ""
echo "=== 2. SYSTEM SETTINGS (Phase 7 relevant) ==="
curl -s "$BASE/system" -H "$AUTH" | python3 -c "
import sys, json
s = json.load(sys.stdin)['settings']
checks = {
    'LLMProvider': 'anthropic',
    'AnthropicModelPref': 'claude-sonnet-4-6',
    'AnthropicApiKey': True,
    'EmbeddingEngine': 'voyageai',
    'EmbeddingModelPref': 'voyage-3-large',
    'VoyageAiApiKey': True,
    'MistralApiKey': True,
    'CohereApiKey': True,
    'CohereModelPref': 'rerank-english-v3.0',
}
for k, expected in checks.items():
    actual = s.get(k)
    status = 'PASS' if actual == expected else 'DEVIATION'
    print(f'  {k}: {actual!r} (expected: {expected!r}) [{status}]')
"

echo ""
echo "=== 3. TEXT SPLITTER / ADMIN PREFS ==="
curl -s "$BASE/admin/system-preferences" -H "$AUTH" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    prefs = d.get('settings', d)
    if isinstance(prefs, dict):
        for k in sorted(prefs.keys()):
            kl = k.lower()
            if 'text' in kl or 'chunk' in kl or 'splitter' in kl or 'ocr' in kl or 'document' in kl:
                print(f'  {k}: {prefs[k]!r}')
    else:
        print(f'  Raw: {str(prefs)[:500]}')
except Exception as e:
    print(f'  Error: {e}')
"

echo ""
echo "=== 4. AGENT SKILLS ==="
for skill in manual-status vin-lookup purchase-router draft-tribal-knowledge; do
    echo "  --- Skill: $skill ---"
    SKILL_DIR="$HOME/diagnostic_engine/plugins/agent-skills/$skill"
    if [ -d "$SKILL_DIR" ]; then
        echo "  plugin.json exists: YES"
        echo "  handler.js exists: $(test -f $SKILL_DIR/handler.js && echo YES || echo NO)"
        echo "  handler.js content:"
        cat "$SKILL_DIR/handler.js" 2>/dev/null | sed 's/^/    /' || echo "    EMPTY"
    else
        echo "  DIRECTORY NOT FOUND"
    fi
done

echo ""
echo "=== 5. FULL SYSTEM PROMPT ==="
curl -s "$BASE/workspace/1975-mercedes-benz-450sl" -H "$AUTH" | python3 -c "
import sys, json
raw = json.load(sys.stdin)
if isinstance(raw, dict) and 'workspace' in raw:
    d = raw['workspace']
    if isinstance(d, list):
        d = d[0] if d else {}
elif isinstance(raw, list):
    d = raw[0] if raw else {}
else:
    d = raw
prompt = d.get('openAiPrompt','') or ''
print(prompt)
"

echo ""
echo "=== 6. DOCKER CONFIG ==="
docker inspect diagnostic_rag_engine --format 'LogConfig: {{.HostConfig.LogConfig}}
NetworkMode: {{.HostConfig.NetworkMode}}
RestartPolicy: {{.HostConfig.RestartPolicy.Name}}
Image: {{.Config.Image}}'

echo ""
echo "=== 7. CRON JOBS ==="
crontab -l 2>/dev/null || echo "No crontab"

echo ""
echo "=== AUDIT DUMP COMPLETE ==="
