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


print(
    "Golden questions:",
    len(golden_questions),
)

print(
    "Embedding records:",
    len(embedding_records),
)
def normalize_source(source: str) -> str:
    return (
        source
        .replace("\\", "/")
        .replace("data/knowledge/", "")
        .lower()
    )
first_question = golden_questions[0]

query = first_question["question"]

query_embedding = embed_text(query)

results = retrieve_top_k(
    query_embedding,
    embedding_records,
    top_k=5,
)


print("\nQUESTION")
print("-" * 70)
print(query)

print("\nEXPECTED SOURCES")
print("-" * 70)

for source in first_question["expected_sources"]:
    print(source)


print("\nTOP 5 RETRIEVED")
print("-" * 70)

for rank, result in enumerate(results, start=1):
    print(
        f"{rank}. "
        f"{result['source']} | "
        f"{result['chunk_id']} | "
        f"score={result['similarity_score']:.4f}"
    )
expected_sources = {
    normalize_source(source)
    for source in first_question["expected_sources"]
}

retrieved_sources = {
    normalize_source(result["source"])
    for result in results
}

matched_sources = (
    expected_sources & retrieved_sources
)

recall_at_5 = (
    len(matched_sources)
    / len(expected_sources)
)


print("\nEVALUATION")
print("-" * 70)

print(
    "Matched sources:",
    len(matched_sources),
    "/",
    len(expected_sources),
)

print(
    "Recall@5:",
    round(recall_at_5, 4),
)