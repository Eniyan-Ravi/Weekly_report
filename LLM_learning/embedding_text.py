from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

text = ["Hi, How are you. I am going to my home town this sunday.",
"How is the weather today.",
"It is rainy."
]

embedding = model.encode(text)

print("Text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nEmbedding dimensions:")
print(len(embedding))