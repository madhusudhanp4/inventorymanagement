from fastapi import APIRouter
from pydantic import BaseModel

from rag.rag_service import ask_question

router = APIRouter()


class RAGRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_rag(request: RAGRequest):
    answer = ask_question(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }