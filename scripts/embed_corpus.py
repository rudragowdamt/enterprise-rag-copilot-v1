import json
from pathlib import Path

from src.documents import load_corpus
from src.chunking import chunk_corpus
from src.embeddings import create_bedrock_client, embed_text


KNOWLEDGE_ROOT = Path("data/knowledge")
OUTPUT_FILE = Path("data/embeddings/chunk_embeddings.json")
documents = load_corpus(KNOWLEDGE_ROOT)
chunks = chunk_corpus(documents)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
client = create_bedrock_client()

records = []

print("\nEmbedding all chunks...")

for index, chunk in enumerate(chunks, start=1):
    vector = embed_text(
        chunk.content,
        client=client,
    )

    records.append(
        {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "title": chunk.title,
            "section": chunk.section,
            "doc_type": chunk.doc_type,
            "system": chunk.system,
            "environment": chunk.environment,
            "source": str(chunk.source),
            "content": chunk.content,
            "embedding": vector,
        }
    )

    print(
        f"[{index}/{len(chunks)}] "
        f"{chunk.chunk_id} | "
        f"dimensions={len(vector)}"
    )
    OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_FILE.write_text(
    json.dumps(records, indent=2),
    encoding="utf-8",
)

print(
    f"\nSaved {len(records)} embeddings to:"
    f"\n{OUTPUT_FILE}"
)