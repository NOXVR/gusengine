#!/bin/bash
set -euo pipefail

echo "=== PHASE 10: CRON JOBS ==="

# Backup cron: runs at 2 AM, stops container, backs up, restarts
BACKUP_CRON='0 2 * * * /usr/bin/docker stop diagnostic_rag_engine ; tar czf $HOME/diagnostic_engine_backup_$(date +\%Y\%m\%d).tar.gz --exclude=diagnostic_engine/staging -C $HOME diagnostic_engine/ ; /usr/bin/docker start diagnostic_rag_engine'

# Cleanup cron: runs at 3 AM, deletes backups older than 7 days
CLEANUP_CRON='0 3 * * * find $HOME/ -name '\''diagnostic_engine_backup_*.tar.gz'\'' -mtime +7 -exec rm {} \;'

# Install cron jobs (avoid duplicates)
CURRENT=$(crontab -l 2>/dev/null || true)

if echo "$CURRENT" | grep -q "diagnostic_engine_backup"; then
    echo "  Backup cron already exists, skipping"
else
    echo "$CURRENT
$BACKUP_CRON" | crontab -
    echo "  Added backup cron"
fi

CURRENT=$(crontab -l 2>/dev/null || true)
if echo "$CURRENT" | grep -q "diagnostic_engine_backup.*mtime"; then
    echo "  Cleanup cron already exists, skipping"
else
    echo "$CURRENT
$CLEANUP_CRON" | crontab -
    echo "  Added cleanup cron"
fi

echo ""
echo "=== Installed crontab ==="
crontab -l
echo ""
echo "=== Done ==="
