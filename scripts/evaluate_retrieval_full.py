import json
from pathlib import Path

from src.embeddings import embed_text
from src.retrieval import retrieve_top_k


GOLDEN_FILE = Path(
    "data/evaluation/golden_questions.json"
)

EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)


golden_questions = json.loads(
    GOLDEN_FILE.read_text(encoding="utf-8")
)

embedding_records = json.loads(
    EMBEDDING_FILE.read_text(encoding="utf-8")
)


def normalize_source(source: str) -> str:
    return (
        source
        .replace("\\", "/")
        .replace("data/knowledge/", "")
        .lower()
    )


print("Golden questions:", len(golden_questions))
print("Embedding records:", len(embedding_records))
print("\nFULL RETRIEVAL EVALUATION")
print("=" * 70)

recall_scores = []

for item in golden_questions:
    query_embedding = embed_text(
        item["question"]
    )

    results = retrieve_top_k(
        query_embedding,
        embedding_records,
        top_k=5,
    )

    expected_sources = {
        normalize_source(source)
        for source in item["expected_sources"]
    }

    retrieved_sources = {
        normalize_source(result["source"])
        for result in results
    }

    matched_sources = (
        expected_sources & retrieved_sources
    )

    recall = (
        len(matched_sources)
        / len(expected_sources)
    )

    recall_scores.append(recall)

    print(
        f"{item['id']} | "
        f"Recall@5={recall:.4f} | "
        f"Matched={len(matched_sources)}/"
        f"{len(expected_sources)}"
    )


average_recall = (
    sum(recall_scores)
    / len(recall_scores)
)

print("-" * 70)
print(
    f"Average Recall@5: "
    f"{average_recall:.4f}"
)