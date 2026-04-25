from fastapi import FastAPI
from pydantic import BaseModel
from app.services.rag_service import RagService

app = FastAPI(title="Backend RAG")

rag_service = RagService()


class AskRequest(BaseModel):
    question: str
    top_k: int | None = 4


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask_question(data: AskRequest):
    return rag_service.ask(data.question, data.top_k)