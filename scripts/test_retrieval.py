from pathlib import Path

from src.embeddings import embed_text
from src.retrieval import (
    load_embedding_records,
    retrieve_top_k,
)


EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)

query = (
    "Our TIBCO BusinessWorks application cannot connect to the JMS broker. "
    "What are the possible causes and troubleshooting steps?"
)

records = load_embedding_records(
    EMBEDDING_FILE
)

query_embedding = embed_text(query)

results = retrieve_top_k(
    query_embedding,
    records,
    top_k=5,
)


print("\nQUERY")
print("-" * 70)
print(query)

print("\nTOP 5 RETRIEVAL RESULTS")
print("-" * 70)

for rank, result in enumerate(results, start=1):
    print(
        f"{rank}. "
        f"{result['chunk_id']} | "
        f"{result['title']} | "
        f"{result['section']} | "
        f"score={result['similarity_score']:.4f}"
    )


print("\nRETRIEVED CONTENT")
print("=" * 70)

for rank, result in enumerate(results, start=1):
    print(f"\n[{rank}] {result['chunk_id']}")
    print(result["content"])