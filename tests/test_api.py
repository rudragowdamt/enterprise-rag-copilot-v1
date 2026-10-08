from fastapi.testclient import TestClient

from src.api import app
import src.api as api_module


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }
def test_ask_endpoint(monkeypatch):
    def fake_ask_rag(question):
        return {
            "question": question,
            "answer": "Check the Axway backend.",
            "sources": [
                {
                    "chunk_id": "RB-AXWAY-001-003",
                    "document_id": "RB-AXWAY-001",
                    "title": "Axway 504 Runbook",
                    "section": "Troubleshooting",
                    "source": "runbooks/axway_gateway_504.md",
                    "similarity_score": 0.90,
                }
            ],
        }

    monkeypatch.setattr(
        api_module,
        "ask_rag",
        fake_ask_rag,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Why is Axway returning 504?"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["question"] == (
        "Why is Axway returning 504?"
    )
    assert body["answer"] == (
        "Check the Axway backend."
    )
    assert len(body["sources"]) == 1
    assert "embedding" not in body["sources"][0]