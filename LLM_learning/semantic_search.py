from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

documents = [
    "Python is a programming language used for software development.",
    "FastAPI is a modern Python framework for building APIs.",
    "SQL is used to store and retrieve data from databases.",
    "Machine learning allows computers to learn patterns from data.",
    "I enjoy eating pizza and burgers."
]

query = "How can I build an API using Python?"

document_embeddings = model.encode(documents)
query_embedding = model.encode([query])

scores = cosine_similarity(query_embedding,document_embeddings)[0]

for document, score in zip(documents, scores):
    print(f"{score:.4f} -> {document}")

best_index = scores.argmax()

print("\nMost relevant document:")
print(documents[best_index])