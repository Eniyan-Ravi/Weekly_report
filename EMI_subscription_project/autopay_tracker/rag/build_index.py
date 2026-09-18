from rag.data_loader.document_loader import load_documents, chunk_documents
from rag.embeddings.embedder import embed_texts
from rag.vectorstore.faiss_store import build_index


def rebuild():
    docs = load_documents()
    chunks = chunk_documents(docs)
    texts = [c["text"] for c in chunks]

    embeddings = embed_texts(texts)
    build_index(embeddings, chunks)

    print(f"Rebuilt index with {len(chunks)} chunks from {len(docs)} documents.")


if __name__ == "__main__":
    rebuild()