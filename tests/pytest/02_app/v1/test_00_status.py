from fastapi.testclient import TestClient
from src.api.main import api


def test_api_info():
    with TestClient(api) as client:
        response = client.get("/app/v1/status")
    assert response.status_code == 200
