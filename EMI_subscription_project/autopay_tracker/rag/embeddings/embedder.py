from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]):
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


def embed_single_text(text: str):
    embedding = model.encode([text], convert_to_numpy=True)
    return embedding[0]