#!/bin/bash
# Check watermarks directly in the vector DB stored text
# LanceDB stores chunks at /app/server/storage/lancedb inside the container
# With --network=host, storage is at the mounted volume path

API_KEY="S14RWKG-6DC451B-KY6VXQB-SYV33BQ"
BASE="http://127.0.0.1:3001/api/v1"

echo "=== Method 1: Check raw file in document processor cache ==="
# AnythingLLM stores processed docs here
STORAGE="/home/ubuntu/diagnostic_engine/storage"
find "$STORAGE" -name "*.json" -path "*/documents/*" 2>/dev/null | head -3 | while read f; do
    echo "--- $f ---"
    python3 -c "
import json
with open('$f') as fh:
    data = json.load(fh)
if isinstance(data, list):
    for chunk in data[:2]:
        text = chunk.get('pageContent', chunk.get('text', ''))[:300]
        has_wm = '[[ABSOLUTE_PAGE:' in text
        print(f'  Has watermark: {has_wm}')
        print(f'  Preview: {text[:200]}')
        print()
elif isinstance(data, dict):
    text = str(data)[:300]
    has_wm = '[[ABSOLUTE_PAGE:' in text
    print(f'  Has watermark: {has_wm}')
    print(f'  Preview: {text[:200]}')
"
done

echo ""
echo "=== Method 2: Search AnythingLLM document store ==="
ls "$STORAGE/documents/" 2>/dev/null | head -5
echo "..."

# Find a recently processed JSON chunk file
CHUNK_FILE=$(find "$STORAGE" -name "*.json" -path "*/documents/*" -newer /home/ubuntu/diagnostic_engine/ingestion_v2.log 2>/dev/null | head -1)
if [ -n "$CHUNK_FILE" ]; then
    echo "Found recent chunk: $CHUNK_FILE"
    python3 << PYEOF
import json
with open("$CHUNK_FILE") as f:
    data = json.load(f)
if isinstance(data, list):
    for i, chunk in enumerate(data[:3]):
        text = chunk.get("pageContent", chunk.get("text", ""))
        has_wm = "[[ABSOLUTE_PAGE:" in text
        print(f"Chunk {i}: watermark={has_wm}, len={len(text)}")
        if has_wm:
            import re
            tags = re.findall(r'\[\[ABSOLUTE_PAGE: \d+\]\]', text)
            print(f"  Tags found: {tags}")
        print(f"  First 150 chars: {text[:150]}")
        print()
PYEOF
else
    echo "No recent chunk files found yet"
fi
