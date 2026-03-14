from sentence_transformers import SentenceTransformer
from functools import lru_cache

EMBED_MODEL = 'BAAI/bge-small-en-v1.5'
VECTOR_DIM = 384

@lru_cache(maxsize=1)
def get_embedding_model():
    print(f'[Embeddings] Loading {EMBED_MODEL} ...')
    model = SentenceTransformer(EMBED_MODEL)
    print('[Embeddings] Ready')
    return model

def encode(texts: list) -> list:
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()

def encode_query(query: str) -> list:
    prefixed = f'Represent this sentence for searching relevant passages: {query}'
    return encode([prefixed])[0]
