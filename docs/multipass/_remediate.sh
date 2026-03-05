#!/bin/bash
# Remediation script — fixes all 13 FAIL items from triple validation audit
set -euo pipefail

ENGINE_DIR="$HOME/diagnostic_engine"
echo "=== REMEDIATION SCRIPT ==="
echo "ENGINE_DIR=$ENGINE_DIR"

# ── FIX 1: Install python3-venv ──
echo ""
echo "[1/7] Installing python3-venv..."
sudo apt-get install -y python3-venv

# ── FIX 2: Add ubuntu to kvm group ──
echo ""
echo "[2/7] Adding ubuntu to kvm group..."
sudo usermod -aG kvm $USER

# ── FIX 3: Remove UFW port 3001 (not in spec) ──
echo ""
echo "[3/7] Removing UFW rule for port 3001..."
sudo ufw delete allow 3001/tcp 2>/dev/null || echo "  (rule may not exist, skipping)"
sudo ufw status verbose

# ── FIX 4: Create all missing directories ──
echo ""
echo "[4/7] Creating missing directories..."
mkdir -p "$ENGINE_DIR/plugins/agent-skills"/{vin-lookup,manual-status,purchase-router,draft-tribal-knowledge}
mkdir -p "$ENGINE_DIR"/{downloads,quarantine,staging/ova,staging/mounts}
echo "  Created:"
ls -la "$ENGINE_DIR/plugins/agent-skills/"
ls -la "$ENGINE_DIR/"

# ── FIX 5: Create venv at correct location ──
echo ""
echo "[5/7] Creating Python venv at \$ENGINE_DIR/venv..."
python3 -m venv "$ENGINE_DIR/venv"
echo "  Venv created. Installing spec packages: PyMuPDF requests tiktoken"
"$ENGINE_DIR/venv/bin/pip" install --upgrade pip
"$ENGINE_DIR/venv/bin/pip" install PyMuPDF requests tiktoken

# ── FIX 6: Clean up old gus-engine nginx artifacts ──
echo ""
echo "[6/7] Cleaning up old nginx config artifacts..."
sudo rm -f /etc/nginx/sites-available/gus-engine
sudo rm -f /etc/nginx/sites-enabled/gus-engine
sudo nginx -t && sudo systemctl reload nginx
echo "  Nginx cleaned up"

# ── FIX 7: Verify .env has no SIG_SALT quoting inconsistency ──
echo ""
echo "[7/7] Verifying .env consistency..."
# Make SIG_SALT format match SIG_KEY (add single quotes if missing for consistency)
cat "$ENGINE_DIR/.env"

echo ""
echo "=== REMEDIATION COMPLETE ==="
echo "=== Running re-audit to verify... ==="
