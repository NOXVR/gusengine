#!/usr/bin/env python3
"""
watermark_pdfs.py — Stamps [[ABSOLUTE_PAGE: N]] on every page of every PDF.

This enables the Gus diagnostic engine's WATERMARK-FIRST citation rule
(V9 spec lines 1287-1288) so source_citations return real page numbers
instead of "page: unknown".

Usage:
    python3 watermark_pdfs.py [--input-dir DIR] [--output-dir DIR] [--dry-run]

Requires: PyMuPDF (fitz) — already installed in venv.
"""

import argparse
import os
import sys
import time
import fitz  # PyMuPDF


def watermark_pdf(input_path, output_path, dry_run=False):
    """Stamp [[ABSOLUTE_PAGE: N]] on every page of a PDF.
    
    Returns (num_pages, success_bool, error_msg_or_None)
    """
    try:
        doc = fitz.open(input_path)
        num_pages = len(doc)
        
        if num_pages == 0:
            doc.close()
            return (0, False, "Empty PDF (0 pages)")
        
        if dry_run:
            doc.close()
            return (num_pages, True, None)
        
        for page_num in range(num_pages):
            page = doc[page_num]
            rect = page.rect
            
            # Watermark text
            tag = f"[[ABSOLUTE_PAGE: {page_num + 1}]]"
            
            # Position: bottom-right corner, 15pt from edges
            # This avoids Mercedes FSM content which uses wide margins
            x = rect.width - 15
            y = rect.height - 10
            
            # Insert as right-aligned small gray text
            # fontsize=7 is small enough not to interfere but OCR-readable
            page.insert_text(
                point=fitz.Point(x, y),
                text=tag,
                fontsize=7,
                fontname="helv",
                color=(0.6, 0.6, 0.6),  # light gray
                rotate=0,
            )
            
            # Also insert at top-left as a backup for OCR
            # Some OCR engines scan top-to-bottom and may miss bottom text
            # if the page is very long or truncated
            page.insert_text(
                point=fitz.Point(10, 12),
                text=tag,
                fontsize=7,
                fontname="helv",
                color=(0.6, 0.6, 0.6),
            )
        
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        return (num_pages, True, None)
        
    except Exception as e:
        return (0, False, str(e))


def main():
    parser = argparse.ArgumentParser(description="Stamp [[ABSOLUTE_PAGE: N]] watermarks on FSM PDFs")
    parser.add_argument("--input-dir", default=os.path.expanduser("~/diagnostic_engine/extracted_manuals"),
                        help="Source PDF directory")
    parser.add_argument("--output-dir", default=os.path.expanduser("~/diagnostic_engine/watermarked_manuals"),
                        help="Output directory for watermarked PDFs")
    parser.add_argument("--dry-run", action="store_true",
                        help="Count pages without modifying files")
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"FATAL: Input directory not found: {args.input_dir}")
        sys.exit(1)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Collect all PDFs
    pdfs = sorted([f for f in os.listdir(args.input_dir) if f.lower().endswith(".pdf")])
    total = len(pdfs)
    print(f"{'DRY RUN: ' if args.dry_run else ''}Processing {total} PDFs")
    print(f"  Input:  {args.input_dir}")
    print(f"  Output: {args.output_dir}")
    print()
    
    success_count = 0
    fail_count = 0
    total_pages = 0
    failures = []
    start_time = time.time()
    
    for i, pdf_name in enumerate(pdfs, 1):
        input_path = os.path.join(args.input_dir, pdf_name)
        output_path = os.path.join(args.output_dir, pdf_name)
        
        pages, ok, err = watermark_pdf(input_path, output_path, dry_run=args.dry_run)
        
        if ok:
            success_count += 1
            total_pages += pages
            if i % 50 == 0 or i == total:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                eta = (total - i) / rate if rate > 0 else 0
                print(f"  [{i}/{total}] {pdf_name} ({pages}p) — {rate:.1f} files/s, ETA {eta:.0f}s")
        else:
            fail_count += 1
            failures.append((pdf_name, err))
            print(f"  [{i}/{total}] FAILED: {pdf_name} — {err}")
    
    elapsed = time.time() - start_time
    print()
    print(f"{'DRY RUN ' if args.dry_run else ''}COMPLETE in {elapsed:.1f}s")
    print(f"  Success: {success_count}/{total}")
    print(f"  Failed:  {fail_count}/{total}")
    print(f"  Total pages watermarked: {total_pages}")
    
    if failures:
        print()
        print("FAILURES:")
        for name, err in failures:
            print(f"  - {name}: {err}")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
