#!/usr/bin/env python3
"""
fix_gaps.py — Brute force gap filler. Scans every stored JSON, checks every
380-char window for an [[ABSOLUTE_PAGE: N]] tag, and injects one if missing.
Runs AFTER densify_watermarks_v2.py as a final guarantee pass.
"""

import os, sys, json, re

DOC_DIR = os.path.expanduser("~/diagnostic_engine/storage/documents/custom-documents")
WINDOW = 380
pattern = r'\[\[ABSOLUTE_PAGE: (\d+)\]\]'

files = sorted([f for f in os.listdir(DOC_DIR) if f.endswith(".json")])
print(f"Gap-filling {len(files)} documents")

fixed = 0
already_ok = 0
unfixable = 0

for fname in files:
    path = os.path.join(DOC_DIR, fname)
    with open(path) as f:
        data = json.load(f)
    
    content = data.get("pageContent", "")
    if not content or len(content) < 30:
        unfixable += 1
        continue
    
    # Find all existing tags to know which page numbers exist
    all_tags = re.findall(pattern, content)
    if not all_tags:
        # No tags at all — inject page 1 at the start
        content = "[[ABSOLUTE_PAGE: 1]] " + content
        all_tags = ["1"]
    
    # Check coverage
    max_iterations = 20
    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        gap_found = False
        
        for ci in range(0, len(content), WINDOW):
            chunk = content[ci:ci + WINDOW]
            if "[[ABSOLUTE_PAGE:" not in chunk and len(chunk) > 30:
                # Find the nearest tag BEFORE this position
                preceding = content[:ci]
                prev_tags = re.findall(pattern, preceding)
                page = prev_tags[-1] if prev_tags else all_tags[0]
                
                # Insert tag at the start of this chunk
                inject_pos = ci
                tag = f" [[ABSOLUTE_PAGE: {page}]] "
                content = content[:inject_pos] + tag + content[inject_pos:]
                gap_found = True
                break  # restart scan since positions shifted
        
        if not gap_found:
            break
    
    # Final verification
    all_covered = True
    for ci in range(0, len(content), WINDOW):
        chunk = content[ci:ci + WINDOW]
        if len(chunk) < 50:
            continue
        if "[[ABSOLUTE_PAGE:" not in chunk:
            all_covered = False
            break
    
    if content != data.get("pageContent", ""):
        data["pageContent"] = content
        data["wordCount"] = len(content.split())
        with open(path, "w") as f:
            json.dump(data, f)
        fixed += 1
    else:
        already_ok += 1

print(f"\nFixed: {fixed}")
print(f"Already OK: {already_ok}")
print(f"Unfixable (empty): {unfixable}")

# Exhaustive verification
print(f"\n=== EXHAUSTIVE VERIFICATION ===")
total_pass = 0
total_fail = 0
fail_list = []

for fname in files:
    path = os.path.join(DOC_DIR, fname)
    with open(path) as f:
        data = json.load(f)
    content = data.get("pageContent", "")
    if not content or len(content) < 30:
        continue
    
    covered = 0
    total = 0
    for ci in range(0, len(content), WINDOW):
        chunk = content[ci:ci + WINDOW]
        if len(chunk) < 50:  # trailing fragment, not a real chunk
            continue
        total += 1
        if "[[ABSOLUTE_PAGE:" in chunk:
            covered += 1
    
    if covered == total:
        total_pass += 1
    else:
        total_fail += 1
        pct = (covered / total * 100) if total > 0 else 0
        fail_list.append((fname[:50], f"{covered}/{total} = {pct:.0f}%"))

print(f"  PASS: {total_pass}")
print(f"  FAIL: {total_fail}")

if fail_list:
    for name, detail in fail_list[:10]:
        print(f"    {name}: {detail}")

if total_fail == 0:
    print("\n  *** ALL FILES PASS — 100% COVERAGE ***")
else:
    print(f"\n  {total_fail} files still failing")
    sys.exit(1)
