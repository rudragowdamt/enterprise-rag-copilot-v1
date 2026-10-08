import hashlib
import re


def normalize_question(question: str) -> str:
    """
    Normalize a user question so minor differences in
    capitalization and whitespace use the same cache entry.
    """

    normalized = question.strip().lower()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized


def create_cache_key(question: str) -> str:
    """
    Create a stable SHA-256 cache key from the
    normalized question.
    """

    normalized = normalize_question(
        question
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()
import json
from pathlib import Path


DEFAULT_CACHE_DIR = Path("data/cache")


def get_cached_result(
    question: str,
    cache_dir: Path = DEFAULT_CACHE_DIR,
):
    cache_key = create_cache_key(question)

    cache_file = cache_dir / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    return json.loads(
        cache_file.read_text(
            encoding="utf-8"
        )
    )


def save_cached_result(
    question: str,
    result: dict,
    cache_dir: Path = DEFAULT_CACHE_DIR,
):
    cache_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    cache_key = create_cache_key(question)

    cache_file = cache_dir / f"{cache_key}.json"

    cache_file.write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )