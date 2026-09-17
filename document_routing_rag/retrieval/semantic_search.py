import os
import json
import faiss

INDEXES_DIR = "indexes"


def build_document_index(folder_name, chunks, embeddings):
    doc_dir = os.path.join(INDEXES_DIR, folder_name)
    os.makedirs(doc_dir, exist_ok=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, os.path.join(doc_dir, "index.faiss"))

    chunk_store = {str(i): chunks[i] for i in range(len(chunks))}
    with open(os.path.join(doc_dir, "chunks.json"), "w") as f:
        json.dump(chunk_store, f, indent=2)


def search_document(folder_name, query_embedding, top_k=3):
    doc_dir = os.path.join(INDEXES_DIR, folder_name)

    doc_index = faiss.read_index(os.path.join(doc_dir, "index.faiss"))
    with open(os.path.join(doc_dir, "chunks.json")) as f:
        chunk_store = json.load(f)

    k = min(top_k, doc_index.ntotal)
    distances, indices = doc_index.search(query_embedding, k)

    results = []
    for dist, pos in zip(distances[0], indices[0]):
        results.append({
            "chunk": chunk_store[str(int(pos))],
            "distance": float(dist),
        })

    return results