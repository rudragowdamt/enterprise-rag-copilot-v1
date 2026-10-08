from pathlib import Path

from src.documents import load_document, load_corpus
from src.chunking import chunk_document, chunk_corpus


KNOWLEDGE_ROOT = Path("data/knowledge")

INC003_PATH = Path(
    "data/knowledge/incidents/INC003_axway_payment_504.md"
)


def test_inc003_creates_expected_chunks():
    document = load_document(INC003_PATH)

    chunks = chunk_document(document)

    assert len(chunks) == 6


def test_inc003_expected_sections():
    document = load_document(INC003_PATH)

    chunks = chunk_document(document)

    sections = [chunk.section for chunk in chunks]

    assert sections == [
        "Overview",
        "Summary",
        "Investigation",
        "Root Cause",
        "Resolution",
        "Lesson",
    ]


def test_chunks_preserve_document_metadata():
    document = load_document(INC003_PATH)

    chunks = chunk_document(document)

    assert all(
        chunk.document_id == document.document_id
        for chunk in chunks
    )

    assert all(
        chunk.doc_type == document.doc_type
        for chunk in chunks
    )

    assert all(
        chunk.system == document.system
        for chunk in chunks
    )


def test_chunks_have_unique_ids():
    documents = load_corpus(KNOWLEDGE_ROOT)

    chunks = chunk_corpus(documents)

    chunk_ids = [chunk.chunk_id for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_chunks_have_content():
    documents = load_corpus(KNOWLEDGE_ROOT)

    chunks = chunk_corpus(documents)

    assert all(
        chunk.content.strip()
        for chunk in chunks
    )


def test_root_cause_chunk_contains_expected_evidence():
    document = load_document(INC003_PATH)

    chunks = chunk_document(document)

    root_cause = next(
        chunk
        for chunk in chunks
        if chunk.section == "Root Cause"
    )

    assert "database" in root_cause.content.lower()

    assert "gateway timeout" in root_cause.content.lower()