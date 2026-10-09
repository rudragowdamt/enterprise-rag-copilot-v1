
import pytest

from src.input_guardrails import validate_question


def test_valid_question():
    assert validate_question("  How do I fix a Boomi SFTP timeout?  ") == (
        "How do I fix a Boomi SFTP timeout?"
    )


@pytest.mark.parametrize("question", ["", "   ", "\n\t"])
def test_empty_question_rejected(question):
    with pytest.raises(ValueError, match="Question cannot be empty"):
        validate_question(question)


def test_question_at_maximum_length():
    assert len(validate_question("A" * 500)) == 500


def test_oversized_question_rejected():
    with pytest.raises(ValueError, match="cannot exceed 500"):
        validate_question("A" * 501)


@pytest.mark.parametrize("question", [None, 123, ["question"]])
def test_non_string_question_rejected(question):
    with pytest.raises(ValueError, match="must be a string"):
        validate_question(question)


def test_null_character_rejected():
    with pytest.raises(ValueError, match="invalid null character"):
        validate_question("Hello" + chr(0))
