
import os
import boto3


GROUNDING_FAILURE_MESSAGE = (
    "The generated answer could not be verified "
    "against the retrieved knowledge."
)


def validate_grounding(
    question: str,
    context: str,
    answer: str,
    client=None,
) -> bool:
    """Check whether the generated answer is grounded in the context."""

    guardrail_id = os.getenv("BEDROCK_GUARDRAIL_ID")

    if not guardrail_id:
        raise RuntimeError(
            "BEDROCK_GUARDRAIL_ID is required for grounding validation."
        )

    if client is None:
        client = boto3.client(
            "bedrock-runtime",
            region_name="ap-south-1",
        )

    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=os.getenv(
            "BEDROCK_GUARDRAIL_VERSION", "DRAFT"
        ),
        source="OUTPUT",
        content=[
            {
                "text": {
                    "text": context,
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

    if response.get("action") == "GUARDRAIL_INTERVENED":
        return False

    assessments = response.get("assessments", [])

    grounding_filters = [
        item
        for assessment in assessments
        for item in assessment.get(
            "contextualGroundingPolicy", {}
        ).get("filters", [])
    ]

    # Fail closed if grounding checks were not evaluated.
    required_types = {"GROUNDING", "RELEVANCE"}
    evaluated_types = {
        item.get("type") for item in grounding_filters
    }

    if not required_types.issubset(evaluated_types):
        return False

    return all(
        item.get("action") == "NONE"
        for item in grounding_filters
        if item.get("type") in required_types
    )
