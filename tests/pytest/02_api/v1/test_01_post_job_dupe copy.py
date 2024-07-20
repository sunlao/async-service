from uuid import uuid4
from fastapi.testclient import TestClient
from src.api.main import api

id = str(uuid4())


async def test_post_jobs():
    job_data = {"id": id, "function": "hello_job"}
    with TestClient(api) as client:
        response = client.post(
            "/api/v1/jobs",
            json=job_data,
        )
    assert response.status_code == 202


async def test_post_jobs_dupe():
    job_data = {"id": id, "function": "hello_job"}
    with TestClient(api) as client:
        response = client.post(
            "/api/v1/jobs",
            json=job_data,
        )
    assert response.status_code == 409
