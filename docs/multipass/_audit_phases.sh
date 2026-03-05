#!/bin/bash
# Triple Validation Audit — Phases 1 & 2 vs ARCHITECTURE_FINAL_V9.md
set -u

PASS=0
FAIL=0
WARN=0

pass() { echo "  ✅ PASS: $1"; ((PASS++)); }
fail() { echo "  ❌ FAIL: $1"; ((FAIL++)); }
warn() { echo "  ⚠️  WARN: $1"; ((WARN++)); }

ENGINE_DIR="$HOME/diagnostic_engine"

echo "================================================================"
echo "  TRIPLE VALIDATION AUDIT — $(date)"
echo "  ENGINE_DIR=$ENGINE_DIR"
echo "================================================================"

# ── PHASE 1 STEP 1: Core Dependencies ──
echo ""
echo "── PHASE 1 STEP 1: CORE DEPENDENCIES ──"
echo "  Spec: curl git build-essential fuse3 libguestfs-tools python3-pip python3-venv tar jq nginx openssl lsof ufw"

REQUIRED_PKGS="curl git build-essential fuse3 libguestfs-tools python3-pip python3-venv tar jq nginx openssl lsof ufw"
for pkg in $REQUIRED_PKGS; do
  if dpkg -s "$pkg" &>/dev/null; then
    pass "$pkg installed"
  else
    fail "$pkg NOT installed"
  fi
done

# Check for packages we wrongly installed
echo ""
echo "  --- Extra packages check ---"
if dpkg -s certbot &>/dev/null; then warn "certbot installed (NOT in spec)"; fi
if dpkg -s python3-certbot-nginx &>/dev/null; then warn "python3-certbot-nginx installed (NOT in spec)"; fi
if dpkg -s python-magic &>/dev/null; then warn "python-magic installed via apt (NOT in spec)"; fi

# Spec says apt-get, not apt — cosmetic but noting
echo ""

# ── PHASE 1 STEP 2: Docker + Groups ──
echo "── PHASE 1 STEP 2: DOCKER + GROUPS ──"
if command -v docker &>/dev/null; then pass "Docker installed: $(docker --version)"; else fail "Docker NOT installed"; fi
if id -nG ubuntu | grep -qw docker; then pass "ubuntu in docker group"; else fail "ubuntu NOT in docker group"; fi
if id -nG ubuntu | grep -qw kvm; then pass "ubuntu in kvm group"; else fail "ubuntu NOT in kvm group (spec: sudo usermod -aG kvm)"; fi

# ── PHASE 1 STEP 3: UFW Firewall ──
echo ""
echo "── PHASE 1 STEP 3: UFW FIREWALL ──"
UFW_STATUS=$(sudo ufw status verbose 2>/dev/null)
if echo "$UFW_STATUS" | grep -q "Status: active"; then pass "UFW active"; else fail "UFW not active"; fi
if echo "$UFW_STATUS" | grep -q "deny (incoming)"; then pass "Default deny incoming"; else fail "Default NOT deny incoming"; fi
if echo "$UFW_STATUS" | grep -q "allow (outgoing)"; then pass "Default allow outgoing"; else fail "Default NOT allow outgoing"; fi
if echo "$UFW_STATUS" | grep -q "22/tcp"; then pass "Port 22/tcp allowed"; else fail "Port 22/tcp NOT allowed"; fi
if echo "$UFW_STATUS" | grep -q "80/tcp"; then pass "Port 80/tcp allowed"; else fail "Port 80/tcp NOT allowed"; fi
if echo "$UFW_STATUS" | grep -q "443/tcp"; then pass "Port 443/tcp allowed"; else fail "Port 443/tcp NOT allowed"; fi

# Spec does NOT allow 3001/tcp — we incorrectly added it
if echo "$UFW_STATUS" | grep -q "3001"; then fail "Port 3001 is allowed (NOT in spec — Docker binds 127.0.0.1 only)"; fi

# ── PHASE 1 STEP 4: File Structure ──
echo ""
echo "── PHASE 1 STEP 4: FILE STRUCTURE ──"
echo "  Spec ENGINE_DIR=\$HOME/diagnostic_engine"

# Check spec directories
SPEC_DIRS="$ENGINE_DIR/plugins/agent-skills/vin-lookup $ENGINE_DIR/plugins/agent-skills/manual-status $ENGINE_DIR/plugins/agent-skills/purchase-router $ENGINE_DIR/plugins/agent-skills/draft-tribal-knowledge $ENGINE_DIR/storage $ENGINE_DIR/downloads $ENGINE_DIR/extracted_manuals $ENGINE_DIR/quarantine $ENGINE_DIR/staging/ova $ENGINE_DIR/staging/mounts"

for d in $SPEC_DIRS; do
  if [ -d "$d" ]; then pass "Dir exists: ${d#$HOME/}"; else fail "Dir MISSING: ${d#$HOME/}"; fi
done

# Check for WRONG directories (we used /opt/gus/ structure)
if [ -d "/opt/gus" ]; then warn "/opt/gus exists (NOT in V9 spec — spec uses \$HOME/diagnostic_engine)"; fi
if [ -d "/opt/gus/quarantine" ]; then warn "/opt/gus/quarantine exists (wrong path)"; fi

# Venv
echo ""
echo "  --- Python Venv ---"
if [ -d "$ENGINE_DIR/venv" ]; then pass "venv exists at \$ENGINE_DIR/venv"; else fail "venv MISSING at \$ENGINE_DIR/venv"; fi

# Spec pip packages: PyMuPDF requests tiktoken (NOT watchdog, NOT python-magic)
if [ -f "$ENGINE_DIR/venv/bin/pip" ]; then
  PIP="$ENGINE_DIR/venv/bin/pip"
  for pypkg in PyMuPDF requests tiktoken; do
    if $PIP show "$pypkg" &>/dev/null; then pass "pip: $pypkg installed"; else fail "pip: $pypkg NOT installed"; fi
  done
  # Check for wrong packages
  if $PIP show watchdog &>/dev/null; then warn "pip: watchdog installed (V9 explicitly removed it — line 59)"; fi
  if $PIP show python-magic &>/dev/null; then warn "pip: python-magic installed (NOT in spec)"; fi
else
  fail "venv pip not found"
fi

# Wrong venv at /opt/gus/venv?
if [ -d "/opt/gus/venv" ]; then warn "/opt/gus/venv exists (wrong location)"; fi

# ── PHASE 1 STEP 5: JWT Secret ──
echo ""
echo "── PHASE 1 STEP 5: JWT SECRET / .env ──"
echo "  Spec: .env at \$ENGINE_DIR/.env with ONLY JWT_SECRET at this stage"

if [ -f "$ENGINE_DIR/.env" ]; then
  pass ".env exists at \$ENGINE_DIR/.env"
  ENV_PERMS=$(stat -c "%a" "$ENGINE_DIR/.env")
  if [ "$ENV_PERMS" = "600" ]; then pass ".env perms are 600"; else fail ".env perms are $ENV_PERMS (should be 600)"; fi
else
  fail ".env MISSING at \$ENGINE_DIR/.env"
fi

# Check for wrong .env at /opt/gus
if [ -f "/opt/gus/.env" ]; then warn ".env at /opt/gus/.env (wrong location)"; fi
if [ -f "/opt/gus/.jwt_secret" ]; then warn "JWT secret at /opt/gus/.jwt_secret (spec puts it inline in .env)"; fi

# ── PHASE 1 STEP 6: Nginx ──
echo ""
echo "── PHASE 1 STEP 6: NGINX ──"
NGINX_CONF="/etc/nginx/sites-available/default"
if [ -f "$NGINX_CONF" ]; then
  pass "Nginx config at $NGINX_CONF"
  # SSL
  if grep -q "listen 443 ssl" "$NGINX_CONF"; then pass "SSL listener on 443"; else fail "No SSL listener on 443"; fi
  if grep -q "listen 80" "$NGINX_CONF"; then pass "Port 80 listener"; else fail "No port 80 listener"; fi
  if grep -q "return 301" "$NGINX_CONF"; then pass "HTTP→HTTPS redirect"; else fail "No HTTP→HTTPS redirect"; fi
  # Security headers
  if grep -q "X-Content-Type-Options" "$NGINX_CONF"; then pass "X-Content-Type-Options header"; else fail "Missing X-Content-Type-Options"; fi
  if grep -q "X-Frame-Options" "$NGINX_CONF"; then pass "X-Frame-Options header"; else fail "Missing X-Frame-Options"; fi
  if grep -q "Referrer-Policy" "$NGINX_CONF"; then pass "Referrer-Policy header"; else fail "Missing Referrer-Policy"; fi
  if grep -q "proxy_hide_header X-Powered-By" "$NGINX_CONF"; then pass "X-Powered-By hidden"; else fail "X-Powered-By NOT hidden"; fi
  # Upload blocking
  if grep -q "upload\|create-folder" "$NGINX_CONF"; then pass "Upload/folder-creation blocking"; else fail "Upload blocking MISSING"; fi
  # client_max_body_size
  if grep -q "client_max_body_size 50M" "$NGINX_CONF"; then pass "client_max_body_size 50M"; else fail "client_max_body_size NOT 50M"; fi
  # X-Forwarded-For overwrite (not append)
  if grep -q 'X-Forwarded-For.*\$remote_addr' "$NGINX_CONF"; then pass "X-Forwarded-For uses \$remote_addr (overwrite)"; else fail "X-Forwarded-For may use \$proxy_add_x_forwarded_for (append — insecure)"; fi
  # proxy_pass to 127.0.0.1
  if grep -q "proxy_pass http://127.0.0.1:3001" "$NGINX_CONF"; then pass "proxy_pass to 127.0.0.1:3001"; else fail "proxy_pass NOT to 127.0.0.1:3001"; fi
  # Timeout
  if grep -q "proxy_read_timeout 86400s" "$NGINX_CONF"; then pass "proxy_read_timeout 86400s"; else fail "proxy_read_timeout missing or wrong"; fi
else
  fail "Nginx config NOT at /etc/nginx/sites-available/default"
fi

# SSL certs
if [ -f "/etc/nginx/ssl/diag-engine.key" ]; then pass "SSL key exists"; else fail "SSL key MISSING"; fi
if [ -f "/etc/nginx/ssl/diag-engine.crt" ]; then pass "SSL cert exists"; else fail "SSL cert MISSING"; fi
KEY_PERMS=$(stat -c "%a" "/etc/nginx/ssl/diag-engine.key" 2>/dev/null)
if [ "$KEY_PERMS" = "600" ]; then pass "SSL key perms 600"; else fail "SSL key perms $KEY_PERMS (should be 600)"; fi
CERT_PERMS=$(stat -c "%a" "/etc/nginx/ssl/diag-engine.crt" 2>/dev/null)
if [ "$CERT_PERMS" = "644" ]; then pass "SSL cert perms 644"; else fail "SSL cert perms $CERT_PERMS (should be 644)"; fi

# Check for old gus-engine nginx config
if [ -f "/etc/nginx/sites-available/gus-engine" ]; then warn "Old gus-engine nginx config exists (should be 'default' per spec)"; fi
if [ -L "/etc/nginx/sites-enabled/gus-engine" ]; then warn "Old gus-engine symlink in sites-enabled"; fi

echo ""
echo "── PHASE 2: DOCKER ORCHESTRATION ──"
# Container name
CONTAINER="diagnostic_rag_engine"
if docker ps --filter "name=$CONTAINER" --format '{{.Names}}' | grep -q "$CONTAINER"; then
  pass "Container $CONTAINER running"
  STATUS=$(docker ps --filter "name=$CONTAINER" --format '{{.Status}}')
  echo "       Status: $STATUS"
else
  fail "Container $CONTAINER NOT running"
fi

# Check container config
echo ""
echo "  --- Docker run flags ---"
INSPECT=$(docker inspect $CONTAINER 2>/dev/null)
if echo "$INSPECT" | grep -q '"127.0.0.1"'; then pass "Port bound to 127.0.0.1 (not 0.0.0.0)"; else fail "Port NOT bound to 127.0.0.1 (security risk)"; fi
if echo "$INSPECT" | grep -q '"RestartPolicy"' && echo "$INSPECT" | grep -q '"always"'; then pass "Restart policy: always"; else fail "Restart policy NOT 'always'"; fi

# Log rotation
LOG_CONFIG=$(docker inspect --format '{{json .HostConfig.LogConfig}}' $CONTAINER 2>/dev/null)
if echo "$LOG_CONFIG" | grep -q "max-size"; then pass "Log rotation: max-size configured"; else fail "Log rotation: max-size MISSING"; fi
if echo "$LOG_CONFIG" | grep -q "max-file"; then pass "Log rotation: max-file configured"; else fail "Log rotation: max-file MISSING"; fi

# Volume mounts
echo ""
echo "  --- Volume mounts ---"
MOUNTS=$(docker inspect --format '{{json .Mounts}}' $CONTAINER 2>/dev/null)
if echo "$MOUNTS" | grep -q "/app/server/storage"; then pass "Volume: storage mounted"; else fail "Volume: storage NOT mounted"; fi
if echo "$MOUNTS" | grep -q "/app/server/.env"; then pass "Volume: .env mounted"; else fail "Volume: .env NOT mounted"; fi
if echo "$MOUNTS" | grep -q "extracted_manuals"; then pass "Volume: extracted_manuals mounted"; else fail "Volume: extracted_manuals NOT mounted"; fi
if echo "$MOUNTS" | grep -q "agent-skills"; then pass "Volume: agent-skills mounted"; else fail "Volume: agent-skills NOT mounted"; fi

# extracted_manuals should be :ro
if echo "$MOUNTS" | grep -q '"RW":false' || docker inspect --format '{{range .Mounts}}{{if eq .Destination "/app/server/extracted_manuals"}}{{.RW}}{{end}}{{end}}' $CONTAINER 2>/dev/null | grep -q "false"; then
  pass "extracted_manuals is read-only"
else
  warn "extracted_manuals may not be read-only (spec says :ro)"
fi

# .env contents
echo ""
echo "  --- .env contents audit ---"
if [ -f "$ENGINE_DIR/.env" ]; then
  echo "  Current .env:"
  cat "$ENGINE_DIR/.env"
  echo ""
  # Check for required keys
  grep -q "^JWT_SECRET=" "$ENGINE_DIR/.env" && pass ".env has JWT_SECRET" || fail ".env MISSING JWT_SECRET"
  grep -q "^STORAGE_DIR=" "$ENGINE_DIR/.env" && pass ".env has STORAGE_DIR" || warn ".env missing STORAGE_DIR"
  grep -q "^SERVER_PORT=" "$ENGINE_DIR/.env" && pass ".env has SERVER_PORT" || warn ".env missing SERVER_PORT"
  grep -q "^SIG_KEY=" "$ENGINE_DIR/.env" && pass ".env has SIG_KEY" || fail ".env MISSING SIG_KEY"
  grep -q "^SIG_SALT=" "$ENGINE_DIR/.env" && pass ".env has SIG_SALT" || fail ".env MISSING SIG_SALT"

  # Duplicate check
  DUPES=$(grep -v '^#' "$ENGINE_DIR/.env" | grep -v '^$' | awk -F= '{print $1}' | sort | uniq -d)
  if [ -z "$DUPES" ]; then pass "No duplicate .env keys"; else fail "Duplicate .env keys: $DUPES"; fi
fi

# Web access check
echo ""
echo "  --- Web access check ---"
HTTP_CODE=$(curl -sk -o /dev/null -w '%{http_code}' https://localhost 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then pass "HTTPS returns 200"; else warn "HTTPS returns $HTTP_CODE"; fi

HTTP_REDIR=$(curl -s -o /dev/null -w '%{http_code}' http://localhost 2>/dev/null)
if [ "$HTTP_REDIR" = "301" ]; then pass "HTTP returns 301 redirect"; else warn "HTTP returns $HTTP_REDIR (expected 301)"; fi

echo ""
echo "================================================================"
echo "  AUDIT COMPLETE"
echo "  ✅ PASS: $PASS"
echo "  ❌ FAIL: $FAIL"
echo "  ⚠️  WARN: $WARN"
echo "================================================================"
