#!/usr/bin/env python3
"""V8 Ledger API Sync.
Uploads a validated MASTER_LEDGER.md directly to AnythingLLM via the
local loopback API (bypassing Nginx) and embeds it in the workspace.
"""

import os, requests, sys

API_KEY = os.popen(
    f"grep INTERNAL_API_KEY {os.path.expanduser('~/diagnostic_engine/.env')} | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS

if len(sys.argv) < 2:
    print("Usage: sync_ledger.py <path_to_ledger.md>")
    sys.exit(1)

ledger_path = sys.argv[1]
filename = os.path.basename(ledger_path)

# V8 FIX (Phase 10 DT R3): Fetch existing workspace documents to find any
# prior ledger version. Without this, every ledger update adds a NEW vector
# set but never removes the old one, causing LanceDB to accumulate
# conflicting historical ledger versions that break the "Absolute Truth"
# override mechanism.
old_ledger_loc = None
try:
    ws_resp = requests.get(
        f"{API_URL}/workspace/{WORKSPACE_SLUG}",
        headers=HEADERS
    )
    if ws_resp.status_code == 200:
        for doc in ws_resp.json().get("workspace", {}).get("documents", []):
            if "MASTER_LEDGER" in doc.get("name", "").upper():
                old_ledger_loc = doc.get("location")
                print(f"Found existing ledger to replace: {old_ledger_loc}")
                break
except Exception as e:
    print(f"WARNING: Could not fetch workspace docs ({e}). Old ledger will NOT be deleted.")

print(f"Uploading ledger: {filename}")
with open(ledger_path, 'rb') as f:
    try:
        resp = requests.post(
            f"{API_URL}/document/upload",
            headers=HEADERS,
            files={"file": (filename, f, "text/markdown")}
        )
        # V2 FIX: Check HTTP status before JSON parsing
        if resp.status_code != 200:
            print(f"FATAL: Upload failed ({resp.status_code}): {resp.text[:200]}")
            sys.exit(1)
        # V2 FIX: Guard against empty documents list
        documents = resp.json().get("documents", [])
        if not documents:
            print(f"FATAL: No document returned. API response: {resp.text[:200]}")
            sys.exit(1)
        doc_loc = documents[0].get("location")
        if doc_loc:
            embed_resp = requests.post(
                f"{API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings",
                headers={**HEADERS, "Content-Type": "application/json"},
                # V8 FIX (Phase 10 DT R3): Inject old ledger into deletes
                # for atomic swap. Prevents legacy vector poisoning.
                json={"adds": [doc_loc], "deletes": [old_ledger_loc] if old_ledger_loc else []}
            )
            if embed_resp.status_code == 200:
                print(f"LEDGER SUCCESSFULLY UPLOADED AND EMBEDDED: {doc_loc}")
            else:
                print(f"EMBED FAILED ({embed_resp.status_code}): {embed_resp.text}")
                sys.exit(1)
        else:
            print(f"FATAL: No document location returned. API response: {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to process ledger upload: {e}")
        sys.exit(1)
