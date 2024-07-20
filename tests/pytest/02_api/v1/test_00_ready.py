from fastapi.testclient import TestClient
from src.api.main import api


def test_api_info():
    with TestClient(api) as client:
        response = client.get("/api/v1/ready")
    assert response.status_code == 200
    json_dict = response.json()
    assert json_dict["DB_Check"] == "ready"
    assert json_dict["Queue_Check"] == "ready"
