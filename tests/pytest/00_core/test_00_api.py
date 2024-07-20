from fastapi.testclient import TestClient
from src.api.main import api


def test_api_hello_world():
    with TestClient(api) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Heath check good!"}
