import os
import requests

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
PHI3_MODEL = 'phi3'

def generate(prompt: str, context_chunks: list) -> str:
    context = '\n\n'.join([f'[{c[\"law\"]}]\n{c[\"text\"]}' for c in context_chunks])
    full_prompt = f'You are an expert Indian legal assistant. Use only the legal context below to answer.\n\nContext:\n{context}\n\nQuestion: {prompt}\n\nAnswer:'
    try:
        resp = requests.post(
            f'{OLLAMA_URL}/api/generate',
            json={'model': PHI3_MODEL, 'prompt': full_prompt, 'stream': False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get('response', '').strip()
    except requests.exceptions.ConnectionError:
        return '[Phi-3] Ollama is not running. Start it with: ollama serve'
    except Exception as e:
        return f'[Phi-3] Error: {e}'
