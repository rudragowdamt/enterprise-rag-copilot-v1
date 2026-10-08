import json

import boto3


DEFAULT_REGION = "ap-south-1"
DEFAULT_MODEL_ID = "amazon.titan-embed-text-v2:0"
DEFAULT_DIMENSIONS = 1024


def create_bedrock_client(region: str = DEFAULT_REGION):
    return boto3.client(
        "bedrock-runtime",
        region_name=region,
    )


def embed_text(
    text: str,
    client=None,
    model_id: str = DEFAULT_MODEL_ID,
    dimensions: int = DEFAULT_DIMENSIONS,
) -> list[float]:

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    if client is None:
        client = create_bedrock_client()

    request_body = {
        "inputText": text,
        "dimensions": dimensions,
        "normalize": True,
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body),
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]