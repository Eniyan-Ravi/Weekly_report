"""
ingest.py

Reads every document in documents/, splits each into chunks, embeds the
chunks with all-MiniLM-L6-v2, and builds:

  indexes/<doc_id>/index.faiss   -> chunk vectors for that document only
  indexes/<doc_id>/chunks.json   -> {position: chunk_text} for that document

  doc_router.faiss               -> one vector per document (its centroid)
  doc_router.json                -> {position: doc_id} for the router

No metadata is attached to chunks. Isolation between documents comes purely
from each document having its own separate FAISS index (see retriever.py).
"""

import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DOCS_DIR = "documents"
INDEXES_DIR = "indexes"
MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 3          # sentences per chunk
CHUNK_OVERLAP = 1        # sentences of overlap between consecutive chunks


def load_model():
    print(f"Loading embedding model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Simple sentence-based chunking with overlap."""
    # crude sentence split on '.', keep it simple since docs are short
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = ". ".join(sentences[i:i + chunk_size]).strip()
        if chunk and not chunk.endswith("."):
            chunk += "."
        if chunk:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def build_document_index(doc_id, chunks, model):
    """Embed a document's chunks and save its own FAISS index + chunk text."""
    embeddings = model.encode(chunks, convert_to_numpy=True).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    doc_dir = os.path.join(INDEXES_DIR, doc_id)
    os.makedirs(doc_dir, exist_ok=True)

    faiss.write_index(index, os.path.join(doc_dir, "index.faiss"))

    chunk_store = {str(i): chunks[i] for i in range(len(chunks))}
    with open(os.path.join(doc_dir, "chunks.json"), "w") as f:
        json.dump(chunk_store, f, indent=2)

    return embeddings


def build_doc_router(doc_ids, doc_centroids, model):
    """Build the small index used to pick which document a query belongs to."""
    dimension = doc_centroids[0].shape[0]
    router_index = faiss.IndexFlatL2(dimension)
    router_index.add(np.array(doc_centroids).astype("float32"))

    faiss.write_index(router_index, "doc_router.faiss")

    router_map = {str(i): doc_ids[i] for i in range(len(doc_ids))}
    with open("doc_router.json", "w") as f:
        json.dump(router_map, f, indent=2)


def main():
    model = load_model()
    os.makedirs(INDEXES_DIR, exist_ok=True)

    doc_ids = []
    doc_centroids = []

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".md"):
            continue

        doc_id = os.path.splitext(filename)[0]   # filename without extension
        file_path = os.path.join(DOCS_DIR, filename)

        with open(file_path, "r") as f:
            text = f.read()

        chunks = split_into_chunks(text)
        print(f"{doc_id}: {len(chunks)} chunks")

        embeddings = build_document_index(doc_id, chunks, model)

        # document-level vector = mean of its chunk embeddings (its centroid)
        centroid = embeddings.mean(axis=0)

        doc_ids.append(doc_id)
        doc_centroids.append(centroid)

    build_doc_router(doc_ids, doc_centroids, model)
    print(f"\nBuilt {len(doc_ids)} document indexes and the doc_router index.")


if __name__ == "__main__":
    main()
