#!/usr/bin/env python3
"""
densify_watermarks_v2.py — Aerospace-grade watermark injection.

Strategy:
1. Parse existing [[ABSOLUTE_PAGE: N]] tags to build a page-to-offset map
2. STRIP all existing watermark tags (remove the OCR blobs)
3. For each character position, determine which page it belongs to
4. Re-inject ONE [[ABSOLUTE_PAGE: N]] tag every INTERVAL characters
5. Save modified pageContent

This guarantees 100% chunk coverage because:
- AnythingLLM chunks at ~400 chars
- Metadata header uses ~160 chars
- Effective content per chunk: ~380 chars (with overlap)
- We inject every 150 chars → at least 2 tags per chunk
"""

import os
import sys
import json
import re


INJECT_INTERVAL = 150  # Must be < 400 - 160 (metadata overhead) - 20 (overlap)


def densify_document(filepath):
    """Strip watermark blobs, re-inject tags every INJECT_INTERVAL chars.
    
    Returns (modified: bool, stats_dict)
    """
    with open(filepath) as f:
        data = json.load(f)
    
    content = data.get("pageContent", "")
    if not content:
        return (False, {"reason": "empty"})
    
    pattern = r'\[\[ABSOLUTE_PAGE: (\d+)\]\]'
    matches = list(re.finditer(pattern, content))
    
    if not matches:
        return (False, {"reason": "no_tags"})
    
    # Build page map: for each tag, record (position_in_clean_text, page_number)
    # First, strip all tags and track where each page starts in the clean text
    page_boundaries = []  # (clean_text_position, page_number)
    clean_parts = []
    last_end = 0
    clean_pos = 0
    
    for m in matches:
        # Add text before this tag
        text_before = content[last_end:m.start()]
        clean_parts.append(text_before)
        clean_pos += len(text_before)
        
        # Record this page boundary in clean text coordinates
        page_num = int(m.group(1))
        # Only record if it's a new page or first occurrence
        if not page_boundaries or page_boundaries[-1][1] != page_num:
            page_boundaries.append((clean_pos, page_num))
        
        last_end = m.end()
    
    # Add remaining text after last tag
    remaining = content[last_end:]
    clean_parts.append(remaining)
    
    clean_text = "".join(clean_parts)
    
    if not clean_text.strip():
        return (False, {"reason": "empty_after_strip"})
    
    # If no page boundaries detected, default to page 1
    if not page_boundaries:
        page_boundaries = [(0, 1)]
    
    # Determine page for any position in clean text
    def get_page(pos):
        current = page_boundaries[0][1]
        for p, pg in page_boundaries:
            if pos >= p:
                current = pg
            else:
                break
        return current
    
    # Now rebuild with evenly spaced tags
    # Strategy: inject a tag at position 0, then every INJECT_INTERVAL chars
    new_parts = []
    
    # Start with a tag
    first_page = get_page(0)
    new_parts.append(f"[[ABSOLUTE_PAGE: {first_page}]] ")
    
    chars_since_tag = 0
    for i, char in enumerate(clean_text):
        current_page = get_page(i)
        new_parts.append(char)
        chars_since_tag += 1
        
        if chars_since_tag >= INJECT_INTERVAL:
            new_parts.append(f" [[ABSOLUTE_PAGE: {current_page}]] ")
            chars_since_tag = 0
    
    # End with a tag
    last_page = get_page(len(clean_text) - 1) if clean_text else first_page
    new_parts.append(f" [[ABSOLUTE_PAGE: {last_page}]]")
    
    new_text = "".join(new_parts)
    
    # Final guarantee pass: scan every 380-char window and inject if missing
    # This handles any edge cases the even-spacing approach might miss
    CHECK_WINDOW = 380  # matches effective chunk content size
    needs_fix = True
    passes = 0
    while needs_fix and passes < 5:
        needs_fix = False
        passes += 1
        fixed_parts = []
        i = 0
        while i < len(new_text):
            window = new_text[i:i+CHECK_WINDOW]
            if "[[ABSOLUTE_PAGE:" not in window and len(window) > 50:
                # Find the midpoint and inject
                mid = i + len(window) // 2
                pg = get_page(min(mid, len(clean_text)-1))
                new_text = new_text[:mid] + f" [[ABSOLUTE_PAGE: {pg}]] " + new_text[mid:]
                needs_fix = True
                break
            i += CHECK_WINDOW // 2  # overlapping scan
    
    # Verify coverage
    chunks_covered = 0
    chunks_total = 0
    for ci in range(0, len(new_text), 380):
        chunk = new_text[ci:ci+380]
        chunks_total += 1
        if "[[ABSOLUTE_PAGE:" in chunk:
            chunks_covered += 1
    
    coverage = (chunks_covered / chunks_total * 100) if chunks_total > 0 else 0
    
    tags_after = len(re.findall(pattern, new_text))
    
    data["pageContent"] = new_text
    data["wordCount"] = len(new_text.split())
    with open(filepath, "w") as f:
        json.dump(data, f)
    
    return (True, {
        "tags": tags_after,
        "coverage": coverage,
        "clean_len": len(clean_text),
        "new_len": len(new_text),
        "pages": len(page_boundaries)
    })


def main():
    doc_dir = os.path.expanduser("~/diagnostic_engine/storage/documents/custom-documents")
    
    if not os.path.isdir(doc_dir):
        print(f"FATAL: {doc_dir} not found")
        sys.exit(1)
    
    files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".json")])
    print(f"Processing {len(files)} documents with INJECT_INTERVAL={INJECT_INTERVAL}")
    
    modified = 0
    skipped = 0
    
    for fname in files:
        path = os.path.join(doc_dir, fname)
        ok, stats = densify_document(path)
        if ok:
            modified += 1
        else:
            skipped += 1
    
    print(f"\nModified: {modified}, Skipped: {skipped}")
    
    # Exhaustive verification — check EVERY file, not a sample
    print(f"\n=== EXHAUSTIVE VERIFICATION ===")
    total_pass = 0
    total_fail = 0
    fail_files = []
    
    for fname in files:
        path = os.path.join(doc_dir, fname)
        with open(path) as f:
            data = json.load(f)
        content = data.get("pageContent", "")
        
        if not content:
            continue
        
        covered = 0
        total = 0
        for ci in range(0, len(content), 380):
            chunk = content[ci:ci+380]
            total += 1
            if "[[ABSOLUTE_PAGE:" in chunk:
                covered += 1
        
        if total > 0 and covered == total:
            total_pass += 1
        else:
            total_fail += 1
            pct = (covered/total*100) if total > 0 else 0
            fail_files.append((fname[:50], f"{covered}/{total} = {pct:.0f}%"))
    
    print(f"  PASS: {total_pass}")
    print(f"  FAIL: {total_fail}")
    
    if fail_files:
        print("\n  Failed files:")
        for name, detail in fail_files[:10]:
            print(f"    {name}: {detail}")
    
    if total_fail == 0:
        print("\n  ALL FILES PASS — 100% COVERAGE ACROSS ENTIRE CORPUS")
    else:
        print(f"\n  {total_fail} files below 100% — needs investigation")
        sys.exit(1)


if __name__ == "__main__":
    main()
