import json

import boto3


REGION = "ap-south-1"
MODEL_ID = "amazon.titan-embed-text-v2:0"


bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
)

def embed_text(text: str) -> list[float]:
    request_body = {
        "inputText": text,
        "dimensions": 1024,
        "normalize": True,
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body),
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]
text = "Axway gateway returned HTTP 504 because the backend response was slow."

embedding = embed_text(text)

print("Text:", text)
print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sum(
        a * a
        for a in vector_a
    ) ** 0.5

    magnitude_b = sum(
        b * b
        for b in vector_b
    ) ** 0.5

    return dot_product / (
        magnitude_a * magnitude_b
    )
text_a = "Axway gateway returned HTTP 504 because the backend response was slow."

text_b = "The API gateway timed out while waiting for the backend service."

text_c = "The SFTP partner changed its SSH host key."


embedding_a = embed_text(text_a)
embedding_b = embed_text(text_b)
embedding_c = embed_text(text_c)


similarity_ab = cosine_similarity(
    embedding_a,
    embedding_b,
)

similarity_ac = cosine_similarity(
    embedding_a,
    embedding_c,
)


print("\nSEMANTIC SIMILARITY TEST")
print("-" * 60)

print("A:", text_a)
print("B:", text_b)
print("C:", text_c)

print()

print(
    "Similarity A ↔ B:",
    round(similarity_ab, 4),
)

print(
    "Similarity A ↔ C:",
    round(similarity_ac, 4),
)