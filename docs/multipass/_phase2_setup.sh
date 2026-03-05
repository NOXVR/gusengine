#!/bin/bash
set -euo pipefail

ENGINE_DIR="$HOME/diagnostic_engine"
echo "=== Phase 2: Docker Orchestration ==="
echo "ENGINE_DIR=$ENGINE_DIR"

# Ensure storage dir is writable by container
chmod 777 "$ENGINE_DIR/storage"

# Create the custom .env with our JWT secret
JWT_VAL=$(cat /opt/gus/.jwt_secret)
echo "JWT_SECRET=$JWT_VAL" > "$ENGINE_DIR/.env.custom"

# Merge: defaults first, then custom overrides appended
cp "$ENGINE_DIR/.env.defaults" "$ENGINE_DIR/.env"
cat "$ENGINE_DIR/.env.custom" >> "$ENGINE_DIR/.env"
chmod 600 "$ENGINE_DIR/.env"

# Verify no duplicate keys
echo "=== Duplicate key check (should be empty) ==="
sort "$ENGINE_DIR/.env" | grep -v '^#' | grep -v '^$' | awk -F= '{print $1}' | sort | uniq -d || true

echo "=== Final .env ==="
cat "$ENGINE_DIR/.env"

# Remove temp container
docker rm -f temp_llm 2>/dev/null || true

# Launch Production Engine per V9 spec
echo ""
echo "=== Launching production container ==="
docker run -d -p 127.0.0.1:3001:3001 \
  --name diagnostic_rag_engine \
  --log-opt max-size=50m --log-opt max-file=3 \
  -v "$ENGINE_DIR/storage:/app/server/storage" \
  -v "$ENGINE_DIR/.env:/app/server/.env" \
  -v "$ENGINE_DIR/extracted_manuals:/app/server/extracted_manuals:ro" \
  -v "$ENGINE_DIR/plugins/agent-skills:/app/server/storage/plugins/agent-skills" \
  -e STORAGE_DIR="/app/server/storage" \
  --restart always \
  mintplexlabs/anythingllm:latest

echo ""
echo "=== Waiting 15s for container health... ==="
sleep 15

echo "=== Container status ==="
docker ps --filter name=diagnostic_rag_engine --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "=== Container logs (last 10 lines) ==="
docker logs diagnostic_rag_engine --tail 10 2>&1

echo ""
echo "=== Phase 2 complete ==="
