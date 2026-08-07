import time

from dotenv import load_dotenv

load_dotenv()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)


def ingest():

    with tracer.start_as_current_span("rag.document_load") as span:

        start = time.time()

        docs = TextLoader(
            "rag/inventory_manual.md",
            encoding="utf-8"
        ).load()

        span.set_attribute(
            "rag.source",
            "inventory_manual.md"
        )

        span.set_attribute(
            "rag.document_count",
            len(docs)
        )

    with tracer.start_as_current_span("rag.chunk") as span:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(docs)

        span.set_attribute(
            "rag.chunk_size",
            600
        )

        span.set_attribute(
            "rag.chunk_overlap",
            50
        )

        span.set_attribute(
            "rag.chunk_count",
            len(chunks)
        )

    with tracer.start_as_current_span("rag.embed") as span:

        embeddings = OllamaEmbeddings(
            model="smollm:latest"
        )

        vectorstore = Chroma(
            collection_name="inventory_manual",
            embedding_function=embeddings,
            persist_directory="./chroma_db"
        )

        vectorstore.add_documents(chunks)

        span.set_attribute(
            "rag.embedding_model",
            "smollm:latest"
        )

        span.set_attribute(
            "rag.vectors_stored",
            len(chunks)
        )

        duration = round(
            (time.time() - start) * 1000,
            2
        )

        print(
            f"POC-07 | chunks={len(chunks)} | embedding_time_ms={duration}"
        )

    print(
        f"Successfully stored {len(chunks)} chunks in ChromaDB"
    )


if __name__ == "__main__":
    ingest()