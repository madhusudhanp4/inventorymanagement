from pathlib import Path

from rag.tracing import tracer


def load_documents(folder_path):
    with tracer.start_as_current_span("rag.document_load") as span:

        documents = []

        folder = Path(folder_path)

        for file in folder.iterdir():
            if file.suffix.lower() in [".txt", ".md"]:
                text = file.read_text(encoding="utf-8").strip()

                if text:
                    documents.append(text)

        span.set_attribute(
            "rag.document_count",
            len(documents)
        )

        span.set_attribute(
            "rag.folder",
            folder_path
        )

        return documents
