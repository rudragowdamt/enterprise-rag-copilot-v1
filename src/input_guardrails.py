
MAX_QUESTION_LENGTH = 500


def validate_question(question: str) -> str:
    """Validate user input before sending it to the RAG pipeline."""

    if not isinstance(question, str):
        raise ValueError("Question must be a string.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError(
            f"Question cannot exceed {MAX_QUESTION_LENGTH} characters."
        )

    if "\x00" in question:
        raise ValueError("Question contains an invalid null character.")

    return question
