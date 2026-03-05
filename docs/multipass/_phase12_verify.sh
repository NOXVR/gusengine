#!/bin/bash
# Phase 12: Full Post-Deployment Verification Checklist

echo "====================================================================="
echo "  V9 POST-DEPLOYMENT VERIFICATION — $(date)"
echo "====================================================================="
echo ""

# 1. Systemd daemon
echo "--- 1. Systemd daemon (manual-ingest.service) ---"
STATUS=$(sudo systemctl is-active manual-ingest.service 2>/dev/null || echo "inactive")
echo "  Status: $STATUS"
if [ "$STATUS" = "active" ]; then echo "  ✅ PASS"; else echo "  ❌ FAIL"; fi
echo ""

# 2. Docker container
echo "--- 2. Docker container ---"
DOCKER=$(docker ps --format '{{.Names}} {{.Status}}' | grep diagnostic_rag_engine)
echo "  $DOCKER"
if echo "$DOCKER" | grep -q "Up"; then echo "  ✅ PASS"; else echo "  ❌ FAIL"; fi
echo ""

# 3. API key
echo "--- 3. API key authentication ---"
AUTH_RESULT=$(curl -s -H "Authorization: Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ" http://127.0.0.1:3001/api/v1/auth)
echo "  $AUTH_RESULT"
if echo "$AUTH_RESULT" | grep -q "authenticated.*true"; then echo "  ✅ PASS"; else echo "  ❌ FAIL"; fi
echo ""

# 4. Nginx blocks external uploads (via localhost to test the config)
echo "--- 4. Nginx upload block (localhost test) ---"
UPLOAD_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST https://127.0.0.1/api/v1/document/upload --insecure 2>/dev/null)
echo "  POST /api/v1/document/upload -> HTTP $UPLOAD_CODE"
if [ "$UPLOAD_CODE" = "403" ]; then echo "  ✅ PASS"; else echo "  ⚠️  Expected 403, got $UPLOAD_CODE"; fi
UPLOAD_CODE_CASE=$(curl -s -o /dev/null -w "%{http_code}" -X POST https://127.0.0.1/api/v1/document/UpLoad --insecure 2>/dev/null)
echo "  POST /api/v1/document/UpLoad -> HTTP $UPLOAD_CODE_CASE"
if [ "$UPLOAD_CODE_CASE" = "403" ]; then echo "  ✅ PASS (case-insensitive)"; else echo "  ⚠️  Expected 403"; fi
echo ""

# 5. UFW
echo "--- 5. UFW status ---"
sudo ufw status | head -10
echo ""

# 6. ExecStopPost escaping
echo "--- 6. ExecStopPost escaping ---"
EXEC_LINE=$(sudo grep 'guestunmount' /etc/systemd/system/manual-ingest.service 2>/dev/null || echo "NOT FOUND")
echo "  $EXEC_LINE"
if echo "$EXEC_LINE" | grep -q '$$m'; then echo "  ✅ PASS ($$m correct)"; else echo "  ❌ FAIL"; fi
echo ""

# 7. .env permissions
echo "--- 7. .env permissions ---"
PERMS=$(stat -c '%a' /home/ubuntu/diagnostic_engine/.env 2>/dev/null || echo "unknown")
echo "  Permissions: $PERMS"
if [ "$PERMS" = "600" ]; then echo "  ✅ PASS"; else echo "  ⚠️  Expected 600, got $PERMS (fixing...)"; chmod 600 /home/ubuntu/diagnostic_engine/.env; fi
echo ""

# 8. TLS key permissions
echo "--- 8. TLS key permissions ---"
if [ -f /etc/nginx/ssl/diag-engine.key ]; then
    TLS_PERMS=$(stat -c '%a' /etc/nginx/ssl/diag-engine.key)
    echo "  Permissions: $TLS_PERMS"
    if [ "$TLS_PERMS" = "600" ]; then echo "  ✅ PASS"; else echo "  ⚠️  Expected 600"; fi
else
    echo "  ⚠️  TLS key not found at expected path"
fi
echo ""

# 9. Docker log rotation
echo "--- 9. Docker log rotation ---"
LOG_CONFIG=$(docker inspect diagnostic_rag_engine --format '{{.HostConfig.LogConfig}}' 2>/dev/null)
echo "  $LOG_CONFIG"
if echo "$LOG_CONFIG" | grep -q "max-size"; then echo "  ✅ PASS"; else echo "  ⚠️  Log rotation not configured"; fi
echo ""

# 10. Cron jobs
echo "--- 10. Cron jobs ---"
CRON=$(crontab -l 2>/dev/null)
echo "$CRON"
if echo "$CRON" | grep -q "diagnostic_rag_engine.*tar"; then echo "  ✅ PASS (backup)"; else echo "  ❌ FAIL (backup)"; fi
if echo "$CRON" | grep -q "mtime.*-exec"; then echo "  ✅ PASS (cleanup)"; else echo "  ❌ FAIL (cleanup)"; fi
echo ""

# 11. Agent skills
echo "--- 11. Agent skills ---"
for s in manual-status vin-lookup purchase-router draft-tribal-knowledge; do
    if [ -f "/home/ubuntu/diagnostic_engine/plugins/agent-skills/$s/plugin.json" ]; then
        echo "  ✅ $s"
    else
        echo "  ❌ $s MISSING"
    fi
done
echo ""

# 12. System prompt
echo "--- 12. System prompt ---"
PROMPT_LEN=$(curl -s "http://127.0.0.1:3001/api/v1/workspace/1975-mercedes-benz-450sl" -H "Authorization: Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ" | python3 -c "import sys,json;ws=json.load(sys.stdin).get('workspace',{});print(len(ws.get('openAiPrompt','')))")
echo "  Prompt length: $PROMPT_LEN chars"
if [ "$PROMPT_LEN" -gt 3000 ]; then echo "  ✅ PASS"; else echo "  ❌ FAIL"; fi
echo ""

# 13. LLM/Embedding config
echo "--- 13. LLM + Embedding config ---"
curl -s "http://127.0.0.1:3001/api/v1/system" -H "Authorization: Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ" | python3 -c "
import sys,json
s=json.load(sys.stdin).get('settings',{})
checks=[
    ('LLMProvider', 'anthropic'),
    ('AnthropicModelPref', 'claude-3-5-sonnet'),
    ('EmbeddingEngine', 'voyageai'),
    ('EmbeddingModelPref', 'voyage-3-large'),
    ('CohereModelPref', 'rerank-english-v3.0'),
]
for key, want in checks:
    val = str(s.get(key, ''))
    ok = want in val
    print(f'  {\"✅\" if ok else \"❌\"} {key}: {val}')
"
echo ""

echo "====================================================================="
echo "  VERIFICATION COMPLETE"
echo "====================================================================="
