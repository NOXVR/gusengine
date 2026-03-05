#!/bin/bash
# Debug: check .env format
echo "=== Raw .env content ==="
cat /home/ubuntu/diagnostic_engine/.env
echo ""

echo "=== grep result ==="
grep INTERNAL_API_KEY /home/ubuntu/diagnostic_engine/.env
echo ""

echo "=== cut result ==="
grep INTERNAL_API_KEY /home/ubuntu/diagnostic_engine/.env | tail -1 | cut -d '=' -f2-
echo ""

echo "=== Python extraction ==="
python3 -c "
with open('/home/ubuntu/diagnostic_engine/.env') as f:
    for line in f:
        if 'INTERNAL_API_KEY' in line:
            print('LINE:', repr(line))
            val = line.strip().split('=', 1)[1] if '=' in line else 'NOT FOUND'
            print('VALUE:', val)
"
