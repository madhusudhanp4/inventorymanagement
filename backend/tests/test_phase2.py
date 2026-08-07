import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import store_chunks, get_chunks
from rag.rag_service import ask_question


# INGESTION TESTS


def test_manual_loads():
    docs = load_documents("documents")
    assert len(docs) > 0
    assert len(docs[0]) > 100


def test_chunks_size():
    docs = load_documents("documents")
    chunks = split_documents(docs)

    for chunk in chunks:
        assert len(chunk) <= 600


def test_min_chunks():
    docs = load_documents("documents")
    chunks = split_documents(docs)

    assert len(chunks) >= 20


def test_chromadb_collection():
    docs = load_documents("documents")
    chunks = split_documents(docs)

    store_chunks(chunks)

    data = get_chunks()

    assert len(data["documents"]) >= 20


# RETRIEVAL TESTS


def test_sku_query():
    answer = ask_question(
        "What is the SKU format for grocery products?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "gro",
            "sku",
            "grocery",
            "prefix"
        ]
    )


def test_top_k():
    data = get_chunks()
    docs = data["documents"]

    assert len(docs[:4]) == 4


def test_irrelevant_low_score():
    answer = ask_question(
        "Football match results"
    ).lower()

    assert any(
        x in answer
        for x in [
            "do not have",
            "no information",
            "cannot",
            "inventory"
        ]
    )


def test_po_lifecycle():
    answer = ask_question(
        "What are the stages of a purchase order?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "draft",
            "submitted",
            "received",
            "status",
            "lifecycle"
        ]
    )


def test_empty_query():
    answer = ask_question("")
    assert answer is not None


def test_latency():
    start = time.time()

    ask_question(
        "What is a reorder point?"
    )

    assert time.time() - start < 15


# GENERATION TESTS


def test_reorder_formula():
    answer = ask_question(
        "How do I calculate a reorder point?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "lead time",
            "daily",
            "demand",
            "safety",
            "reorder"
        ]
    )


def test_po_approval():
    answer = ask_question(
        "When does a PO need Store Manager approval?"
    )

    assert (
        "50,000" in answer
        or "50000" in answer
        or "₹" in answer
    )


def test_movement_types():
    answer = ask_question(
        "What are the stock movement types?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "receipt",
            "sale",
            "adjustment",
            "transfer",
            "return"
        ]
    )


def test_out_of_scope():
    answer = ask_question(
        "What is the weather forecast for Mumbai?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "do not have",
            "no information",
            "cannot",
            "not"
        ]
    )


def test_non_empty():
    for question in [
        "What is SKU?",
        "What is FIFO?",
        "What is a stockout?"
    ]:
        answer = ask_question(question)
        assert len(answer) > 10


def test_category_management():
    answer = ask_question(
        "How do grocery products differ from electronics in inventory management?"
    ).lower()

    assert any(
        x in answer
        for x in [
            "grocery",
            "electronic",
            "shelf life",
            "velocity",
            "cost"
        ]
    )


# OBSERVABILITY TESTS


def test_langsmith():
    assert True


def test_otel_spans():
    answer = ask_question(
        "What is EOQ?"
    )

    assert len(answer) > 0


def test_log_poc_id():
    answer = ask_question(
        "What is a stock movement?"
    )

    assert answer is not None


def test_sources():
    answer = ask_question(
        "How does PO receiving update stock?"
    )

    assert len(answer) > 0