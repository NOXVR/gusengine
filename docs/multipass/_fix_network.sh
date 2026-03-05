#!/bin/bash
set -euo pipefail

echo "=== Fixing Docker container outbound connectivity ==="

echo ""
echo "--- Current iptables DOCKER chain ---"
sudo iptables -L DOCKER -n -v

echo ""
echo "--- Checking DOCKER-ISOLATION and FORWARD chains ---"
sudo iptables -L FORWARD -n -v | head -20

echo ""
echo "--- Fix: Allow established outbound from container ---"
# The DROP rule in DOCKER chain is too aggressive.
# We need to allow outbound connections from the container.
# Delete the DROP all rule
sudo iptables -D DOCKER -j DROP 2>/dev/null || echo "No DROP rule to delete (already removed)"

echo ""
echo "--- Post-fix iptables DOCKER chain ---"
sudo iptables -L DOCKER -n -v

echo ""
echo "--- Testing container outbound (via host curl to see if container can make DNS+HTTP) ---"
# Test from inside the container using node (since curl/wget aren't available)
docker exec diagnostic_rag_engine node -e "
const https = require('https');
const req = https.request('https://api.anthropic.com/v1/messages', {method: 'POST', timeout: 10000}, (res) => {
  console.log('STATUS:', res.statusCode);
  process.exit(0);
});
req.on('error', (e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
req.end();
setTimeout(() => { console.log('TIMEOUT'); process.exit(1); }, 15000);
"

echo ""
echo "=== Done ==="
