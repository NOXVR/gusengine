#!/bin/bash
echo "=== iptables DOCKER chain after fix ==="
sudo iptables -L DOCKER -n

echo ""
echo "=== Testing container outbound via Node.js ==="
docker exec diagnostic_rag_engine node -e "
const https = require('https');
const req = https.request('https://api.anthropic.com/v1/messages', {method: 'POST', timeout: 10000}, (res) => {
  console.log('Anthropic reachable! HTTP', res.statusCode);
  process.exit(0);
});
req.on('error', (e) => {
  console.error('ERROR:', e.message);
  process.exit(1);
});
req.end();
setTimeout(() => { console.log('TIMEOUT after 15s'); process.exit(1); }, 15000);
"
echo ""
echo "=== Done ==="
