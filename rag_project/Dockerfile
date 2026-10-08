FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY documents/ documents/
COPY indexes/ indexes/

COPY ingest.py .
COPY retriever.py .

COPY doc_router.faiss .
COPY doc_router.json .

CMD ["python", "retriever.py"]