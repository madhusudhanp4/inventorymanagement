from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import store_chunks, get_chunks

docs = load_documents("documents")

chunks = split_documents(docs)

store_chunks(chunks)

data = get_chunks()

print("Stored Documents:", len(data["documents"]))