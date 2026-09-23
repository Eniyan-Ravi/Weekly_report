# Online Game Review System

## 1. System Overview

The Online Game Review System allows customers to submit ratings and written reviews for games. The system stores customer information and game review information in a database and exposes the functionality through a FastAPI backend.

The current database contains a `customers` table and a `game_reviews` table. A customer has a name, email, and age. A game review contains the game name, customer ID, rating, written review, and game price.

The FastAPI application is responsible for exposing API endpoints and handling database operations. The RAG system is kept separate from the API so that retrieval, embeddings, vector storage, and future AI functionality can be modified without tightly coupling them to the API layer.

## 2. Customer Information

A customer represents a person who can submit game reviews.

Customer information includes:

- Customer ID
- Name
- Email
- Age

The email is unique for each customer. Customer requests are validated before being stored.

## 3. Game Review Information

Each game review contains:

- Review ID
- Game name
- Customer ID
- Rating
- Written review
- Game price

The rating is represented on a scale from 1 to 5. The written review contains the customer's description or opinion about the game.

## 4. Review Data

Example review records can contain information such as:

- Game: Elden Ring
- Rating: 5
- Review: The open world is challenging and exploration is rewarding.
- Price: 59.99

- Game: Cyberpunk 2077
- Rating: 4
- Review: The story and characters are engaging, although some areas could be improved.
- Price: 49.99

- Game: Minecraft
- Rating: 5
- Review: The sandbox gameplay provides a large amount of freedom and replayability.
- Price: 29.99

These records provide knowledge that can later be retrieved by a RAG system.

## 5. Possible User Questions

The AI system can use the review knowledge base to answer questions such as:

- What do customers think about Elden Ring?
- Which games have highly rated reviews?
- What are common opinions about Minecraft?
- Show reviews related to open-world games.
- What did customers say about the story of a game?
- Which games received a rating of 5?
- What reviews mention replayability?
- What is the price of a particular game?
- Summarize the customer reviews for a game.

## 6. RAG Responsibilities

The RAG folder is responsible for the retrieval pipeline.

A basic pipeline is:

Documents
→ Chunking
→ Embedding
→ FAISS Vector Store
→ Similarity Search
→ Retrieved Context

The RAG layer should not directly contain FastAPI route definitions. This separation allows the retrieval implementation to be changed later without changing the API structure.

## 7. Embedding

The review documents can be converted into numerical vectors using a sentence-transformer embedding model.

The current learning setup uses:

`sentence-transformers/all-MiniLM-L6-v2`

The embedding layer should expose a standard interface so that the embedding model can be replaced later if required.

## 8. Vector Store

FAISS can be used as the local vector store for the review knowledge base.

The vector store should contain:

- Embedded review chunks
- Original chunk text
- Source information
- Useful metadata such as game name and review ID when available

A user query can be embedded and compared against the stored vectors to retrieve relevant reviews.

## 9. Retrieval

The retriever receives a natural-language question and returns the most relevant review chunks.

Example:

Question:

`What do customers think about the gameplay of Elden Ring?`

Possible retrieved information:

`The open world is challenging and exploration is rewarding.`

The retrieved context can then be passed to an LLM for answer generation.

## 10. FastAPI Responsibilities

The API folder is responsible for:

- Customer CRUD operations
- Game review creation and retrieval
- Request validation
- Database access
- Future API endpoints
- Providing data to external clients or AI agents through tools

The current FastAPI application creates the database tables and registers the customer router.

## 11. Agent and Tool Integration

The LangChain agent should not directly depend on the internal database implementation.

Instead, API operations can be exposed as tools.

Example tools:

- `create_customer`
- `get_customer`
- `get_customers`
- `update_customer`
- `delete_customer`
- `create_review`
- `get_review`
- `get_reviews`
- `get_reviews_by_game`

The agent can decide when a tool is required based on the user's request.

For example:

User:

`Add my review for Elden Ring with a rating of 5.`

Agent:

`create_review(...)`

Another request:

`What do customers think about Elden Ring?`

Agent:

`RAG retrieval → retrieve relevant reviews → LLM generates answer`

## 12. Separation Between API and RAG

The project should maintain two independent responsibilities.

### API

```text
api/
├── main.py
├── database.py
├── model.py
├── schema.py
└── routes/
    ├── customer.py
    └── review.py
```

### RAG

```text
rag/
├── data/
│   └── game_reviews.md
├── embeddings.py
├── indexing.py
├── vector_store.py
├── retriever.py
└── pipeline.py
```

The API handles structured database operations.

The RAG system handles unstructured semantic retrieval.

## 13. Future Extension

The architecture should allow additional tools and retrieval methods to be added without rewriting the existing system.

Possible future additions include:

- Game search tool
- Review search tool
- Game price lookup
- Rating aggregation
- Review summarization
- Sentiment analysis
- Hybrid search using semantic search and BM25
- Multiple vector stores
- Additional database entities
- Additional LangChain tools

The agent can act as the orchestration layer that decides whether to use an API tool, the RAG retriever, or both.

## 14. Example Agent Workflow

A request such as:

`Find customer reviews for Elden Ring and summarize what they say about gameplay.`

can follow this workflow:

User Query
→ LangChain Agent
→ Review Retrieval Tool / RAG Retriever
→ Relevant Review Chunks
→ LLM
→ Final Answer

A request such as:

`Add a new customer`

can follow:

User Query
→ LangChain Agent
→ `create_customer` API Tool
→ FastAPI
→ Database
→ Tool Result
→ Final Answer

This separation makes the API and RAG components independently maintainable while allowing the LangChain agent to orchestrate both.
