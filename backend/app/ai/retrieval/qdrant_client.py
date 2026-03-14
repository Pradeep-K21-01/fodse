import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from embeddings.bge_model import encode_query

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
COLLECTION_NAME = 'legal_docs'
_client = None

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(url=QDRANT_URL)
    return _client

def search(query: str, top_k: int = 5, law_filter: str = None) -> list:
    try:
        vector = encode_query(query)
        client = get_client()
        query_filter = None
        if law_filter:
            query_filter = Filter(must=[FieldCondition(key='law', match=MatchValue(value=law_filter))])
        results = client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=top_k, query_filter=query_filter, with_payload=True)
        return [{'text': h.payload.get('text',''), 'law': h.payload.get('law',''), 'source': h.payload.get('source',''), 'score': round(h.score,4)} for h in results]
    except Exception as e:
        print(f'[qdrant_client] Error: {e}')
        return []
