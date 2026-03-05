#!/usr/bin/env python3
"""V8 Synchronous Ingestion Script.
Uploads chunked PDFs to AnythingLLM and embeds them one at a time,
with a 12-second cooldown between uploads to prevent Mistral OCR 429s.
"""

import os, sys, time, requests, glob
import re  # V9 RECOVERY (I-1): required by preprocess_markdown_tables()

API_KEY = os.popen(
    f"grep INTERNAL_API_KEY {os.path.expanduser('~/diagnostic_engine/.env')} | tail -1 | cut -d '=' -f2-"
).read().strip()

# V2 FIX: Guard against empty API key. Without this, the script proceeds
# with "Bearer " (empty), gets silent 403s, and the operator thinks
# ingestion succeeded when no files were actually uploaded.
if not API_KEY:
    print("FATAL: INTERNAL_API_KEY is empty. Check ~/diagnostic_engine/.env")
    sys.exit(1)

API_URL = "http://127.0.0.1:3001/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
WORKSPACE_SLUG = "1975-mercedes-benz-450sl"  # CHANGE THIS TO YOUR WORKSPACE
CHUNKS_DIR = os.path.expanduser("~/diagnostic_engine/extracted_manuals")

def preprocess_markdown_tables(md_content, max_rows=20):
    """Split oversized tables, prepending header rows to each sub-table.
    Prevents Markdown Table chunk explosion during Mistral OCR vectorization.
    V9 RECOVERY (I-1): Restored from VFINAL Phase 10 (lines 391-416).
    """
    lines = md_content.split('\n')
    output = []
    i = 0
    part = 0
    while i < len(lines):
        if '|' in lines[i] and i + 1 < len(lines) and re.match(r'\|[\s\-:]+\|', lines[i + 1]):
            header_row = lines[i]
            separator = lines[i + 1]
            data_rows = []
            i += 2
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                data_rows.append(lines[i])
                i += 1
            if len(data_rows) <= max_rows:
                output.extend([header_row, separator] + data_rows)
            else:
                for j in range(0, len(data_rows), max_rows):
                    part += 1
                    output.append(f"### Table Continuation (Part {part})")
                    output.extend([header_row, separator] + data_rows[j:j+max_rows] + [""])
        else:
            output.append(lines[i])
            i += 1
    return '\n'.join(output)

# V8 FIX (Phase 10 DT R3): Fetch already-embedded documents BEFORE the loop.
# Without this, running the script a second time re-uploads and re-embeds
# every PDF in extracted_manuals/, causing exponential vector duplication.
print(f"Fetching existing documents for workspace: {WORKSPACE_SLUG}...")
try:
    ws_resp = requests.get(
        f"{API_URL}/workspace/{WORKSPACE_SLUG}",
        headers=HEADERS
    )
    existing_docs = set()
    if ws_resp.status_code == 200:
        for doc in ws_resp.json().get("workspace", {}).get("documents", []):
            existing_docs.add(doc.get("name", ""))
    print(f"Found {len(existing_docs)} already-embedded documents.")
except Exception as e:
    print(f"WARNING: Could not fetch workspace docs ({e}). Proceeding without dedup.")
    existing_docs = set()

print(f"Ingesting to workspace: {WORKSPACE_SLUG}...")
for chunk_path in sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.pdf"))):
    filename = os.path.basename(chunk_path)

    # V8 FIX (Phase 10 DT R3): Skip already-embedded documents
    if filename in existing_docs:
        print(f"SKIP (already embedded): {filename}")
        continue

    print(f"Uploading: {filename}")

    # V9 RECOVERY (I-1): Preprocess markdown files to split oversized tables
    # before API submission. Prevents Markdown Table chunk explosion.
    # NOTE: Currently dormant — the glob at line 812 targets *.pdf only.
    # This branch will activate if .md files are added to extracted_manuals/
    # or if the glob is expanded to include *.md files in a future version.
    if filename.lower().endswith('.md'):
        with open(chunk_path, 'r') as md_f:
            processed = preprocess_markdown_tables(md_f.read())
        with open(chunk_path, 'w') as md_f:
            md_f.write(processed)

    with open(chunk_path, 'rb') as f:
        try:
            resp = requests.post(
                f"{API_URL}/document/upload",
                headers=HEADERS,
                files={"file": (filename, f, "application/pdf")}
            )
            # V2 FIX: Check HTTP status before parsing JSON.
            # A 500 error with HTML body would crash resp.json().
            if resp.status_code != 200:
                print(f"UPLOAD FAILED ({resp.status_code}): {filename} — {resp.text[:200]}")
                continue
            time.sleep(2)  # Internal queue buffer
            # V2 FIX: Guard against empty documents list.
            # Original code used [{}][0] which masks real failure.
            # If API returns {"documents": []}, this is now caught explicitly.
            documents = resp.json().get("documents", [])
            if not documents:
                print(f"WARNING: No document returned for {filename}. Skipping.")
                continue
            doc_loc = documents[0].get("location")
            if doc_loc:
                embed_resp = requests.post(
                    f"{API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings",
                    headers={**HEADERS, "Content-Type": "application/json"},
                    json={"adds": [doc_loc], "deletes": []}
                )
                if embed_resp.status_code == 200:
                    print(f"EMBEDDED: {filename}. Cooling down Mistral API...")
                else:
                    print(f"EMBED FAILED ({embed_resp.status_code}): {filename}")
            else:
                print(f"WARNING: No document location returned for {filename}")
        except Exception as e:
            print(f"Failed: {e}")
        finally:
            # V8 FIX (Phase 10 R4): Mandatory 12s cooldown in `finally` block
            # so it fires UNCONDITIONALLY — after `continue` (upload failure,
            # empty docs), after `except` (network errors), and after normal
            # success. Previous placement inside the try block was bypassed by
            # `continue` and `except`, creating the exact death spiral (tight-
            # loop 429 → no cooldown → re-request → IP/API ban) that the fix
            # was designed to prevent.
            time.sleep(12)

print("Ingestion complete.")
