from rag.document_loader import load_documents

docs = load_documents("documents")

print("Documents Found:", len(docs))

for i, doc in enumerate(docs):
    print(f"Document {i+1} length:", len(doc))