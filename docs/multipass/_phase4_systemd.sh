#!/bin/bash
# Phase 4 Step 2: Deploy systemd service for vmdk_extractor.py
# Per V9 architecture lines 676-703
set -euo pipefail

USER_NAME=$(whoami)
USER_HOME=$(eval echo ~$USER_NAME)

echo "=== Phase 4 Step 2: Deploying systemd service ==="
echo "USER_NAME=$USER_NAME"
echo "USER_HOME=$USER_HOME"

# Write the systemd unit file
# CRITICAL: The ExecStopPost escaping is done carefully.
# Since we are writing directly from a bash script (not through
# sudo bash -c "cat <<EOF"), we use $$m for the systemd escaping.
# systemd reduces $$ to literal $ at runtime, so bash gets $m as loop var.
sudo tee /etc/systemd/system/manual-ingest.service > /dev/null << SVCEOF
[Unit]
Description=V8 Automotive Diagnostic Extraction Daemon
After=network.target

[Service]
Type=simple
User=$USER_NAME
ExecStart=$USER_HOME/diagnostic_engine/venv/bin/python3 $USER_HOME/diagnostic_engine/vmdk_extractor.py
ExecStopPost=/bin/bash -c 'for m in $USER_HOME/diagnostic_engine/staging/mounts/*; do guestunmount \$\$m 2>/dev/null || true; done; rm -rf --one-file-system $USER_HOME/diagnostic_engine/staging/mounts $USER_HOME/diagnostic_engine/staging/ova; mkdir -p $USER_HOME/diagnostic_engine/staging/mounts $USER_HOME/diagnostic_engine/staging/ova'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SVCEOF

echo ""
echo "=== Unit file written. Verifying ExecStopPost escaping ==="
sudo grep 'guestunmount' /etc/systemd/system/manual-ingest.service
echo ""

# Check for $$m (correct) vs $m (broken)
if sudo grep -q 'guestunmount \$\$m' /etc/systemd/system/manual-ingest.service; then
    echo "✅ PASS: ExecStopPost contains \$\$m (correct systemd escaping)"
else
    echo "❌ FAIL: ExecStopPost does NOT contain \$\$m — escaping is wrong!"
    exit 1
fi

echo ""
echo "=== Enabling and starting service ==="
sudo systemctl daemon-reload
sudo systemctl enable --now manual-ingest.service

sleep 3
echo ""
echo "=== Service status ==="
sudo systemctl status manual-ingest.service --no-pager -l

echo ""
echo "=== Phase 4 deployment complete ==="
