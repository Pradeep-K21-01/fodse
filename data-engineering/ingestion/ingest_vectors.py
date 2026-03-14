"""
data-engineering/ingestion/ingest_vectors.py
Reads structured_json/ → embeds each chunk → uploads to Qdrant vector DB.

Install:  pip install qdrant-client sentence-transformers tqdm
Run:      python ingestion/ingest_vectors.py

Requires: Qdrant running locally (docker run -p 6333:6333 qdrant/qdrant)
          OR set QDRANT_URL in your .env file for cloud Qdrant.
"""

import os
import json
import uuid
from pathlib import Path
from tqdm import tqdm

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

# ── Config ─────────────────────────────────────────────────────────────────────
QDRANT_URL      = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "legal_docs"
EMBED_MODEL     = "BAAI/bge-small-en-v1.5"   # fast, accurate, free
BATCH_SIZE      = 64                           # how many chunks to embed at once
VECTOR_DIM      = 384                          # bge-small dimension

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).resolve().parent.parent
STRUCTURED_DIR = BASE_DIR / "structured_json"


# ── Setup ──────────────────────────────────────────────────────────────────────

def get_qdrant_client() -> QdrantClient:
    print(f"[Qdrant] Connecting to {QDRANT_URL} ...")
    client = QdrantClient(url=QDRANT_URL)
    print("[Qdrant] Connected ✅")
    return client


def ensure_collection(client: QdrantClient):
    """Create collection if it doesn't exist yet."""
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )
        print(f"[Qdrant] Collection '{COLLECTION_NAME}' created ✅")
    else:
        print(f"[Qdrant] Collection '{COLLECTION_NAME}' already exists.")


def load_all_chunks() -> list[dict]:
    """Load every record from every JSON file in structured_json/."""
    all_chunks = []
    for json_file in sorted(STRUCTURED_DIR.glob("*.json")):
        records = json.loads(json_file.read_text(encoding="utf-8"))
        all_chunks.extend(records)
    return all_chunks


def embed_and_upload(client: QdrantClient, chunks: list[dict], model: SentenceTransformer):
    """Embed chunks in batches and upload to Qdrant."""
    print(f"\n[Embed] Embedding {len(chunks)} chunks with '{EMBED_MODEL}' ...\n")

    for i in tqdm(range(0, len(chunks), BATCH_SIZE), desc="Uploading batches"):
        batch   = chunks[i : i + BATCH_SIZE]
        texts   = [c["text"] for c in batch]
        vectors = model.encode(texts, normalize_embeddings=True).tolist()

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[j],
                payload={
                    "id":       batch[j]["id"],
                    "law":      batch[j]["law"],
                    "source":   batch[j]["source"],
                    "chunk_id": batch[j]["chunk_id"],
                    "text":     batch[j]["text"],
                },
            )
            for j in range(len(batch))
        ]

        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"\n[✓] {len(chunks)} vectors uploaded to '{COLLECTION_NAME}'")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # 1. Load chunks
    chunks = load_all_chunks()
    if not chunks:
        print(f"[!] No JSON files found in: {STRUCTURED_DIR}")
        print("    Run clean_text.py first.")
        return
    print(f"[✓] Loaded {len(chunks)} chunks from structured_json/")

    # 2. Load embedding model
    print(f"\n[Model] Loading '{EMBED_MODEL}' ...")
    model = SentenceTransformer(EMBED_MODEL)
    print(f"[Model] Ready ✅")

    # 3. Connect to Qdrant
    client = get_qdrant_client()
    ensure_collection(client)

    # 4. Embed + upload
    embed_and_upload(client, chunks, model)

    # 5. Verify
    info = client.get_collection(COLLECTION_NAME)
    print(f"\n[Qdrant] Total vectors in collection: {info.points_count}")
    print("\n🎉 Ingestion complete! Your legal data is ready for RAG queries.\n")


if __name__ == "__main__":
    main()
