from src.cache import (
    normalize_question,
    create_cache_key,
)


def test_normalize_question():
    q1 = "PaymentService through Axway"
    q2 = "  paymentservice   through AXWAY  "

    assert normalize_question(q1) == normalize_question(q2)


def test_same_question_creates_same_cache_key():
    q1 = "PaymentService through Axway"
    q2 = "  paymentservice   through AXWAY  "

    assert create_cache_key(q1) == create_cache_key(q2)


def test_cache_hit_bypasses_aws(monkeypatch):
    import src.rag_pipeline as pipeline

    cached_result = {
        "question": "cached question",
        "answer": "Cached answer",
        "sources": [],
        "cache_hit": False,
    }

    monkeypatch.setattr(
        pipeline,
        "get_cached_result",
        lambda question: cached_result.copy(),
    )

    def aws_must_not_be_called(*args, **kwargs):
        raise AssertionError(
            "AWS was called during a cache hit."
        )

    monkeypatch.setattr(
        pipeline,
        "embed_text",
        aws_must_not_be_called,
    )

    monkeypatch.setattr(
        pipeline,
        "generate_answer",
        aws_must_not_be_called,
    )

    result = pipeline.ask_rag(
        "cached question"
    )

    assert result["cache_hit"] is True
    assert result["answer"] == "Cached answer"