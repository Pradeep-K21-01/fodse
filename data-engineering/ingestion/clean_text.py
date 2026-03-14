"""
data-engineering/ingestion/clean_text.py
Reads .txt files from processed_text/ → structured JSON in structured_json/

Install:  pip install langdetect
Run:      python ingestion/clean_text.py
"""

import re
import json
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent.parent
PROCESSED_DIR   = BASE_DIR / "processed_text"
STRUCTURED_DIR  = BASE_DIR / "structured_json"
METADATA_DIR    = BASE_DIR / "metadata"

STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

# Maps filename keywords → law name
LAW_NAME_MAP = {
    "IT_Act":                   "Information Technology Act, 2000",
    "Consumer_Protection":      "Consumer Protection Act, 2019",
    "CrPC_to_BNSS":             "CrPC to BNSS Transition Guide",
    "Cybercrime":               "Cybercrime Law (IT Act)",
    "Hindu_Marriage_Act":       "Hindu Marriage Act, 1955",
    "Hindu_Marriage_FAQ":       "Hindu Marriage Act FAQ",
    "Indian_Contract":          "Indian Contract Act, 1872",
    "Motor_Vehicle":            "Motor Vehicles Act, 1988",
    "Negotiable_Instruments":   "Negotiable Instruments Act, 1881",
    "Case_Law":                 "Case Law Precedents",
}


def guess_law_name(filename: str) -> str:
    for key, name in LAW_NAME_MAP.items():
        if key.lower() in filename.lower():
            return name
    return filename.replace("_", " ").replace("-", " ").strip()


def clean_text(raw: str) -> str:
    """Remove page headers, extra whitespace, and junk characters."""
    text = re.sub(r"--- Page \d+ ---", "", raw)   # remove page markers
    text = re.sub(r"\n{3,}", "\n\n", text)         # collapse blank lines
    text = re.sub(r"[ \t]+", " ", text)            # collapse spaces
    text = re.sub(r"[^\x00-\x7F]+", " ", text)    # remove non-ASCII (optional)
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    """
    Split text into overlapping chunks of ~chunk_size words.
    Each chunk overlaps the previous one by 50 words for context continuity.
    """
    words  = text.split()
    chunks = []
    step   = chunk_size - 50          # 50-word overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks


def process_all_texts():
    txt_files = sorted(PROCESSED_DIR.glob("*.txt"))
    if not txt_files:
        print(f"[!] No .txt files found in: {PROCESSED_DIR}")
        return

    print(f"[✓] Found {len(txt_files)} text file(s). Structuring...\n")

    all_metadata = []
    total_chunks = 0

    for txt_file in txt_files:
        print(f"  ➤  {txt_file.name}")
        raw  = txt_file.read_text(encoding="utf-8")
        text = clean_text(raw)

        law_name = guess_law_name(txt_file.stem)
        chunks   = split_into_chunks(text)

        records = []
        for idx, chunk in enumerate(chunks):
            records.append({
                "id":       f"{txt_file.stem}_{idx:04d}",
                "law":      law_name,
                "source":   txt_file.stem,
                "chunk_id": idx,
                "text":     chunk,
            })

        out = STRUCTURED_DIR / (txt_file.stem + ".json")
        out.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

        all_metadata.append({
            "file":       txt_file.name,
            "law":        law_name,
            "chunks":     len(records),
            "output":     out.name,
        })
        total_chunks += len(records)
        print(f"      ✅  {len(records)} chunks → structured_json/{out.name}")

    # Save master metadata
    meta_file = METADATA_DIR / "ingestion_metadata.json"
    meta_file.write_text(json.dumps(all_metadata, indent=2), encoding="utf-8")

    print(f"\n[Done] {len(txt_files)} files → {total_chunks} total chunks.")
    print(f"[Meta] Saved → metadata/ingestion_metadata.json\n")


if __name__ == "__main__":
    process_all_texts()
