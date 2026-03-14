import fitz
import sys

path = r"D:\Quick Access Downloads\ShopManual_Ford_2_3_4000_v2.pdf"
doc = fitz.open(path)

print(f"Pages: {len(doc)}")

# Sample first 5 pages
for i in range(min(5, len(doc))):
    t = doc[i].get_text()
    print(f"Page {i+1}: {len(t)} chars")

print(f"\n--- Sample text (page 1) ---")
print(doc[0].get_text()[:500])

print(f"\n--- Sample text (page 3) ---")
print(doc[2].get_text()[:500])

total_chars = sum(len(doc[i].get_text()) for i in range(len(doc)))
print(f"\nTotal extractable text: {total_chars:,} chars across {len(doc)} pages")
print(f"Avg chars/page: {total_chars // len(doc)}")

empty = sum(1 for i in range(len(doc)) if len(doc[i].get_text().strip()) < 50)
print(f"Near-empty pages (likely scans): {empty}/{len(doc)}")

if empty > len(doc) * 0.5:
    print("\n>>> VERDICT: NEEDS DOCLING (majority scanned/image pages)")
else:
    print("\n>>> VERDICT: PyMuPDF OK (text-extractable)")
