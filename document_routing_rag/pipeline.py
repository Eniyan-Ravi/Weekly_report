from embeddings.model import encode_text
from routing.document_router import route_query
from retrieval.semantic_search import search_document


def run_query(user_query, top_k=3):
    query_embedding = encode_text(user_query)   # shape (1, dimension)

    doc_id, folder_name, route_distance = route_query(query_embedding)
    results = search_document(folder_name, query_embedding, top_k=top_k)

    print(f"\nQuery: {user_query}")
    print(f"Routed to document: {doc_id}  (route distance: {route_distance:.4f})")
    for r in results:
        print(f"   -> ({r['distance']:.4f}) {r['chunk']}")


user_query = input("Enter your question: ")
run_query(user_query)