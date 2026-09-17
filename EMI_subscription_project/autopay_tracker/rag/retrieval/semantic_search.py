from rag.embeddings.embedder import embed_single_text
from rag.vectorstore.faiss_store import search


def semantic_search(query: str, index, chunks: list[dict], top_k: int = 3):
    query_vector = embed_single_text(query)
    results = search(
        index,
        query_vector, 
        chunks, 
        top_k=top_k
        )
    return results