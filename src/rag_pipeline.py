
import time
from pathlib import Path

from src.app_logging import get_logger
from src.citation_validator import validate_citations
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

logger = get_logger(__name__)


def ask_rag(
    question: str,
    top_k: int = 5,
    embedding_file: Path = DEFAULT_EMBEDDING_FILE,
) -> dict:

    start = time.perf_counter()

    try:
        # Step 1: Validate question.
        question = validate_question(question)

        # Step 2: Check cache.
        cached_result = get_cached_result(question)

        if (
            cached_result is not None
            and cached_result.get("answer") not in (
                GUARDRAIL_BLOCKED_MESSAGE,
                CITATION_FAILURE_MESSAGE,
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

        # Step 4: Generate question embedding.
        query_embedding = embed_text(
            question
        )

        # Step 5: Retrieve documents.
        results = retrieve_top_k(
            query_embedding,
            records,
            top_k=top_k,
        )

        # Step 6: Check retrieval confidence.
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

        # Step 7: Build RAG context.
        context = build_context(results)

        # Step 8: Build prompt.
        prompt = build_prompt(
            question,
            context,
        )

        # Step 9: Generate answer with Bedrock.
        answer = generate_answer(prompt)

        # Step 10: Check security and citations.
        if answer == GUARDRAIL_BLOCKED_MESSAGE:

            status = "guardrail_blocked"

        elif not validate_citations(
            answer,
            len(results),
        ):

            answer = CITATION_FAILURE_MESSAGE
            status = "citation_failed"

        else:
            status = "success"

        # Step 11: Remove embedding vectors.
        clean_sources = [
            {
                key: value
                for key, value in source.items()
                if key != "embedding"
            }
            for source in results
        ]

        # Step 12: Prepare response.
        result = {
            "question": question,
            "answer": answer,
            "sources": clean_sources,
            "cache_hit": False,
        }

        # Step 13: Cache only successful answers.
        if status == "success":
            save_cached_result(
                question,
                result,
            )

        # Step 14: Log execution status.
        logger.info(
            "rag_complete status=%s "
            "source_count=%d elapsed_ms=%.0f",
            status,
            len(results),
            (time.perf_counter() - start) * 1000,
        )

        return result

    except Exception:

        # Do not log questions, secrets or document content.
        logger.error(
            "rag_failed stage=pipeline elapsed_ms=%.0f",
            (time.perf_counter() - start) * 1000,
        )

        raise
