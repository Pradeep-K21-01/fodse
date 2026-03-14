import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from retrieval import qdrant_client
from llm.router import route

FRAUD_KEYWORDS = ['cheated','scam','fraud','fake','phishing','hacked','money stolen','upi fraud','online cheating','impersonation','job fraud','blackmail']

def is_fraud_query(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in FRAUD_KEYWORDS)

def run(query: str) -> dict:
    if not is_fraud_query(query):
        return {'is_fraud_case': False, 'answer': None, 'sources': []}
    try:
        it_chunks = qdrant_client.search(query, top_k=3, law_filter='Information Technology Act, 2000')
        cp_chunks = qdrant_client.search(query, top_k=2, law_filter='Consumer Protection Act, 2019')
        all_chunks = it_chunks + cp_chunks
    except Exception as e:
        print(f'[fraud_agent] Qdrant error: {e}')
        all_chunks = []
    if not all_chunks:
        return {'is_fraud_case': True, 'answer': 'This appears to be a fraud/cybercrime case. Please file a complaint at cybercrime.gov.in or call 1930.', 'model_used': 'static', 'sources': []}
    result = route(query, all_chunks)
    sources = [{'law': c['law'], 'text_preview': c['text'][:120] + '...'} for c in all_chunks]
    return {'is_fraud_case': True, 'answer': result['answer'], 'model_used': result['model_used'], 'sources': sources}
