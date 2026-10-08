import pytest
from src.generation import build_prompt

def test_build_prompt_contains_grounding_rules():
    prompt = build_prompt(
        "Why is Axway returning 504?",
        "[SOURCE 1]\nBackend response was slow.",
    )

    assert "ONLY the supplied context" in prompt
    assert "Do not invent information" in prompt
    assert "[SOURCE 1]" in prompt
    assert "Why is Axway returning 504?" in prompt

from src.generation import generate_answer


def test_generate_answer_rejects_empty_prompt():
    with pytest.raises(
        ValueError,
        match="Prompt cannot be empty",
    ):
        generate_answer("")
from src.generation import build_context


def test_build_context_includes_source_metadata():
    results = [
        {
            "title": "Axway 504 Runbook",
            "section": "Troubleshooting",
            "document_id": "RB-AXWAY-001",
            "content": "Check backend connectivity.",
        }
    ]

    context = build_context(results)

    assert "[SOURCE 1]" in context
    assert "Axway 504 Runbook" in context
    assert "Troubleshooting" in context
    assert "RB-AXWAY-001" in context
    assert "Check backend connectivity." in context