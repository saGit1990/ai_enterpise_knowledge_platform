from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_document():
    response = client.post(
        "/api/v1/documents",
        json={
            "filename": "policy.pdf",
            "file_type": "pdf",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "policy.pdf"
    assert data["file_type"] == "pdf"
    assert data["status"] == "uploaded"
    assert "id" in data
    assert "created_at" in data