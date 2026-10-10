
import time
from pathlib import Path

from src.app_logging import get_logger
from src.citation_validator import validate_citations
from src.contextual_grounding import (
    validate_grounding,
    GROUNDING_FAILURE_MESSAGE,
)
from src.document_access import filter_authorized_records
from src.input_guardrails import validate_question
from src.embeddings import embed_text

from src.retrieval import (
    load_embedding_records,
    retrieve_top_k,
)

from src.retrieval_confidence import (
    has_sufficient_evidence,
    INSUFFICIENT_EVIDENCE_MESSAGE,
)

from src.generation import (
    build_context,
    build_prompt,
    generate_answer,
    GUARDRAIL_BLOCKED_MESSAGE,
)

from src.cache import (
    get_cached_result,
    save_cached_result,
)


DEFAULT_EMBEDDING_FILE = Path(
    "data/embeddings/chunk_embeddings.json"
)

CITATION_FAILURE_MESSAGE = (
    "The generated answer could not be verified "
    "against the retrieved sources."
)

ACCESS_DENIED_MESSAGE = (
    "No knowledge documents are available "
    "for your authorized systems."
)

logger = get_logger(__name__)


def ask_rag(
    question: str,
    top_k: int = 5,
    embedding_file: Path = DEFAULT_EMBEDDING_FILE,
    allowed_systems: list[str] | None = None,
) -> dict:

    start = time.perf_counter()

    try:
        # Step 1: Validate question.
        question = validate_question(question)

        access_scoped = allowed_systems is not None

        # Step 2: Check cache.
        # Scoped requests cannot reuse the shared cache.
        if not access_scoped:
            cached_result = get_cached_result(question)

            if (
                cached_result is not None
                and cached_result.get("answer") not in (
                    GUARDRAIL_BLOCKED_MESSAGE,
                    CITATION_FAILURE_MESSAGE,
                    GROUNDING_FAILURE_MESSAGE,
                )
            ):
                logger.info(
                    "rag_complete status=cache_hit elapsed_ms=%.0f",
                    (time.perf_counter() - start) * 1000,
                )

                return {
                    **cached_result,
                    "cache_hit": True,
                }

        # Step 3: Load knowledge base.
        records = load_embedding_records(
            embedding_file
        )

        # Step 4: Apply document access filtering.
        if access_scoped:
            records = filter_authorized_records(
                records,
                allowed_systems,
            )

            logger.info(
                "rag_access_filter authorized_records=%d",
                len(records),
            )

            if not records:
                logger.info(
                    "rag_complete status=no_authorized_documents "
                    "elapsed_ms=%.0f",
                    (time.perf_counter() - start) * 1000,
                )

                return {
                    "question": question,
                    "answer": ACCESS_DENIED_MESSAGE,
                    "sources": [],
                    "cache_hit": False,
                }

        # Step 5: Generate question embedding.
        query_embedding = embed_text(question)

        # Step 6: Retrieve matching documents.
        results = retrieve_top_k(
            query_embedding,
            records,
            top_k=top_k,
            query_text=question,
        )

        # Step 7: Check retrieval confidence.
        if not has_sufficient_evidence(results):
            logger.info(
                "rag_complete status=insufficient_evidence "
                "source_count=%d elapsed_ms=%.0f",
                len(results),
                (time.perf_counter() - start) * 1000,
            )

            return {
                "question": question,
                "answer": INSUFFICIENT_EVIDENCE_MESSAGE,
                "sources": [],
                "cache_hit": False,
            }

        # Step 8: Build retrieved context.
        context = build_context(results)

        # Step 9: Build prompt.
        prompt = build_prompt(
            question,
            context,
        )

        # Step 10: Generate answer using Bedrock Guardrails.
        answer = generate_answer(prompt)

        # Step 11: Verify security, citations and grounding.
        if answer == GUARDRAIL_BLOCKED_MESSAGE:
            status = "guardrail_blocked"

        elif not validate_citations(
            answer,
            len(results),
        ):
            answer = CITATION_FAILURE_MESSAGE
            status = "citation_failed"

        elif not validate_grounding(
            question=question,
            context=context,
            answer=answer,
        ):
            answer = GROUNDING_FAILURE_MESSAGE
            status = "grounding_failed"

        else:
            status = "success"

        # Step 12: Remove embedding vectors.
        clean_sources = [
            {
                key: value
                for key, value in source.items()
                if key != "embedding"
            }
            for source in results
        ]

        # Step 13: Prepare response.
        result = {
            "question": question,
            "answer": answer,
            "sources": clean_sources,
            "cache_hit": False,
        }

        # Step 14: Cache only successful unscoped answers.
        if status == "success" and not access_scoped:
            save_cached_result(
                question,
                result,
            )

        # Step 15: Log result without sensitive content.
        logger.info(
            "rag_complete status=%s "
            "source_count=%d elapsed_ms=%.0f",
            status,
            len(results),
            (time.perf_counter() - start) * 1000,
        )

        return result

    except Exception:
        logger.error(
            "rag_failed stage=pipeline elapsed_ms=%.0f",
            (time.perf_counter() - start) * 1000,
        )
        raise
