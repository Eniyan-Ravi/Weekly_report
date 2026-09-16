import os
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent.parent / "documents"


def load_documents() -> list[dict]:
  #list of dicts, document -> filename and raw text.
    documents = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".md"):
            filepath = DOCUMENTS_DIR / filename
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            documents.append({
                "source": filename,
                "content": content
            })

    return documents


def chunk_documents(documents: list[dict], max_chunk_size: int = 500) -> list[dict]:

    chunks = []

    for doc in documents:
        content = doc["content"].strip()
        source = doc["source"]

        if len(content) <= max_chunk_size:
            chunks.append({
                "source": source,
                "chunk_id": f"{source}-0",
                "text": content
            })
        else:
            paragraphs = content.split("\n")
            current_chunk = ""
            chunk_index = 0

            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) <= max_chunk_size:
                    current_chunk += paragraph + "\n"
                else:
                    chunks.append({
                        "source": source,
                        "chunk_id": f"{source}-{chunk_index}",
                        "text": current_chunk.strip()
                    })
                    chunk_index += 1
                    current_chunk = paragraph + "\n"

            if current_chunk.strip():
                chunks.append({
                    "source": source,
                    "chunk_id": f"{source}-{chunk_index}",
                    "text": current_chunk.strip()
                })

    return chunks