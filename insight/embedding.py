from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache(maxsize=1)
def encoder():
    return SentenceTransformer("all-MiniLM-L6-v2")
