from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = None   # loaded once, reused everywhere


def get_model():
    global model
    if model is None:
        print(f"embedding model: {MODEL_NAME}")
        model = SentenceTransformer(MODEL_NAME)
    return model


def encode_text(texts):
    if isinstance(texts, str):
        texts = [texts]

    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.astype("float32")