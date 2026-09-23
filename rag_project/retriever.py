"""
retriever.py

Two-stage retrieval, since the query itself carries no metadata:

  Stage 1 (doc routing): embed the query, search doc_router.faiss (one
  vector per document) to find the single best-matching doc_id.

  Stage 2 (chunk search): load ONLY that document's index.faiss +
  chunks.json, and run the real similarity search inside it.

Other documents' vectors are never loaded or compared against.
"""

import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEXES_DIR = "indexes"
MODEL_NAME = "all-MiniLM-L6-v2"


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

        self.router_index = faiss.read_index("doc_router.faiss")
        with open("doc_router.json") as f:
            self.router_map = json.load(f)   # {"0": "behavior_guide", ...}

    def route_query(self, query_embedding):
        """Stage 1: pick the single best-matching document for this query."""
        distances, indices = self.router_index.search(query_embedding, k=1)
        best_position = int(indices[0][0])
        doc_id = self.router_map[str(best_position)]
        return doc_id, float(distances[0][0])

    def search_document(self, doc_id, query_embedding, top_k=3):
        """Stage 2: search only inside the routed document's own index."""
        doc_dir = os.path.join(INDEXES_DIR, doc_id)

        doc_index = faiss.read_index(os.path.join(doc_dir, "index.faiss"))
        with open(os.path.join(doc_dir, "chunks.json")) as f:
            chunk_store = json.load(f)

        k = min(top_k, doc_index.ntotal)
        distances, indices = doc_index.search(query_embedding, k)

        results = []
        for dist, pos in zip(distances[0], indices[0]):
            results.append({
                "doc_id": doc_id,
                "chunk": chunk_store[str(int(pos))],
                "distance": float(dist),
            })
        return results

    def query(self, user_query, top_k=3):
        query_embedding = self.model.encode([user_query], convert_to_numpy=True).astype("float32")

        doc_id, route_distance = self.route_query(query_embedding)
        results = self.search_document(doc_id, query_embedding, top_k=top_k)

        return {
            "query": user_query,
            "routed_doc_id": doc_id,
            "route_distance": route_distance,
            "results": results,
        }


if __name__ == "__main__":
    retriever = Retriever()

    test_queries = [
        "How should the assistant respond if a payment status is unclear?",
        "What tone should be used when discussing money?",
        "What is an EMI?",
    ]

    for q in test_queries:
        output = retriever.query(q, top_k=2)
        print(f"\nQuery: {output['query']}")
        print(f"Routed to document: {output['routed_doc_id']}")
        for r in output["results"]:
            print(f"  - ({r['distance']:.4f}) {r['chunk']}")
