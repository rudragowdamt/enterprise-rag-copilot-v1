import json
from pathlib import Path


def load_embedding_records(path: Path) -> list[dict]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )
def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sum(
        a * a
        for a in vector_a
    ) ** 0.5

    magnitude_b = sum(
        b * b
        for b in vector_b
    ) ** 0.5

    return dot_product / (
        magnitude_a * magnitude_b
    )
def retrieve_top_k(
    query_embedding: list[float],
    records: list[dict],
    top_k: int = 5,
) -> list[dict]:

    scored_records = []

    for record in records:
        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_records.append(
            {
                **record,
                "similarity_score": score,
            }
        )

    scored_records.sort(
        key=lambda item: item["similarity_score"],
        reverse=True,
    )

    return scored_records[:top_k]