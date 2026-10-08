import pytest

from src.rag_pipeline import ask_rag


def test_ask_rag_rejects_empty_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        ask_rag("")