#!/bin/bash
echo "=== 1. Host network check ==="
echo "Host can reach Anthropic:"
curl -s -o /dev/null -w "%{http_code}" https://api.anthropic.com/v1/messages -X POST 2>/dev/null || echo "FAIL"
echo ""

echo "=== 2. Docker network mode ==="
docker inspect diagnostic_rag_engine --format '{{.HostConfig.NetworkMode}}'

echo ""
echo "=== 3. Container DNS ==="
docker exec diagnostic_rag_engine cat /etc/resolv.conf 2>/dev/null || echo "Cannot read resolv.conf"

echo ""
echo "=== 4. Container can reach internet? ==="
docker exec diagnostic_rag_engine sh -c "wget -q -O /dev/null --timeout=5 https://api.anthropic.com 2>&1 && echo 'YES' || echo 'NO'" 2>/dev/null

echo ""
echo "=== 5. Container curl test ==="
docker exec diagnostic_rag_engine sh -c "curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 https://api.anthropic.com 2>/dev/null || echo 'curl not available, trying wget...'; wget -q -S --timeout=5 https://api.anthropic.com -O /dev/null 2>&1 | head -5" 2>/dev/null

echo ""
echo "=== 6. DNS resolution ==="
docker exec diagnostic_rag_engine sh -c "nslookup api.anthropic.com 2>/dev/null || getent hosts api.anthropic.com 2>/dev/null || echo 'DNS tools not available'" 2>/dev/null

echo ""
echo "=== 7. Container network interfaces ==="
docker exec diagnostic_rag_engine sh -c "ip addr 2>/dev/null || ifconfig 2>/dev/null || echo 'No network tools'" 2>/dev/null | head -20

echo ""
echo "=== 8. Docker run command (check network flag) ==="
docker inspect diagnostic_rag_engine --format '{{json .HostConfig.ExtraHosts}}'
echo ""
docker inspect diagnostic_rag_engine --format '{{json .HostConfig.Dns}}'

echo ""
echo "=== 9. iptables (VM host) ==="
sudo iptables -L DOCKER -n 2>/dev/null | head -10

echo ""
echo "=== Done ==="
