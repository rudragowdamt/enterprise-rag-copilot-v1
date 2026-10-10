
import json
import re
from pathlib import Path

from src.rag_pipeline import ask_rag


CACHE_DIRECTORY = Path("data/cache")
OUTPUT_DIRECTORY = Path("data/demo_cache")
OUTPUT_FILE = OUTPUT_DIRECTORY / "demo_answers.json"

# Maximum number of new RAG questions to run in this batch.
MAX_NEW_AWS_QUESTIONS = 9


# Six questions already present in the V2 cache.
EXISTING_QUESTIONS = [
    (
        "Axway HTTP 504",
        "PaymentService through Axway is returning HTTP 504. "
        "What should I investigate and have we seen this before?",
    ),
    (
        "Expired OAuth Token",
        "What steps should I follow to troubleshoot an expired "
        "OAuth token in an API integration?",
    ),
    (
        "Boomi SFTP Timeout",
        "Our Boomi SFTP integration is timing out when connecting "
        "to the server on port 22. What should we check?",
    ),
    (
        "API Gateway Timeout",
        "What should the support team verify when a production "
        "API starts returning repeated gateway timeout errors?",
    ),
    (
        "Boomi Deployment Failure",
        "A Boomi production process started failing immediately "
        "after deployment. What should support check?",
    ),
    (
        "TIBCO JMS Connection Failure",
        "Our TIBCO BusinessWorks application cannot connect to "
        "the JMS broker. What are the possible causes and "
        "troubleshooting steps?",
    ),
]


# Nine proposed additional scenarios.
NEW_QUESTIONS = [
    (
        "INC001 Boomi Root Cause",
        "What caused incident INC001, and how was the Boomi "
        "production failure resolved?",
    ),
    (
        "INC002 Layer7 Certificate Expiry",
        "How should support investigate incident INC002 "
        "involving a Layer7 certificate expiry?",
    ),
    (
        "INC004 Database Connection",
        "What caused incident INC004, and what database checks "
        "should support perform?",
    ),
    (
        "INC005 Partner SFTP Failure",
        "How should support investigate incident INC005 "
        "involving a partner SFTP failure?",
    ),
    (
        "Boomi Atom Unavailable",
        "What checks should be performed when a Boomi Atom "
        "becomes unavailable?",
    ),
    (
        "Layer7 Policy Failure",
        "How should support investigate a Layer7 API Gateway "
        "policy failure?",
    ),
    (
        "Production Deployment Checks",
        "What should support verify before and after a "
        "production deployment?",
    ),
    (
        "P1 Incident Escalation",
        "What is the recommended P1 incident escalation process?",
    ),
    (
        "Middleware Disaster Recovery",
        "What checks are required during middleware "
        "disaster recovery?",
    ),
]


BLOCKED_PHRASES = [
    "violates the assistant's security policy",
    "could not be verified against the retrieved knowledge",
    "could not find sufficiently relevant information",
    "no answer returned",
]


def valid_answer(result):
    """Perform basic quality checks before exporting."""

    if not isinstance(result, dict):
        return False

    answer = str(result.get("answer") or "").strip()
    sources = result.get("sources") or []

    if not answer or not isinstance(sources, list):
        return False

    if not sources:
        return False

    if any(
        phrase in answer.lower()
        for phrase in BLOCKED_PHRASES
    ):
        return False

    # Support both [SOURCE 1] and [SOURCE 1, SOURCE 2].
    citations = [
        int(number)
        for number in re.findall(
            r"SOURCE\s+(\d+)",
            answer,
            flags=re.IGNORECASE,
        )
    ]

    if not citations:
        return False

    if any(
        number < 1 or number > len(sources)
        for number in citations
    ):
        return False

    return True


def normalize_result(label, question, result):
    """Export only the fields needed by the demo."""

    clean_sources = []

    for source in result.get("sources", []):
        clean_sources.append({
            "title": source.get("title", ""),
            "section": source.get("section", ""),
            "document_id": source.get("document_id", ""),
            "chunk_id": source.get("chunk_id", ""),
            "source": source.get("source", ""),
            "content": source.get("content", ""),
            "similarity_score": source.get(
                "similarity_score", 0
            ),
        })

    return {
        "label": label,
        "question": question,
        "answer": result["answer"],
        "sources": clean_sources,
        "mode": "pre_generated_rag",
    }


def load_existing_cached_answers():
    """Read existing cache files without using AWS."""

    cache = {}

    if not CACHE_DIRECTORY.exists():
        return cache

    for path in CACHE_DIRECTORY.rglob("*.json"):
        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )

            if not valid_answer(data):
                continue

            question = data.get("question", "").strip()

            if question:
                cache.setdefault(question, data)

        except (
            OSError,
            ValueError,
            TypeError,
        ):
            continue

    return cache


def load_existing_export():
    """Permit safe reruns without generating saved questions."""

    if not OUTPUT_FILE.exists():
        return {}

    try:
        data = json.loads(
            OUTPUT_FILE.read_text(encoding="utf-8")
        )

        return {
            item["question"]: item
            for item in data.get("questions", [])
            if isinstance(item, dict)
            and valid_answer(item)
            and item.get("question")
        }

    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
    ):
        return {}


def save_export(results):
    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "title": "Enterprise Integration RAG Copilot",
        "description": (
            "Previously generated RAG answers using "
            "synthetic enterprise integration knowledge."
        ),
        "demo_mode": "cache_only",
        "questions": results,
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def main():

    existing_cache = load_existing_cached_answers()
    previous_export = load_existing_export()

    results = []
    new_aws_calls = 0

    print("\nENTERPRISE RAG DEMO CACHE GENERATOR")
    print("=" * 55)

    print("\nReusing existing cached answers...\n")

    for label, question in EXISTING_QUESTIONS:

        result = (
            previous_export.get(question)
            or existing_cache.get(question)
        )

        if result and valid_answer(result):

            results.append(
                normalize_result(label, question, result)
            )

            print("[REUSED]", label)

        else:
            print("[MISSING]", label)

    print("\nGenerating additional questions...\n")

    for label, question in NEW_QUESTIONS:

        result = (
            previous_export.get(question)
            or existing_cache.get(question)
        )

        if result and valid_answer(result):

            print("[REUSED]", label)

        else:

            if new_aws_calls >= MAX_NEW_AWS_QUESTIONS:
                print("[SKIPPED: CALL LIMIT]", label)
                continue

            print("[GENERATING]", label, flush=True)

            # This is the only place where new AWS requests
            # may be triggered by this script.
            new_aws_calls += 1

            try:
                result = ask_rag(question)

            except Exception as error:
                print(
                    "[ERROR]",
                    label,
                    type(error).__name__,
                )
                continue

        if valid_answer(result):

            results.append(
                normalize_result(label, question, result)
            )

            print("[SAVED]", label)

        else:
            print(
                "[REJECTED: REVIEW REQUIRED]",
                label,
            )

        # Preserve progress if the script is interrupted.
        save_export(results)

    save_export(results)

    print("\n" + "=" * 55)
    print("RESULT")
    print("=" * 55)

    print("Saved questions:", len(results))
    print("New RAG calls attempted:", new_aws_calls)
    print("Output:", OUTPUT_FILE)

    print(
        "\nIMPORTANT: Review generated answers against "
        "their cited documents before publishing."
    )


if __name__ == "__main__":
    main()
