#!/bin/bash
set -euo pipefail

ENGINE_DIR="/home/ubuntu/diagnostic_engine"
# The API key is valid but INTERNAL_API_KEY line was overwritten
# by AnythingLLM's env-dump. Using the known key directly.
INTERNAL_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"

echo "=== PHASE 9: AGENT SKILLS ==="

# @Manual-Status (needs API key injection)
mkdir -p "$ENGINE_DIR/plugins/agent-skills/manual-status"
echo '{"name":"Manual-Status","hubId":"manual-status","version":"1.0.0","schema":"skill-1.0.0","imported":true,"active":true,"description":"Verify FSM index status in database","entrypoint":{"file":"handler.js","params":{"workspace_slug":{"type":"string","required":true}}}}' > "$ENGINE_DIR/plugins/agent-skills/manual-status/plugin.json"

cat > "$ENGINE_DIR/plugins/agent-skills/manual-status/handler.js" << 'HEOF'
module.exports.runtime = {
  handler: async function ({ workspace_slug }) {
    try {
      const response = await fetch(`http://127.0.0.1:3001/api/v1/workspace/${workspace_slug}`, {
        headers: { "Authorization": "Bearer REPLACE_ME_KEY" }
      });
      const data = await response.json();
      if (data.workspace && data.workspace.documents.length > 0)
        return `SUCCESS: ${data.workspace.documents.length} document chunks verified.`;
      return `CRITICAL: No documentation found.`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
HEOF
sed -i "s/REPLACE_ME_KEY/$INTERNAL_KEY/g" "$ENGINE_DIR/plugins/agent-skills/manual-status/handler.js"
echo "  Done: @Manual-Status"

# @VIN-Lookup
mkdir -p "$ENGINE_DIR/plugins/agent-skills/vin-lookup"
echo '{"name":"VIN-Lookup","hubId":"vin-lookup","version":"1.0.0","schema":"skill-1.0.0","imported":true,"active":true,"description":"Decodes VINs or Chassis Codes","entrypoint":{"file":"handler.js","params":{"vin":{"description":"17-digit VIN or legacy chassis code","type":"string","required":true}}}}' > "$ENGINE_DIR/plugins/agent-skills/vin-lookup/plugin.json"

cat > "$ENGINE_DIR/plugins/agent-skills/vin-lookup/handler.js" << 'HEOF'
module.exports.runtime = {
  handler: async function ({ vin }) {
    if (!vin || vin.length < 5) return "Error: Invalid VIN.";
    if (vin.length < 17) return `CLASSIC CHASSIS IDENTIFIED: ${vin}. Bypassing NHTSA API. Lock workspace manually.`;
    try {
      const response = await fetch(`https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/${encodeURIComponent(vin)}?format=json`);
      const data = await response.json();
      const res = data.Results[0];
      if (res.ErrorCode !== "0" && res.ErrorCode !== "") return `API Error: ${res.ErrorText}`;
      return `VEHICLE: ${res.ModelYear} ${res.Make} ${res.Model}. ENGINE: ${res.DisplacementL}L. METADATA LOCK ENFORCED.`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
HEOF
echo "  Done: @VIN-Lookup"

# @Purchase-Router
mkdir -p "$ENGINE_DIR/plugins/agent-skills/purchase-router"
echo '{"name":"Purchase-Router","hubId":"purchase-router","version":"1.0.0","schema":"skill-1.0.0","imported":true,"active":true,"description":"Acquire missing FSMs","entrypoint":{"file":"handler.js","params":{"vehicle_data":{"description":"Year make model","type":"string","required":true}}}}' > "$ENGINE_DIR/plugins/agent-skills/purchase-router/plugin.json"

cat > "$ENGINE_DIR/plugins/agent-skills/purchase-router/handler.js" << 'HEOF'
module.exports.runtime = {
  handler: async function ({ vehicle_data }) {
    try {
      const query = encodeURIComponent(`${vehicle_data} factory service manual OEM PDF`);
      return `DOCUMENTATION MISSING. Secure OEM files here:\n- Factory-Manuals: https://factory-manuals.com/search?q=${query}\n- eManualOnline: https://www.emanualonline.com/search.html?q=${query}`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
HEOF
echo "  Done: @Purchase-Router"

# @Draft-Tribal-Knowledge
mkdir -p "$ENGINE_DIR/plugins/agent-skills/draft-tribal-knowledge"
echo '{"name":"Draft-Tribal-Knowledge","hubId":"draft-tribal-knowledge","version":"1.0.0","schema":"skill-1.0.0","imported":true,"active":true,"description":"Drafts undocumented fix for Manager approval","entrypoint":{"file":"handler.js","params":{"symptom":{"description":"Exact vehicle symptom.","type":"string","required":true},"fix":{"description":"The undocumented fix.","type":"string","required":true}}}}' > "$ENGINE_DIR/plugins/agent-skills/draft-tribal-knowledge/plugin.json"

cat > "$ENGINE_DIR/plugins/agent-skills/draft-tribal-knowledge/handler.js" << 'HEOF'
module.exports.runtime = {
  handler: async function ({ symptom, fix }) {
    try {
      return `### TRIBAL KNOWLEDGE DRAFT ###\n\n**SHOP MANAGER ACTION REQUIRED:**\nReview the following fix. Copy into pinned MASTER_LEDGER.md:\n\n## FAULT SIGNATURE: ${symptom}\n- **MASTER TECH OVERRIDE:** ${fix}\n\n*STATUS: Pending QA Review.*`;
    } catch (e) { return `ERROR: ${e.message}`; }
  }
};
HEOF
echo "  Done: @Draft-Tribal-Knowledge"

echo ""
echo "--- Restarting Docker ---"
docker restart diagnostic_rag_engine
sleep 5

echo ""
echo "=== Verify ==="
for s in manual-status vin-lookup purchase-router draft-tribal-knowledge; do
    if [ -f "$ENGINE_DIR/plugins/agent-skills/$s/plugin.json" ] && [ -f "$ENGINE_DIR/plugins/agent-skills/$s/handler.js" ]; then
        echo "  OK: $s"
    else
        echo "  FAIL: $s"
    fi
done
if grep -q "REPLACE_ME_KEY" "$ENGINE_DIR/plugins/agent-skills/manual-status/handler.js"; then
    echo "  FAIL: key not injected"
else
    echo "  OK: API key injected"
fi

echo ""
echo "=== PHASE 10: CRON ==="
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/bin/docker stop diagnostic_rag_engine ; tar czf \$HOME/diagnostic_engine_backup_\$(date +\%Y\%m\%d).tar.gz --exclude=diagnostic_engine/staging -C \$HOME diagnostic_engine/ ; /usr/bin/docker start diagnostic_rag_engine") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * * find \$HOME/ -name 'diagnostic_engine_backup_*.tar.gz' -mtime +7 -exec rm {} \;") | crontab -
echo "Crontab:"
crontab -l

echo ""
docker ps --format 'table {{.Names}}\t{{.Status}}'
echo ""
echo "=== DONE ==="
