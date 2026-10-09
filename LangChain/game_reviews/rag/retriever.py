from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS


embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


vector_store = FAISS.load_local(
    "rag/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


query = "What do customers think about gameplay?"

results = retriever.invoke(query)


for i, doc in enumerate(results, start=1):

    print(f"\nResult {i}:")

    print(
        "Source:",
        doc.metadata.get("source")
    )

    print("Content:")
    print(doc.page_content)