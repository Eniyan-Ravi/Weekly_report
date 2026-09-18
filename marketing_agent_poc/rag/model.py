"""
Single place that owns the embedding model, so it's loaded once
and shared by indexing.py and semantic_search.py.
"""

from sentence_transformers import SentenceTransformer

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, runs fine on CPU

_model = None


def get_embed_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model