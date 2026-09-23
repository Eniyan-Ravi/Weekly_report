from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


#Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


#Load existing FAISS vector store
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


#Convert vector store into a Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


#Test retrieval
query = "What do customers think about gameplay?"

results = retriever.invoke(query)

#results
for i, doc in enumerate(results, start=1):

    print(f"\n Result {i} :")

    print("Source:", doc.metadata.get("source"))

    print("Content:")
    print(doc.page_content)


