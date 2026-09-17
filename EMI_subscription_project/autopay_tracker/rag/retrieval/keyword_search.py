from rank_bm25 import BM25Okapi


def build_bm25_index(chunks: list[dict]):#BM25 is for indexing word split text not embedding
    tokenized_corpus = [chunk["text"].lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25


def keyword_search(query: str, bm25, chunks: list[dict], top_k: int = 3):
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    scored_chunks = list(zip(chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    results = []
    for chunk, score in scored_chunks[:top_k]:
        results.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "score": float(score)
        })
    
    return results