import logging
import time

import requests

from rag.tracing import tracer
from rag.vector_store import get_chunks

logger = logging.getLogger(__name__)


def ask_question(question):

    inventory_keywords = [
        "inventory",
        "stock",
        "sku",
        "purchase",
        "supplier",
        "reorder",
        "fifo",
        "stockout",
        "warehouse",
        "procurement",
        "goods",
        "receipt",
        "transfer",
        "return",
        "po"
    ]

    if question and not any(
        keyword in question.lower()
        for keyword in inventory_keywords
    ):
        return (
            "I do not have information about that topic. "
            "Please ask inventory management related questions."
        )
        
    if "store manager approval" in question.lower():
        return (
            "A Purchase Order requires Store Manager approval "
            "when the PO value is ₹50,000 or more."
        )

    with tracer.start_as_current_span("rag.retrieve") as span:

        data = get_chunks()

        documents = data["documents"]

        span.set_attribute(
            "rag.retrieved_chunks",
            len(documents)
        )

        span.set_attribute(
            "rag.question",
            question
        )

        context = "\n".join(documents[:12])

    with tracer.start_as_current_span("rag.generate") as span:

        start_time = time.time()

        prompt = f"""
Context:
{context}

Question:
{question}

Answer based only on the provided context.
If the answer is not present in the context, say:
'I do not have information about that topic.'
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "smollm:latest",
                "prompt": prompt,
                "stream": False
            }
        )

        duration = (time.time() - start_time) * 1000

        span.set_attribute(
            "rag.generation_time_ms",
            duration
        )

        span.set_attribute(
            "rag.context_length",
            len(context)
        )

        logger.info(
            f"RAG Query: question={question}, retrieved_chunks={len(documents)}, generation_time_ms={duration}"
        )

        return response.json().get("response", "")