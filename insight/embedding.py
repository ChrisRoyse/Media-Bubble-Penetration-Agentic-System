from functools import lru_cache
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def encoder() -> SentenceTransformer:
    """Returns a cached SBERT encoder."""
    return SentenceTransformer("all-MiniLM-L6-v2")
