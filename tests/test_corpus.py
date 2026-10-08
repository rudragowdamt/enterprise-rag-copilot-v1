from pathlib import Path

from src.documents import load_corpus


KNOWLEDGE_ROOT = Path("data/knowledge")

EXPECTED_DOC_TYPES = {
    "runbook",
    "incident",
    "policy",
    "procedure",
    "architecture",
}


def test_corpus_document_count():
    docs = load_corpus(KNOWLEDGE_ROOT)

    assert len(docs) == 24


def test_corpus_document_types():
    docs = load_corpus(KNOWLEDGE_ROOT)

    actual_types = {doc.doc_type for doc in docs}

    assert actual_types == EXPECTED_DOC_TYPES


def test_all_documents_have_titles():
    docs = load_corpus(KNOWLEDGE_ROOT)

    assert all(doc.title.strip() for doc in docs)


def test_all_documents_have_content():
    docs = load_corpus(KNOWLEDGE_ROOT)

    assert all(doc.content.strip() for doc in docs)


def test_all_documents_have_document_ids():
    docs = load_corpus(KNOWLEDGE_ROOT)

    assert all(doc.document_id.strip() for doc in docs)


def test_document_ids_are_unique():
    docs = load_corpus(KNOWLEDGE_ROOT)

    document_ids = [doc.document_id for doc in docs]

    assert len(document_ids) == len(set(document_ids))


def test_expected_platform_documents_exist():
    docs = load_corpus(KNOWLEDGE_ROOT)

    combined_text = " ".join(
        f"{doc.title} {doc.system} {doc.content}"
        for doc in docs
    ).lower()

    assert "boomi" in combined_text
    assert "axway" in combined_text
    assert "layer7" in combined_text
    assert "sftp" in combined_text