from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool

from langchain.agents import create_agent

from app.tools.db_tools import (
    get_customers,
    get_customer,
    get_reviews,
    get_review
)

from dotenv import load_dotenv
from collections import deque


# Load environment variables
load_dotenv()


# --------------------------------------------------
# Embeddings
# --------------------------------------------------

embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# --------------------------------------------------
# FAISS Vector Store
# --------------------------------------------------

vector_store = FAISS.load_local(
    "rag/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# Retriever
# --------------------------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# --------------------------------------------------
# Document Search Tool
# --------------------------------------------------

def search_documents(query: str) -> str:

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant documents found."

    return "\n\n".join(
        document.page_content
        for document in documents
    )


# --------------------------------------------------
# RAG Tool
# --------------------------------------------------

rag_tool = StructuredTool.from_function(
    func=search_documents,
    name="search_documents",
    description=(
        "Search the game review documentation "
        "and return relevant information."
    )
)


# --------------------------------------------------
# Database Tools
# --------------------------------------------------

customers_tool = StructuredTool.from_function(
    func=get_customers,
    name="get_customers",
    description="Get all customers from the database."
)

customer_tool = StructuredTool.from_function(
    func=get_customer,
    name="get_customer",
    description="Get a specific customer from the database."
)

reviews_tool = StructuredTool.from_function(
    func=get_reviews,
    name="get_reviews",
    description="Get game reviews from the database."
)

review_tool = StructuredTool.from_function(
    func=get_review,
    name="get_review",
    description="Get a specific game review from the database."
)


# --------------------------------------------------
# Tools
# --------------------------------------------------

tools = [
    rag_tool,
    customers_tool,
    customer_tool,
    reviews_tool,
    review_tool
]


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# --------------------------------------------------
# System Prompt
# --------------------------------------------------

system_prompt = """
You are an assistant for an online game review system.

Use the document search tool when the user asks
about information contained in the documentation.

Use the database tools when the user asks about
actual customer or review data.

You may use multiple tools when necessary.

Do not invent customer or review information.

Do not modify the database.

Keep answers concise and accurate.
"""


# --------------------------------------------------
# Conversation History
# --------------------------------------------------

chat_history = deque(maxlen=10)


# --------------------------------------------------
# Agent
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


# --------------------------------------------------
# Main RAG Function
# --------------------------------------------------

def answer_question(question: str) -> str:

    chat_history.append({
        "role": "user",
        "content": question
    })

    result = agent.invoke({
        "messages": list(chat_history)
    })

    assistant_message = result["messages"][-1]

    chat_history.append(assistant_message)

    return assistant_message.content


# --------------------------------------------------
# CLI
# --------------------------------------------------

if __name__ == "__main__":
    import time

    print("RAG service started.")

    while True:
        time.sleep(3600)