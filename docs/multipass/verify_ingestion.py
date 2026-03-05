#!/usr/bin/env python3
"""V8 Post-Ingestion Verification.
Compares filesystem chunks against embedded workspace documents.
"""

import os, sys, requests

API_KEY = os.popen(
    "grep INTERNAL_API_KEY ~/diagnostic_engine/.env | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS
chunks_dir = os.path.expanduser("~/diagnostic_engine/extracted_manuals")

expected = set(f for f in os.listdir(chunks_dir) if f.endswith('.pdf'))
try:
    resp = requests.get(f"{API_URL}/workspace/{WORKSPACE_SLUG}", headers=HEADERS)
except requests.RequestException as e:
    print(f"ERROR: Cannot reach API: {e}")
    sys.exit(1)
if resp.status_code == 200:
    docs = resp.json().get("workspace", {}).get("documents", [])
    embedded = set(d.get("name", "") for d in docs)
    missing = expected - embedded
    if missing:
        print(f"MISSING CHUNKS ({len(missing)}):")
        for m in sorted(missing):
            print(f"  ✗ {m}")
    else:
        print(f"✓ ALL {len(expected)} CHUNKS VERIFIED.")
else:
    print(f"ERROR: API returned {resp.status_code}")
