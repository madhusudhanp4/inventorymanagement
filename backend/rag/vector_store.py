import chromadb
import logging

from rag.tracing import tracer

logger = logging.getLogger(__name__)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="inventory_manual"
)


def store_chunks(chunks):

    with tracer.start_as_current_span("rag.embed") as span:

        ids = [str(i) for i in range(len(chunks))]

        embeddings = [[0.0] * 10 for _ in chunks]

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

        span.set_attribute(
            "rag.embedding_count",
            len(chunks)
        )

        span.set_attribute(
            "rag.embedding_dimension",
            10
        )

        logger.info(
            f"Ingestion completed. chunks_created={len(chunks)}"
        )

        print(f"Stored {len(chunks)} chunks")


def get_chunks():
    return collection.get()