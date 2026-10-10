
import os
import re
import logging

import boto3


logger = logging.getLogger(__name__)

GROUNDING_FAILURE_MESSAGE = (
    "The generated answer could not be verified "
    "against the retrieved knowledge."
)


def clean_grounding_context(context: str) -> str:
    """
    Remove document metadata while preserving the evidence text.

    Diagnostic experiment:
    Determine whether metadata affects Bedrock grounding scores.
    """

    cleaned_context = re.sub(
        r"(?m)^(?:"
        r"\[SOURCE \d+\]|"
        r"Title:.*|"
        r"Section:.*|"
        r"Document ID:.*|"
        r"Content:"
        r")\s*$",
        "",
        context,
    )

    return cleaned_context.strip()


def validate_grounding(
    question: str,
    context: str,
    answer: str,
    client=None,
) -> bool:
    """
    Validate an answer against retrieved knowledge
    using AWS Bedrock Guardrails.
    """

    guardrail_id = os.getenv("BEDROCK_GUARDRAIL_ID")

    if not guardrail_id:
        raise RuntimeError(
            "BEDROCK_GUARDRAIL_ID is required for grounding validation."
        )

    if client is None:
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv(
                "BEDROCK_REGION", "ap-south-1"
            ),
        )

    # Diagnostic: remove document metadata and section labels.
    # All retrieved evidence remains available to the validator.
    cleaned_context = clean_grounding_context(context)

    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=os.getenv(
            "BEDROCK_GUARDRAIL_VERSION", "DRAFT"
        ),
        source="OUTPUT",
        content=[
            {
                "text": {
                    "text": cleaned_context,
                    "qualifiers": ["grounding_source"],
                }
            },
            {
                "text": {
                    "text": question,
                    "qualifiers": ["query"],
                }
            },
            {
                "text": {
                    "text": answer,
                    "qualifiers": ["guard_content"],
                }
            },
        ],
    )

    action = response.get("action")
    assessments = response.get("assessments", [])

    grounding_filters = [
        item
        for assessment in assessments
        for item in assessment.get(
            "contextualGroundingPolicy", {}
        ).get("filters", [])
    ]

    # Log diagnostic scores without logging document contents,
    # user questions, generated answers, or credentials.
    logger.warning(
        "grounding_diagnostic action=%s filters=%s",
        action,
        [
            {
                "type": item.get("type"),
                "score": item.get("score"),
                "threshold": item.get("threshold"),
                "action": item.get("action"),
            }
            for item in grounding_filters
        ],
    )

    # Reject any response blocked by Bedrock Guardrails.
    if action == "GUARDRAIL_INTERVENED":
        logger.warning(
            "grounding_rejected reason=guardrail_intervened"
        )
        return False

    required_types = {"GROUNDING", "RELEVANCE"}

    evaluated_types = {
        item.get("type")
        for item in grounding_filters
    }

    # Fail closed if required assessments are missing.
    if not required_types.issubset(evaluated_types):
        logger.warning(
            "grounding_rejected reason=missing_assessments"
        )
        return False

    failed_filters = [
        item
        for item in grounding_filters
        if item.get("type") in required_types
        and item.get("action") != "NONE"
    ]

    if failed_filters:
        logger.warning(
            "grounding_rejected reason=failed_filters types=%s",
            [item.get("type") for item in failed_filters],
        )
        return False

    logger.info("grounding_validation_passed")
    return True
