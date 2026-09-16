import faiss
import pickle
import numpy as np
from pathlib import Path


INDEX_DIR = Path("index")
INDEX_FILE = INDEX_DIR / "faiss.index"
CHUNKS_FILE = INDEX_DIR / "chunks.pkl"


def build_index(embeddings, chunks):
    INDEX_DIR.mkdir(exist_ok=True)

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    return index


def load_index():
    index = faiss.read_index(str(INDEX_FILE))

    with open(CHUNKS_FILE, "rb") as f:
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