from uuid import uuid4
from fastapi.testclient import TestClient
from src.api.main import api


id = str(uuid4())


async def test_post_jobs_bad():
    kwargs = {"key1": "fail"}
    job_data = {"id": id, "function": "hello_job", "input_params": kwargs}
    with TestClient(api) as client:
        response = client.post(
            "/api/v1/jobs",
            json=job_data,
        )
    assert response.status_code == 202
