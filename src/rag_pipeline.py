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
from src.cache import (
    get_cached_result,
    save_cached_result,
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
    
    cached_result = get_cached_result(
    question
    )

    if cached_result is not None:
        cached_result["cache_hit"] = True
        return cached_result

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
    clean_sources = []

    for source in results:
        clean_source = {
            key: value
            for key, value in source.items()
            if key != "embedding"
        }
        clean_sources.append(
            clean_source
        )
    result = {
        "question": question,
        "answer": answer,
        "sources": clean_sources,
        "cache_hit": False,
    }

    save_cached_result(
        question,
        result,
    )

    return result