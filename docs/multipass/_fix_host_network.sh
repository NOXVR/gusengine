#!/bin/bash
set -euo pipefail

ENGINE_DIR="/home/ubuntu/diagnostic_engine"

echo "=== Recreating container with --network=host ==="

echo "--- Stopping current container ---"
docker stop diagnostic_rag_engine
docker rm diagnostic_rag_engine

echo ""
echo "--- Starting with host networking ---"
docker run -d \
  --name diagnostic_rag_engine \
  --network=host \
  --restart always \
  --log-opt max-size=50m \
  --log-opt max-file=3 \
  -v "$ENGINE_DIR/storage:/app/server/storage" \
  -v "$ENGINE_DIR/.env:/app/server/.env" \
  -v "$ENGINE_DIR/plugins:/app/server/storage/plugins" \
  -e STORAGE_DIR="/app/server/storage" \
  -e SERVER_PORT=3001 \
  mintplexlabs/anythingllm

echo ""
echo "--- Waiting for container to start ---"
sleep 10

echo ""
echo "--- Container status ---"
docker ps --format 'table {{.Names}}\t{{.Status}}'

echo ""
echo "--- Testing DNS from container ---"
docker exec diagnostic_rag_engine node -e "
const dns = require('dns');
dns.resolve('api.anthropic.com', (err, addresses) => {
  if (err) { console.error('DNS FAIL:', err.message); process.exit(1); }
  console.log('DNS OK:', addresses);

  const https = require('https');
  const req = https.request('https://api.anthropic.com/v1/messages', {method: 'POST', timeout: 10000}, (res) => {
    console.log('Anthropic reachable! HTTP', res.statusCode);
    process.exit(0);
  });
  req.on('error', (e) => { console.error('HTTP ERROR:', e.message); process.exit(1); });
  req.end();
});
setTimeout(() => { console.log('TIMEOUT'); process.exit(1); }, 15000);
"

echo ""
echo "--- Testing local API ---"
curl -s -H "Authorization: Bearer S14RWKG-6DC451B-KY6VXQB-SYV33BQ" http://127.0.0.1:3001/api/v1/auth

echo ""
echo "=== Done ==="
