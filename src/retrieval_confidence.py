MIN_SIMILARITY_SCORE = 0.30

INSUFFICIENT_EVIDENCE_MESSAGE = (
    "I could not find sufficiently relevant information "
    "in the knowledge base to answer this question."
)


def has_sufficient_evidence(results: list[dict]) -> bool:
    if not results:
        return False

    best_score = max(
        item["similarity_score"]
        for item in results
    )

    return best_score >= MIN_SIMILARITY_SCORE
