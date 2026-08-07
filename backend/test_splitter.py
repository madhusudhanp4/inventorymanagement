from rag.document_loader import load_documents
from rag.text_splitter import split_documents

docs = load_documents("documents")

chunks = split_documents(docs)

print("Documents:", len(docs))
print("Chunks:", len(chunks))
print()
print(chunks[0])