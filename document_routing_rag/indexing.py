import os

from embeddings.model import encode_text
from routing.document_router import build_router_index, DOC_FOLDER_MAP
from retrieval.semantic_search import build_document_index

DOCS_DIR = "documents"
CHUNK_SIZE = 3       # sentences per chunk
CHUNK_OVERLAP = 1    


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
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


def run_ingest():
    doc_ids = []
    doc_centroids = []

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".md"):
            continue

        doc_id = os.path.splitext(filename)[0]          
        folder_name = DOC_FOLDER_MAP[doc_id]             
        file_path = os.path.join(DOCS_DIR, filename)

        with open(file_path, "r") as f:
            text = f.read()

        chunks = split_into_chunks(text)
        print(f"{doc_id}: {len(chunks)} chunks")

        embeddings = encode_text(chunks)
        build_document_index(folder_name, chunks, embeddings)

        centroid = embeddings.mean(axis=0)   
        doc_ids.append(doc_id)
        doc_centroids.append(centroid)

    build_router_index(doc_ids, doc_centroids)
    print(f"\nBuilt {len(doc_ids)} document indexes and the router index.")


run_ingest()