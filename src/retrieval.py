
import json
import re
from collections import defaultdict
from pathlib import Path


STOP_WORDS = {
    "how", "do", "i", "a", "an", "the", "to",
    "in", "on", "for", "of", "and", "or",
    "can", "my", "is", "with", "troubleshoot",
    "diagnose", "failure", "failures", "step",
    "steps", "verify", "check", "what", "should",
    "through", "returning", "have", "we", "seen",
    "this", "before", "previous", "historical",
    "incident", "incidents", "investigate",
    "there", "any", "similar", "past",
}


def load_embedding_records(path: Path) -> list[dict]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sum(
        a * a for a in vector_a
    ) ** 0.5

    magnitude_b = sum(
        b * b for b in vector_b
    ) ** 0.5

    denominator = magnitude_a * magnitude_b

    if denominator == 0:
        return 0.0

    return dot_product / denominator


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords for retrieval ranking."""

    words = re.findall(
        r"[a-z0-9]+",
        text.lower(),
    )

    return {
        word
        for word in words
        if len(word) > 2
        and word not in STOP_WORDS
    }


def calculate_section_boost(
    question: str,
    section: str,
) -> float:
    """Boost sections matching the question's keywords."""

    question_words = extract_keywords(question)
    section_words = extract_keywords(section)

    matches = question_words.intersection(
        section_words
    )

    return min(len(matches) * 0.20, 0.40)


def is_historical_incident_question(question: str) -> bool:
    """Detect questions requesting previous incident evidence."""

    historical_patterns = [
        r"\binc\d+\b",
        r"\bprevious\b",
        r"\bhistorical\b",
        r"\bincident\b",
        r"\bincidents\b",
        r"\bseen\b.*\bbefore\b",
        r"\bsimilar\b.*\bissue\b",
        r"\bpast\b.*\bissue\b",
        r"\bhappened\b.*\bbefore\b",
    ]

    question_lower = question.lower()

    return any(
        re.search(pattern, question_lower)
        for pattern in historical_patterns
    )


def get_http_status_codes(text: str) -> set[str]:
    """Extract HTTP error codes such as 401, 429, and 504."""

    return set(
        re.findall(
            r"\b[45]\d{2}\b",
            text,
        )
    )


def get_document_id(record: dict) -> str:
    """Get a stable document grouping key."""

    return str(
        record.get("document_id")
        or record.get("title")
        or ""
    )


def incident_section_priority(section: str) -> int:
    """
    Prioritize useful incident evidence rather than
    selecting only high-similarity metadata sections.
    """

    section_lower = section.lower()

    priorities = [
        ("summary", 0),
        ("investigation", 1),
        ("root cause", 2),
        ("resolution", 3),
        ("lesson", 4),
        ("overview", 5),
    ]

    for keyword, priority in priorities:
        if keyword in section_lower:
            return priority

    return 6


def find_matching_incident(
    question: str,
    scored_records: list[dict],
) -> str | None:
    """
    Find a strongly matching historical incident.

    Only activates when:
    - The user asks about historical incidents.
    - An HTTP error code is mentioned.
    - An incident record matches that error code.
    - Other question keywords also match the incident.

    This avoids selecting an unrelated incident solely
    because it mentions the same HTTP status.
    """

    if not is_historical_incident_question(question):
        return None

    question_codes = get_http_status_codes(question)

    if not question_codes:
        return None

    question_keywords = extract_keywords(question)
    question_keywords -= question_codes

    documents = defaultdict(list)

    for record in scored_records:
        documents[get_document_id(record)].append(
            record
        )

    best_document_id = None
    best_score = 0.0

    for document_id, document_records in documents.items():

        title = str(
            document_records[0].get("title", "")
        )

        # Restrict grouping to recognizable incident records.
        if not re.search(
            r"\bINC[-_ ]?\d+\b",
            title,
            flags=re.IGNORECASE,
        ):
            continue

        document_text = "\n".join(
            " ".join(
                [
                    str(record.get("title", "")),
                    str(record.get("section", "")),
                    str(record.get("content", "")),
                ]
            )
            for record in document_records
        )

        document_codes = get_http_status_codes(
            document_text
        )

        matched_codes = (
            question_codes & document_codes
        )

        if not matched_codes:
            continue

        document_keywords = extract_keywords(
            document_text
        )

        keyword_matches = (
            question_keywords & document_keywords
        )

        # Require more evidence than just an HTTP status.
        if len(keyword_matches) < 2:
            continue

        score = (
            5.0 * len(matched_codes)
            + 2.0 * len(keyword_matches)
            + max(
                record["similarity_score"]
                for record in document_records
            )
        )

        if score > best_score:
            best_score = score
            best_document_id = document_id

    return best_document_id


def retrieve_top_k(
    query_embedding: list[float],
    records: list[dict],
    top_k: int = 5,
    query_text: str | None = None,
) -> list[dict]:
    """
    Retrieve the most relevant knowledge-base chunks.

    For historical incident questions, prioritize
    sections from the same matching incident.

    For other questions, use the existing similarity
    and section-keyword ranking.
    """

    if top_k <= 0:
        return []

    scored_records = []

    for record in records:

        similarity = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_record = {
            **record,
            "similarity_score": similarity,
        }

        if query_text:
            boost = calculate_section_boost(
                query_text,
                record.get("section", ""),
            )

            scored_record["ranking_score"] = (
                similarity + boost
            )

        scored_records.append(scored_record)

    sort_field = (
        "ranking_score"
        if query_text
        else "similarity_score"
    )

    scored_records.sort(
        key=lambda item: item[sort_field],
        reverse=True,
    )

    if not query_text:
        return scored_records[:top_k]

    matching_incident_id = find_matching_incident(
        query_text,
        scored_records,
    )

    if not matching_incident_id:
        return scored_records[:top_k]

    incident_records = [
        record
        for record in scored_records
        if get_document_id(record) == matching_incident_id
    ]

    incident_records.sort(
        key=lambda record: (
            incident_section_priority(
                record.get("section", "")
            ),
            -record["similarity_score"],
        )
    )

    selected = incident_records[:top_k]

    # Fill remaining slots with normally ranked chunks.
    if len(selected) < top_k:
        for record in scored_records:
            if len(selected) >= top_k:
                break

            if get_document_id(record) != matching_incident_id:
                selected.append(record)

    return selected[:top_k]
