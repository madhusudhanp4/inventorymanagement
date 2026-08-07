from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.tracing import tracer


def split_documents(documents):
    with tracer.start_as_current_span("rag.chunk") as span:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = []

        for doc in documents:
            chunks.extend(splitter.split_text(doc))

        span.set_attribute(
            "rag.chunk_count",
            len(chunks)
        )

        span.set_attribute(
            "rag.chunk_size",
            500
        )

        return chunks