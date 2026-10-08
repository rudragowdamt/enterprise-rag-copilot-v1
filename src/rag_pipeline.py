from pathlib import Path

from src.embeddings import embed_text
from src.retrieval import (
    load_embedding_records,
    retrieve_top_k,
)
from src.generation import (
    build_context,
    build_prompt,
    generate_answer,
)


DEFAULT_EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)


def ask_rag(
    question: str,
    top_k: int = 5,
    embedding_file: Path = DEFAULT_EMBEDDING_FILE,
) -> dict:

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    records = load_embedding_records(
        embedding_file
    )

    query_embedding = embed_text(
        question
    )

    results = retrieve_top_k(
        query_embedding,
        records,
        top_k=top_k,
    )

    context = build_context(
        results
    )

    prompt = build_prompt(
        question,
        context,
    )

    answer = generate_answer(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "sources": results,
    }