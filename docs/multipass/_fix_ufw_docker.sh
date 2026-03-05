#!/bin/bash
set -euo pipefail

echo "=== Fixing UFW + Docker conflict ==="

# Check current ufw-before-forward
echo "--- ufw-before-forward chain ---"
sudo iptables -L ufw-before-forward -n -v

echo ""
echo "--- ufw-reject-forward chain ---"
sudo iptables -L ufw-reject-forward -n -v

echo ""
echo "--- Fix: Add ACCEPT rules to ufw-before-forward for Docker ---"
# Allow outbound from docker0
sudo iptables -I ufw-before-forward -i docker0 ! -o docker0 -j ACCEPT
# Allow established/related return traffic to docker0
sudo iptables -I ufw-before-forward -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

echo ""
echo "--- Post-fix ufw-before-forward ---"
sudo iptables -L ufw-before-forward -n -v

echo ""
echo "--- Make persistent: add to /etc/ufw/before.rules ---"
# Check if already patched
if grep -q "docker0" /etc/ufw/before.rules; then
    echo "Already patched"
else
    # Insert before the COMMIT line in the filter table
    sudo sed -i '/^COMMIT$/i # Docker bridge forwarding\n-A ufw-before-forward -i docker0 ! -o docker0 -j ACCEPT\n-A ufw-before-forward -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT' /etc/ufw/before.rules
    echo "Patched /etc/ufw/before.rules"
fi

echo ""
echo "--- Testing container DNS ---"
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
  req.on('error', (e) => {
    console.error('HTTP ERROR:', e.message);
    process.exit(1);
  });
  req.end();
});
setTimeout(() => { console.log('TIMEOUT'); process.exit(1); }, 15000);
"

echo ""
echo "=== Done ==="
