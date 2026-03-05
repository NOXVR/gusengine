#!/bin/bash
set -euo pipefail

echo "=== Diagnosing container networking ==="

echo ""
echo "--- FORWARD chain ---"
sudo iptables -L FORWARD -n -v | head -20

echo ""
echo "--- DOCKER-FORWARD chain ---"
sudo iptables -L DOCKER-FORWARD -n -v 2>/dev/null || echo "No DOCKER-FORWARD chain"

echo ""
echo "--- DOCKER-USER chain ---"
sudo iptables -L DOCKER-USER -n -v 2>/dev/null || echo "No DOCKER-USER chain"

echo ""
echo "--- NAT table (POSTROUTING for masquerade) ---"
sudo iptables -t nat -L POSTROUTING -n -v

echo ""
echo "--- Fix: Allow Docker bridge traffic in FORWARD chain ---"
# Docker bridge is docker0 (172.17.0.0/16)
# Allow outbound traffic from docker0 to any interface
sudo iptables -I DOCKER-FORWARD -i docker0 ! -o docker0 -j ACCEPT 2>/dev/null || \
  sudo iptables -I FORWARD -i docker0 ! -o docker0 -j ACCEPT

# Allow established/related return traffic
sudo iptables -I DOCKER-FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || \
  sudo iptables -I FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

echo ""
echo "--- Ensure MASQUERADE is set for docker0 ---"
sudo iptables -t nat -C POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE 2>/dev/null && echo "MASQUERADE already exists" || \
  (sudo iptables -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE && echo "Added MASQUERADE")

echo ""
echo "--- Post-fix FORWARD chain ---"
sudo iptables -L FORWARD -n -v | head -20

echo ""
echo "--- Testing container DNS ---"
docker exec diagnostic_rag_engine node -e "
const dns = require('dns');
dns.resolve('api.anthropic.com', (err, addresses) => {
  if (err) { console.error('DNS ERROR:', err.message); process.exit(1); }
  console.log('DNS OK:', addresses);
  process.exit(0);
});
setTimeout(() => { console.log('DNS TIMEOUT'); process.exit(1); }, 10000);
"

echo ""
echo "=== Done ==="
