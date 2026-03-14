import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from retrieval import qdrant_client, elastic_client
from retrieval.reranker import rerank
from llm.router import route

def run(query: str, top_k: int = 5) -> dict:
    try:
        qdrant_hits = qdrant_client.search(query, top_k=top_k)
    except Exception as e:
        print(f'[legal_agent] Qdrant error: {e}')
        qdrant_hits = []
    try:
        elastic_hits = elastic_client.search(query, top_k=top_k)
    except Exception as e:
        print(f'[legal_agent] ES error: {e}')
        elastic_hits = []
    best_chunks = rerank(query, qdrant_hits, elastic_hits, top_n=5)
    result = route(query, best_chunks)
    sources = [{'law': c['law'], 'text_preview': c['text'][:120] + '...'} for c in best_chunks]
    return {'answer': result['answer'], 'model_used': result['model_used'], 'sources': sources}
