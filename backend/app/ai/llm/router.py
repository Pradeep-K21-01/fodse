import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from llm import gemini_model, phi3_model

LLM_MODE = os.getenv('LLM_MODE', 'auto')

def route(query: str, context_chunks: list, language: str = 'english') -> dict:
    if LLM_MODE == 'gemini':
        return _call_gemini(query, context_chunks)
    if LLM_MODE == 'phi3':
        return _call_phi3(query, context_chunks)
    result = _call_gemini(query, context_chunks)
    if not result['answer'].strip() or result['answer'].startswith('[Gemini] Error'):
        print('[Router] Gemini failed, falling back to Phi-3')
        return _call_phi3(query, context_chunks)
    return result

def _call_gemini(query, chunks):
    try:
        answer = gemini_model.generate(query, chunks)
        return {'answer': answer, 'model_used': 'gemini-1.5-flash'}
    except Exception as e:
        return {'answer': f'[Gemini] Error: {e}', 'model_used': 'gemini-1.5-flash'}

def _call_phi3(query, chunks):
    answer = phi3_model.generate(query, chunks)
    return {'answer': answer, 'model_used': 'phi3-mini'}
