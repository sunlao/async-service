from fastapi.testclient import TestClient
from src.api.main import api


def test_api_info():
    with TestClient(api) as client:
        response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.json()["DB_HealthCheck"] == "Connected"
