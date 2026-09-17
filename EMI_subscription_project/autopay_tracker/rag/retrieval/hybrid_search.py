def hybrid_search(query: str, index, bm25, chunks: list[dict], top_k: int = 3):
    from rag.retrieval.semantic_search import semantic_search
    from rag.retrieval.keyword_search import keyword_search

    semantic_results = semantic_search(query, index, chunks, top_k=top_k)
    keyword_results = keyword_search(query, bm25, chunks, top_k=top_k)

    combined = {}

    for rank, result in enumerate(semantic_results):
        chunk_id = result["chunk_id"]
        combined[chunk_id] = combined.get(chunk_id, 0) + 1 / (rank + 1)

    for rank, result in enumerate(keyword_results):
        chunk_id = result["chunk_id"]
        combined[chunk_id] = combined.get(chunk_id, 0) + 1 / (rank + 1)

    chunk_lookup = {c["chunk_id"]: c for c in chunks}

    sorted_chunk_ids = sorted(combined.items(), key=lambda x: x[1], reverse=True)

    results = []
    for chunk_id, fused_score in sorted_chunk_ids[:top_k]:
        chunk = chunk_lookup[chunk_id]
        results.append({
            "source": chunk["source"],
            "chunk_id": chunk_id,
            "text": chunk["text"],
            "fused_score": fused_score
        })

    return results