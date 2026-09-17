from rag.data_loader.document_loader import load_documents, chunk_documents
from rag.embeddings.embedder import embed_texts
from rag.vectorstore.faiss_store import build_index, load_index
from rag.retrieval.keyword_search import build_bm25_index
from rag.retrieval.hybrid_search import hybrid_search

docs = load_documents()
chunks = chunk_documents(docs)
texts = [c["text"] for c in chunks]

embeddings = embed_texts(texts)
build_index(embeddings, chunks)
index, loaded_chunks = load_index()

bm25 = build_bm25_index(loaded_chunks)

query = "never make up financial numbers"
results = hybrid_search(query, index, bm25, loaded_chunks, top_k=2)

for r in results:
    print(r["source"], "-", r["fused_score"])
    print(r["text"][:100], "...\n")