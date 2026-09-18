"""
Builds and persists the FAISS index from knowledge/blog_knowledge.txt.
Run directly to (re)build the index:
    python -m rag.indexing
"""

import pickle
import faiss

from rag.model import get_embed_model

KNOWLEDGE_PATH = "knowledge/blog_knowledge.txt"
INDEX_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"


def load_knowledge(path=KNOWLEDGE_PATH):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def build_index(chunks, model):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index, chunks, index_path=INDEX_PATH, chunks_path=CHUNKS_PATH):
    faiss.write_index(index, index_path)
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)


def load_index(index_path=INDEX_PATH, chunks_path=CHUNKS_PATH):
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def main():
    model = get_embed_model()
    chunks = load_knowledge()
    index = build_index(chunks, model)
    save_index(index, chunks)
    print(f"Indexed {len(chunks)} chunks -> {INDEX_PATH} / {CHUNKS_PATH}")


if __name__ == "__main__":
    main()