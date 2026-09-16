from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# texts = [
#     "The weather is not hot today.",
#     "Today the weather is cold."
# ]

# embeddings = model.encode(texts)

# similarity = model.similarity(
#     embeddings[0],
#     embeddings[1]
# )
texts = [
    "Python is a programming language.",
    "Python is commonly used for software development.",
    "I like eating pizza."
]

embeddings = model.encode(texts)

print(model.similarity(embeddings[0], embeddings[1]))
print(model.similarity(embeddings[0], embeddings[2]))

#print("Similarity:", similarity)