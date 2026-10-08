from collections import Counter
from pathlib import Path

from src.documents import load_corpus
from src.chunking import chunk_corpus


KNOWLEDGE_ROOT = Path("data/knowledge")


documents = load_corpus(KNOWLEDGE_ROOT)

chunks = chunk_corpus(documents)


print("=" * 70)
print("ENTERPRISE RAG - CHUNK INSPECTION")
print("=" * 70)

print(f"\nDocuments : {len(documents)}")
print(f"Chunks    : {len(chunks)}")


print("\nCHUNKS BY DOCUMENT")
print("-" * 70)

chunk_counts = Counter(
    chunk.document_id
    for chunk in chunks
)

for document_id, count in sorted(chunk_counts.items()):
    print(f"{document_id:35} {count:3} chunks")


print("\nCHUNK SIZE ANALYSIS")
print("-" * 70)

word_counts = [
    len(chunk.content.split())
    for chunk in chunks
]

print(f"Smallest chunk : {min(word_counts)} words")
print(f"Largest chunk  : {max(word_counts)} words")
print(
    f"Average chunk  : "
    f"{sum(word_counts) / len(word_counts):.1f} words"
)


small_chunks = [
    chunk
    for chunk in chunks
    if len(chunk.content.split()) < 15
]


print(f"\nChunks below 15 words: {len(small_chunks)}")

for chunk in small_chunks:
    words = len(chunk.content.split())

    print(
        f"{words:3} words | "
        f"{chunk.chunk_id} | "
        f"{chunk.section}"
    )