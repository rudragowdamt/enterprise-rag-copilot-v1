import boto3


DEFAULT_REGION = "ap-south-1"

DEFAULT_GENERATION_MODEL_ID = (
    "in.anthropic.claude-haiku-4-5-20251001-v1:0"
)


def create_bedrock_client(
    region: str = DEFAULT_REGION,
):
    return boto3.client(
        "bedrock-runtime",
        region_name=region,
    )
def build_context(
    retrieved_results: list[dict],
) -> str:

    context_parts = []

    for index, result in enumerate(
        retrieved_results,
        start=1,
    ):
        context_parts.append(
            f"[SOURCE {index}]\n"
            f"Title: {result['title']}\n"
            f"Section: {result['section']}\n"
            f"Document ID: {result['document_id']}\n"
            f"Content:\n{result['content']}"
        )

    return "\n\n".join(context_parts)
def build_prompt(
    question: str,
    context: str,
) -> str:

    return f"""
You are an Enterprise Integration Support Copilot.

Answer the user's question using ONLY the supplied context.

Rules:
1. Do not invent information.
2. If the context does not contain enough information, say so.
3. Provide practical troubleshooting steps when available.
4. Mention relevant historical incidents when available.
5. Cite sources using [SOURCE 1], [SOURCE 2], etc.
6. Keep the answer concise and operationally useful.

USER QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
""".strip()
def generate_answer(
    prompt: str,
    client=None,
    model_id: str = DEFAULT_GENERATION_MODEL_ID,
) -> str:

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    if client is None:
        client = create_bedrock_client()

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": 800,
            "temperature": 0.1,
        },
    )

    return (
        response["output"]["message"]["content"][0]["text"]
    )