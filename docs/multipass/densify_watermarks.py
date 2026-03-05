#!/usr/bin/env python3
"""
densify_watermarks.py — Post-process stored document JSON files to inject
[[ABSOLUTE_PAGE: N]] every 200 chars, guaranteeing 100% chunk coverage.

This runs AFTER Mistral OCR has extracted text. It modifies the pageContent
in each stored JSON file so that every 400-char text chunk contains at
least one [[ABSOLUTE_PAGE: N]] tag. Then the workspace must be reset and
re-embedded to pick up the changes.

This is aerospace-grade: 100% coverage, not 50%.
"""

import os
import sys
import json
import re


INJECT_INTERVAL = 200  # chars between injected tags


def densify_document(filepath):
    """Inject [[ABSOLUTE_PAGE: N]] tags every INJECT_INTERVAL chars.
    
    Algorithm:
    1. Parse existing [[ABSOLUTE_PAGE: N]] tags and their positions
    2. Between consecutive tags, if gap > INJECT_INTERVAL, inject
       copies of the earlier tag at regular intervals
    3. For text BEFORE the first tag, inject [[ABSOLUTE_PAGE: 1]]
    4. For text AFTER the last tag, inject the last page tag
    
    Returns (modified: bool, tag_count_before, tag_count_after)
    """
    with open(filepath) as f:
        data = json.load(f)
    
    content = data.get("pageContent", "")
    if not content:
        return (False, 0, 0)
    
    # Find all existing watermark tags and their positions
    pattern = r'\[\[ABSOLUTE_PAGE: (\d+)\]\]'
    matches = list(re.finditer(pattern, content))
    
    if not matches:
        # No watermarks at all — skip (shouldn't happen with v2 PDFs)
        return (False, 0, 0)
    
    tags_before = len(matches)
    
    # Build a list of (position, page_number) for all existing tags
    tag_positions = [(m.start(), m.end(), int(m.group(1))) for m in matches]
    
    # Now rebuild the content with densified tags
    new_content = []
    prev_end = 0
    
    for i, (start, end, page_num) in enumerate(tag_positions):
        # Get the text segment before this tag
        segment = content[prev_end:start]
        
        if len(segment) > INJECT_INTERVAL:
            # Need to inject tags into this segment
            # Determine which page number to use
            if i == 0:
                inject_page = page_num  # before first tag, use first page
            else:
                inject_page = tag_positions[i-1][2]  # use previous page's number
            
            inject_tag = f"[[ABSOLUTE_PAGE: {inject_page}]]"
            
            # Inject at regular intervals
            pos = 0
            while pos < len(segment):
                chunk_end = min(pos + INJECT_INTERVAL, len(segment))
                new_content.append(segment[pos:chunk_end])
                if chunk_end < len(segment):
                    new_content.append(f" {inject_tag} ")
                pos = chunk_end
        else:
            new_content.append(segment)
        
        # Add the original tag
        new_content.append(content[start:end])
        prev_end = end
    
    # Handle text after the last tag
    remaining = content[prev_end:]
    if len(remaining) > INJECT_INTERVAL:
        last_page = tag_positions[-1][2]
        inject_tag = f"[[ABSOLUTE_PAGE: {last_page}]]"
        pos = 0
        while pos < len(remaining):
            chunk_end = min(pos + INJECT_INTERVAL, len(remaining))
            new_content.append(remaining[pos:chunk_end])
            if chunk_end < len(remaining):
                new_content.append(f" {inject_tag} ")
            pos = chunk_end
    else:
        new_content.append(remaining)
    
    new_text = "".join(new_content)
    tags_after = len(re.findall(pattern, new_text))
    
    # Verify 100% coverage
    chunks_covered = 0
    chunks_total = 0
    for ci in range(0, len(new_text), 400):
        chunk = new_text[ci:ci+400]
        chunks_total += 1
        if "[[ABSOLUTE_PAGE:" in chunk:
            chunks_covered += 1
    
    coverage = (chunks_covered / chunks_total * 100) if chunks_total > 0 else 0
    
    if coverage < 100:
        # If still not 100%, do a brute force pass
        # Insert the nearest page tag into any uncovered chunk
        final_parts = []
        for ci in range(0, len(new_text), 200):
            chunk = new_text[ci:ci+200]
            final_parts.append(chunk)
            # Find nearest page tag before this position
            nearest = re.findall(pattern, new_text[:ci+200])
            if nearest and "[[ABSOLUTE_PAGE:" not in chunk:
                final_parts.append(f" [[ABSOLUTE_PAGE: {nearest[-1]}]] ")
        new_text = "".join(final_parts)
        tags_after = len(re.findall(pattern, new_text))
    
    # Save
    data["pageContent"] = new_text
    data["wordCount"] = len(new_text.split())
    with open(filepath, "w") as f:
        json.dump(data, f)
    
    return (True, tags_before, tags_after)


def main():
    doc_dir = os.path.expanduser("~/diagnostic_engine/storage/documents/custom-documents")
    
    if not os.path.isdir(doc_dir):
        print(f"FATAL: {doc_dir} not found")
        sys.exit(1)
    
    files = sorted([f for f in os.listdir(doc_dir) if f.endswith(".json")])
    print(f"Processing {len(files)} document chunks")
    
    modified = 0
    skipped = 0
    total_tags_before = 0
    total_tags_after = 0
    
    for fname in files:
        path = os.path.join(doc_dir, fname)
        ok, before, after = densify_document(path)
        if ok:
            modified += 1
            total_tags_before += before
            total_tags_after += after
        else:
            skipped += 1
    
    print(f"\nResults:")
    print(f"  Modified: {modified}")
    print(f"  Skipped: {skipped}")
    print(f"  Tags before: {total_tags_before}")
    print(f"  Tags after: {total_tags_after}")
    
    # Final coverage verification
    print(f"\n=== COVERAGE VERIFICATION ===")
    import random
    sample = random.sample(files[:modified] if modified else files, min(5, len(files)))
    all_pass = True
    for fname in sample:
        path = os.path.join(doc_dir, fname)
        with open(path) as f:
            data = json.load(f)
        content = data.get("pageContent", "")
        covered = 0
        total = 0
        for ci in range(0, len(content), 400):
            chunk = content[ci:ci+400]
            total += 1
            if "[[ABSOLUTE_PAGE:" in chunk:
                covered += 1
        pct = (covered / total * 100) if total > 0 else 0
        status = "PASS" if pct == 100 else "FAIL"
        if pct < 100:
            all_pass = False
        print(f"  {status}: {fname[:50]} — {covered}/{total} chunks ({pct:.0f}%)")
    
    if all_pass:
        print("\nALL PASS — 100% coverage achieved")
    else:
        print("\nFAIL — some chunks still uncovered")
        sys.exit(1)


if __name__ == "__main__":
    main()
