import pytest

from src.embeddings import embed_text


def test_embed_text_rejects_empty_text():
    with pytest.raises(ValueError, match="Text cannot be empty"):
        embed_text("")