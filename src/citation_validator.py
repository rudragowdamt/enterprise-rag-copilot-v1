import re


def validate_citations(answer: str, source_count: int) -> bool:
    """Check that citations reference available sources."""

    citations = re.findall(
        r"\[SOURCE\s+(\d+)\]",
        answer,
        flags=re.IGNORECASE,
    )

    if not citations:
        return False

    return all(
        1 <= int(number) <= source_count
        for number in citations
    )
