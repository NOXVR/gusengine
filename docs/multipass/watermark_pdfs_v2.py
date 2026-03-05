#!/usr/bin/env python3
"""
watermark_pdfs_v2.py — Dense watermarking for RAG chunk compatibility.

Problem: PyMuPDF stamps [[ABSOLUTE_PAGE: N]] at top/bottom of each page,
but AnythingLLM's 400-char text splitter creates chunks where many chunks
fall BETWEEN page boundaries and contain no watermark tag.

Solution: Instead of visual PDF overlays, we post-process the extracted text
AFTER Mistral OCR runs, injecting [[ABSOLUTE_PAGE: N]] every ~250 chars.
But we can't modify AnythingLLM's OCR pipeline...

Real solution: Stamp MANY copies of the watermark on each page so that
text extraction picks up the tag frequently, not just at page edges.
We place the tag at multiple Y positions down each page.

Usage:
    python3 watermark_pdfs_v2.py [--input-dir DIR] [--output-dir DIR]
"""

import argparse
import os
import sys
import time
import fitz  # PyMuPDF


def watermark_pdf(input_path, output_path):
    """Stamp [[ABSOLUTE_PAGE: N]] at multiple positions on every page.
    
    We place tags every ~100px vertically so that no matter how
    the text splitter chunks the OCR output, every chunk contains
    at least one [[ABSOLUTE_PAGE: N]] tag.
    """
    try:
        doc = fitz.open(input_path)
        num_pages = len(doc)
        
        if num_pages == 0:
            doc.close()
            return (0, False, "Empty PDF")
        
        for page_num in range(num_pages):
            page = doc[page_num]
            rect = page.rect
            tag = f"[[ABSOLUTE_PAGE: {page_num + 1}]]"
            
            # Calculate how many watermark positions we need
            # Page height is typically 792 points (US Letter) or ~842 (A4)
            # We want a tag every ~100 points vertically
            # This ensures every ~300 chars of extracted text has a tag
            page_height = rect.height
            spacing = 100  # points between watermarks
            
            # Place at left edge, multiple Y positions
            y = 12  # start near top
            while y < page_height - 5:
                page.insert_text(
                    point=fitz.Point(5, y),
                    text=tag,
                    fontsize=6,
                    fontname="helv",
                    color=(0.75, 0.75, 0.75),  # light gray
                    rotate=0,
                )
                y += spacing
            
            # Also place at right edge for redundancy
            x_right = rect.width - 10
            y = 12
            while y < page_height - 5:
                page.insert_text(
                    point=fitz.Point(x_right, y),
                    text=tag,
                    fontsize=6,
                    fontname="helv",
                    color=(0.75, 0.75, 0.75),
                    rotate=0,
                )
                y += spacing
        
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        return (num_pages, True, None)
        
    except Exception as e:
        return (0, False, str(e))


def main():
    parser = argparse.ArgumentParser(description="Dense watermark PDFs for RAG")
    parser.add_argument("--input-dir", default=os.path.expanduser("~/diagnostic_engine/extracted_manuals"),
                        help="Source PDF directory")
    parser.add_argument("--output-dir", default=os.path.expanduser("~/diagnostic_engine/watermarked_manuals"),
                        help="Output directory for watermarked PDFs")
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"FATAL: Input directory not found: {args.input_dir}")
        sys.exit(1)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    pdfs = sorted([f for f in os.listdir(args.input_dir) if f.lower().endswith(".pdf")])
    total = len(pdfs)
    print(f"Dense watermarking {total} PDFs")
    print(f"  Input:  {args.input_dir}")
    print(f"  Output: {args.output_dir}")
    print(f"  Tag spacing: every 100 points vertically, both margins")
    print()
    
    success = 0
    fail = 0
    total_pages = 0
    failures = []
    t0 = time.time()
    
    for i, name in enumerate(pdfs, 1):
        inp = os.path.join(args.input_dir, name)
        out = os.path.join(args.output_dir, name)
        pages, ok, err = watermark_pdf(inp, out)
        if ok:
            success += 1
            total_pages += pages
            if i % 100 == 0 or i == total:
                elapsed = time.time() - t0
                print(f"  [{i}/{total}] {elapsed:.0f}s elapsed")
        else:
            fail += 1
            failures.append((name, err))
            print(f"  [{i}/{total}] FAILED: {name} — {err}")
    
    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s: {success} ok, {fail} failed, {total_pages} pages")
    
    if failures:
        print("\nFailures:")
        for n, e in failures:
            print(f"  {n}: {e}")
    
    # Quick verification
    print("\n=== Verification ===")
    import random, re
    sample = random.sample(pdfs[:success], min(3, success))
    for name in sample:
        path = os.path.join(args.output_dir, name)
        doc = fitz.open(path)
        for pg_idx in range(len(doc)):
            text = doc[pg_idx].get_text()
            tag = f"[[ABSOLUTE_PAGE: {pg_idx + 1}]]"
            count = text.count(tag)
            if count < 3:
                print(f"  WARNING: {name} page {pg_idx+1} has only {count} tags")
            else:
                if pg_idx == 0:
                    print(f"  PASS: {name} page 1 has {count} tags")
        doc.close()


if __name__ == "__main__":
    main()
