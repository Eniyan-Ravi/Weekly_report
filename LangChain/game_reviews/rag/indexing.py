from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#loaging
loader = TextLoader(
    "data/game_reviews.md",
    encoding="utf-8"
)

documents = loader.load()

print(f"Loaded documents: {len(documents)}")

#spelitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print(f"Created chunks: {len(chunks)}")

#embedding
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


#fiass vector store
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

print("FAISS vector store created")


#fiass index
vector_store.save_local("faiss_index")

print("FAISS index saved successfully")