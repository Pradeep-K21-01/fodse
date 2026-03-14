"""
data-engineering/ingestion/pdf_to_text.py
Converts all PDFs from raw_pdfs/ → processed_text/
"""

import sys
import pdfplumber
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PDF_DIR = BASE_DIR / "raw_pdfs"
PROCESSED_DIR = BASE_DIR / "processed_text"

print(f"[DEBUG] Base directory: {BASE_DIR}")
print(f"[DEBUG] Looking for PDFs in: {RAW_PDF_DIR}")

# Ensure folders exist
RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def pdf_to_text(pdf_path: Path) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"--- Page {i} ---\n{text.strip()}")
    return "\n\n".join(pages)


def process_all_pdfs():
    pdf_files = sorted(RAW_PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("\n[!] No PDFs found.")
        print(f"[!] Put PDF files inside: {RAW_PDF_DIR}\n")
        sys.exit(0)

    print(f"\n[✓] Found {len(pdf_files)} PDF(s). Starting extraction...\n")

    success, failed = 0, 0

    for pdf_file in pdf_files:
        print(f"  ➤  {pdf_file.name}")
        try:
            text = pdf_to_text(pdf_file)
            output_path = PROCESSED_DIR / (pdf_file.stem + ".txt")
            output_path.write_text(text, encoding="utf-8")
            print(f"      ✅ Saved → {output_path.name}")
            success += 1
        except Exception as e:
            print(f"      ❌ Error: {e}")
            failed += 1

    print(f"\n[Done] {success} converted, {failed} failed.")
    print(f"[Output Folder] {PROCESSED_DIR}\n")


if __name__ == "__main__":
    process_all_pdfs()