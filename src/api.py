from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_pipeline import ask_rag


app = FastAPI(
    title="Enterprise Integration RAG Copilot",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    result = ask_rag(
        request.question
    )

    clean_sources = [
        {
            "chunk_id": source["chunk_id"],
            "document_id": source["document_id"],
            "title": source["title"],
            "section": source["section"],
            "source": source["source"],
            "similarity_score": source["similarity_score"],
        }
        for source in result["sources"]
    ]

    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": clean_sources,
    }