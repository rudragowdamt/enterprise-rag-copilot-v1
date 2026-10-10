
import hashlib
import json
import re
from pathlib import Path


DEFAULT_CACHE_DIR = Path("data/cache")
DEFAULT_EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)

CACHE_SCHEMA_VERSION = "v3"


def normalize_question(question: str) -> str:
    normalized = question.strip().lower()
    return re.sub(r"\s+", " ", normalized)


def get_knowledge_version(
    embedding_file: Path = DEFAULT_EMBEDDING_FILE,
) -> str:
    """Generate a version based on knowledge-base content."""

    if not embedding_file.exists():
        return "missing"

    file_hash = hashlib.sha256()

    with embedding_file.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            file_hash.update(chunk)

    return file_hash.hexdigest()[:16]


def create_cache_key(question: str) -> str:
    """Preserve the existing normalized-question key."""

    normalized = normalize_question(question)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def get_versioned_cache_dir(
    cache_dir: Path = DEFAULT_CACHE_DIR,
    embedding_file: Path = DEFAULT_EMBEDDING_FILE,
) -> Path:
    version = get_knowledge_version(embedding_file)

    return cache_dir / CACHE_SCHEMA_VERSION / version


def get_cached_result(
    question: str,
    cache_dir: Path = DEFAULT_CACHE_DIR,
):
    cache_key = create_cache_key(question)

    versioned_dir = get_versioned_cache_dir(cache_dir)
    cache_file = versioned_dir / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    return json.loads(
        cache_file.read_text(encoding="utf-8")
    )


def save_cached_result(
    question: str,
    result: dict,
    cache_dir: Path = DEFAULT_CACHE_DIR,
):
    versioned_dir = get_versioned_cache_dir(cache_dir)

    versioned_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    cache_key = create_cache_key(question)
    cache_file = versioned_dir / f"{cache_key}.json"

    cache_file.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
