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


EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)


question = (
    "Our Axway API Gateway is returning HTTP 429 Too Many Requests. "
    "What are the possible root causes, troubleshooting steps, "
    "and recommended resolutions for rate limits and quotas?"
)


records = load_embedding_records(
    EMBEDDING_FILE
)

query_embedding = embed_text(question)

results = retrieve_top_k(
    query_embedding,
    records,
    top_k=5,
)

context = build_context(results)

prompt = build_prompt(
    question,
    context,
)

answer = generate_answer(prompt)

print("\nRAG ANSWER")
print("=" * 70)
print(answer)