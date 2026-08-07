#import logging_config

from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import store_chunks

documents = load_documents("documents")

chunks = split_documents(documents)

store_chunks(chunks)

print("Ingestion Complete")