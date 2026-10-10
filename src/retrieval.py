
import json
import re
from pathlib import Path


STOP_WORDS = {
    "how", "do", "i", "a", "an", "the", "to",
    "in", "on", "for", "of", "and", "or",
    "can", "my", "is", "with", "troubleshoot",
    "diagnose", "failure", "failures", "step",
    "steps", "verify", "check",
}


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

    denominator = magnitude_a * magnitude_b

    if denominator == 0:
        return 0.0

    return dot_product / denominator


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords for section ranking."""

    words = re.findall(
        r"[a-z0-9]+",
        text.lower(),
    )

    return {
        word
        for word in words
        if len(word) > 2
        and word not in STOP_WORDS
    }


def calculate_section_boost(
    question: str,
    section: str,
) -> float:
    """Boost sections matching the question's keywords."""

    question_words = extract_keywords(question)
    section_words = extract_keywords(section)

    matches = question_words.intersection(
        section_words
    )

    # Maximum additional ranking score: 0.40
    return min(len(matches) * 0.20, 0.40)


def retrieve_top_k(
    query_embedding: list[float],
    records: list[dict],
    top_k: int = 5,
    query_text: str | None = None,
) -> list[dict]:

    scored_records = []

    for record in records:

        similarity = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_record = {
            **record,
            "similarity_score": similarity,
        }

        if query_text:
            boost = calculate_section_boost(
                query_text,
                record.get("section", ""),
            )

            scored_record["ranking_score"] = (
                similarity + boost
            )

        scored_records.append(scored_record)

    sort_field = (
        "ranking_score"
        if query_text
        else "similarity_score"
    )

    scored_records.sort(
        key=lambda item: item[sort_field],
        reverse=True,
    )

    return scored_records[:top_k]
