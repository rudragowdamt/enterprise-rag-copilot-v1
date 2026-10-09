import json
import os
from pathlib import Path

from src.documents import load_corpus
from src.chunking import chunk_corpus
from src.embeddings import create_bedrock_client, embed_text

KNOWLEDGE_ROOT = Path("data/knowledge")
INDEX_FILE = Path("data/embeddings/chunk_embeddings.json")

def main():
    documents = load_corpus(KNOWLEDGE_ROOT)
    chunks = chunk_corpus(documents)

    if INDEX_FILE.exists():
        existing = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    else:
        existing = []

    stored = {record["chunk_id"]: record for record in existing}

    new_or_changed = [
        chunk for chunk in chunks
        if chunk.chunk_id not in stored
        or chunk.content != stored[chunk.chunk_id]["content"]
    ]

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Reusable: {len(chunks) - len(new_or_changed)}")
    print(f"New/changed: {len(new_or_changed)}")

    client = create_bedrock_client() if new_or_changed else None
    records = []

    for index, chunk in enumerate(chunks, start=1):
        old = stored.get(chunk.chunk_id)

        if old and old["content"] == chunk.content:
            vector = old["embedding"]
        else:
            vector = embed_text(chunk.content, client=client)
            print(f"Embedded {index}/{len(chunks)}: {chunk.chunk_id}")

        records.append({
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
        })

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = INDEX_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(records, indent=2), encoding="utf-8")
    os.replace(temporary, INDEX_FILE)

    print(f"Saved {len(records)} embeddings to {INDEX_FILE}")

if __name__ == "__main__":
    main()
