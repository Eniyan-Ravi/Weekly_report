import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_core.tools import StructuredTool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from sympy import true


BASE_DIR = Path(__file__).parent
KNOWLEDGE_FILE = BASE_DIR / "product_catalog.md"
INDEX_DIR = BASE_DIR / "faiss_index"


#Build FAISS index
def build_index():
    print("Building FAISS index...")

    loader = TextLoader(str(KNOWLEDGE_FILE), encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    INDEX_DIR.mkdir(exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))

    print(f"Indexed {len(chunks)} chunks.")
    return vectorstore


vectorstore = build_index()


#semantic search
def search_product_catalog(query: str) -> str:
    """Search the NovaTech catalog for products, prices, specifications,
    features, warranty, and return-policy information."""

    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "No relevant information was found in the catalog."

    return "\n\n".join(
        f"Result {i}:\n{doc.page_content}"
        for i, doc in enumerate(results, start=1)
    )


catalog_tool = StructuredTool.from_function(
    func=search_product_catalog,
    name="search_product_catalog",
    description=(
        "Search the NovaTech product catalog. Use it for questions "
        "about products, prices, specifications, features, warranty, "
        "or return policy."
    )
)


#LLM 
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

llm_with_tools = llm.bind_tools([catalog_tool])


#LangGraph state
class State(MessagesState):
    pass


#LLM node
def call_llm(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


#Conditional routing
def should_continue(state: State):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"


#Tool node
tool_node = ToolNode([catalog_tool])


#Build graph
graph = StateGraph(State)

graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

graph.add_edge("tools", "llm")


#Checkpointing
checkpointer = InMemorySaver()

app = graph.compile(checkpointer=checkpointer)


SYSTEM_MESSAGE = """
You are a helpful NovaTech product assistant.

Use the search_product_catalog tool whenever the user asks for
information that should come from the product catalog.

Do not invent prices, specifications, warranty rules, or return rules.

If the catalog does not contain the requested information, say so.
"""


def main():
    thread_id = "product_support_001"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("\nNovaTech Product Assistant")
    print("Type 'exit' to stop.\n")

    first_message = True

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            continue

        if first_message:
            messages = [
                SystemMessage(content=SYSTEM_MESSAGE),
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            first_message = False
        else:
            messages = [
                {
                    "role": "user",
                    "content": user_input
                }
            ]

        result = app.invoke(
            {"messages": messages},
            config
        )

        print("\nAssistant:", result["messages"][-1].content)
        print()


if __name__ == "__main__":
    main()
