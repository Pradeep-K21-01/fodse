"""
search-graph/elasticsearch/setup_index.py
Creates the Elasticsearch index and loads all legal chunks from structured_json/.

Install: pip install elasticsearch
Run:     python elasticsearch/setup_index.py

Requires: Elasticsearch running on localhost:9200
          docker run -p 9200:9200 -e "discovery.type=single-node" \
                     -e "xpack.security.enabled=false" \
                     elasticsearch:8.13.0
"""

import os
import json
from pathlib import Path
from elasticsearch import Elasticsearch, helpers

ES_URL        = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
INDEX_NAME    = "legal_docs"
CONFIG_FILE   = Path(__file__).parent / "index_config.json"

# Path to structured JSON from data-engineering pipeline
# Adjust if your folder is in a different location
STRUCTURED_DIR = Path(__file__).resolve().parent.parent.parent / "data-engineering" / "structured_json"


def get_client() -> Elasticsearch:
    print(f"[ES] Connecting to {ES_URL} ...")
    es = Elasticsearch(ES_URL)
    if not es.ping():
        raise ConnectionError(f"[ES] Cannot connect to Elasticsearch at {ES_URL}")
    print("[ES] Connected ✅")
    return es


def create_index(es: Elasticsearch):
    """Create index with mapping from index_config.json."""
    config = json.loads(CONFIG_FILE.read_text())

    if es.indices.exists(index=INDEX_NAME):
        print(f"[ES] Index '{INDEX_NAME}' already exists — deleting and recreating...")
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(index=INDEX_NAME, body=config)
    print(f"[ES] Index '{INDEX_NAME}' created ✅")


def load_documents() -> list[dict]:
    """Load all chunks from structured_json/ folder."""
    all_docs = []
    json_files = sorted(STRUCTURED_DIR.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(f"[ES] No JSON files found in: {STRUCTURED_DIR}")

    for jf in json_files:
        records = json.loads(jf.read_text(encoding="utf-8"))
        all_docs.extend(records)
        print(f"  Loaded {len(records)} chunks from {jf.name}")

    return all_docs


def bulk_index(es: Elasticsearch, docs: list[dict]):
    """Bulk upload all documents to Elasticsearch."""
    print(f"\n[ES] Indexing {len(docs)} documents...")

    actions = [
        {
            "_index": INDEX_NAME,
            "_id":    doc["id"],
            "_source": {
                "id":       doc["id"],
                "law":      doc["law"],
                "source":   doc["source"],
                "chunk_id": doc["chunk_id"],
                "text":     doc["text"],
            }
        }
        for doc in docs
    ]

    success, errors = helpers.bulk(es, actions, raise_on_error=False)
    print(f"[ES] Indexed {success} documents ✅")
    if errors:
        print(f"[ES] {len(errors)} errors — first: {errors[0]}")


def verify(es: Elasticsearch):
    """Check document count in index."""
    es.indices.refresh(index=INDEX_NAME)
    count = es.count(index=INDEX_NAME)["count"]
    print(f"\n[ES] Total documents in '{INDEX_NAME}': {count}")

    # Test search
    result = es.search(index=INDEX_NAME, body={
        "size": 1,
        "query": {"match": {"text": "cheque bounce"}}
    })
    hits = result["hits"]["hits"]
    if hits:
        print(f"[ES] Test search 'cheque bounce' → found: {hits[0]['_source']['law']}")
    print("\n[ES] Setup complete! Elasticsearch is ready for hybrid search.\n")


def main():
    es   = get_client()
    create_index(es)
    docs = load_documents()
    bulk_index(es, docs)
    verify(es)


if __name__ == "__main__":
    main()
