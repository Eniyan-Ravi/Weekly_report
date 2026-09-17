import faiss
import pickle
import numpy as np
from pathlib import Path


index_dir = Path(__file__).parent / "index"
index_file = index_dir / "faiss.index"
chunks_file = index_dir / "chunks.pkl"


def build_index(embeddings, chunks):
    index_dir.mkdir(exist_ok=True)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(index_file))

    with open(chunks_file, "wb") as f:
        pickle.dump(chunks, f)

    return index


def load_index():
    index = faiss.read_index(str(index_file))

    with open(chunks_file, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def search(index, query_embedding, chunks, top_k=3):
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indexes = index.search(query_embedding, top_k)

    results = []

    for idx, distance in zip(indexes[0], distances[0]):
        if idx == -1:
            continue
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "chunk_id": chunks[idx]["chunk_id"],
            "distance": float(distance)
        })

    return results