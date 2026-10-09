from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS


# Load document
loader = TextLoader(
    "rag/data/game_reviews.md",
    encoding="utf-8"
)

documents = loader.load()


# Split document into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)


# Create lightweight embeddings
embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# Create FAISS vector store
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)


# Save vector store
vector_store.save_local("rag/faiss_index")

print("FAISS index created successfully.")