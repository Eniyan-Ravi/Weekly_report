import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_groq import ChatGroq

load_dotenv()

#Loading embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


#Loading FAISS
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


#Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

#LLM

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


#Format retrieved Documents
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


#Prompt
prompt = ChatPromptTemplate.from_template("""
You are an assistant for an online game review system.

Answer the user's question using only the provided context.

Do not use outside knowledge.
If the context does not contain enough information to answer,
say: "The information is not available in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
""")


#Create RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


#question
question = input("Enter the query: ")

# Generate answer
answer = rag_chain.invoke(question)

print("\nAnswer:")
print(answer)

# Retrieve relevant chunks
retrieved_docs = retriever.invoke(question)

print("\nRelevant Retrieved Chunks:")

for i, doc in enumerate(retrieved_docs, start=1):
    print(f"\n--- Chunk {i} ---")
    print(doc.page_content)
    print("Metadata:", doc.metadata)

