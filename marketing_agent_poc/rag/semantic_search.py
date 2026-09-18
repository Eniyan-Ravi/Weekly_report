"""
Retrieval only — given a query, return the top-k most relevant chunks.
"""

from rag.model import get_embed_model
from rag.indexing import load_index


def retrieve(query, top_k=3):
    model = get_embed_model()
    index, chunks = load_index()
    q_emb = model.encode([query], convert_to_numpy=True)
    _, indices = index.search(q_emb, top_k)
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]