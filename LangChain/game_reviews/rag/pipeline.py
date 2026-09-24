from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool
from langchain.agents import create_agent
from app.tools.db_tools import get_customers,get_customer,get_reviews,get_review
from dotenv import load_dotenv
from collections import deque

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = FAISS.load_local(
    "rag/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


def search_documents(query: str) -> str:
    """Search the game review documents for relevant information."""

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant documents found."

    return "\n\n".join(
        document.page_content
        for document in documents
    )


rag_tool = StructuredTool.from_function(
    func=search_documents,
    name="search_documents",
    description="Search the game review documents for information about games, ratings, reviews, and other documented information."
)


customers_tool = StructuredTool.from_function(
    func=get_customers,
    name="get_customers",
    description="Get all customers from the database."
)


customer_tool = StructuredTool.from_function(
    func=get_customer,
    name="get_customer",
    description="Get one customer using their customer ID."
)


reviews_tool = StructuredTool.from_function(
    func=get_reviews,
    name="get_reviews",
    description="Get all game reviews from the database."
)


review_tool = StructuredTool.from_function(
    func=get_review,
    name="get_review",
    description="Get one game review using its review ID."
)


tools = [rag_tool,customers_tool,customer_tool,reviews_tool,review_tool]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


system_prompt = """
You are an assistant for an online game review system.

You have access to:
1. A document search tool for game review documents.
2. Database tools for customer and review information.

Use the document search tool when the question requires information
from the documents.

Use database tools when the user asks for actual customer or
review data from the database.

You can use multiple tools when required.

Do not invent or modify database information.

Answer the user's question directly and concisely.
Do not add unnecessary explanations or information that was not asked for.
"""

chat_history = deque(maxlen=10)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt)


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


if __name__ == "__main__":
    while True:
        question = input("\nAsk your question (type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)