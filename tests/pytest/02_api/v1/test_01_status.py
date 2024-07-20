from time import sleep
from fastapi.testclient import TestClient
from src.api.main import api
from tests.fixtures.support import db_single_job
from tests.fixtures.fixtures_jobs import worker_info_job


async def test_one_job_status(worker_info_job):
    id = await db_single_job()
    keep_looping = True
    while keep_looping:
        sleep(1)
        print("** Sleep 1 for local queue performance\n")
        try:
            await worker_info_job(id)
            keep_looping = False
        except KeyError:
            pass
    with TestClient(api) as client:
        response = client.get(f"/api/v1/status/{id}")
    assert response.status_code == 200
    assert response.json()["job_id"] == id


async def test_all_jobs_status():
    id = await db_single_job()
    with TestClient(api) as client:
        response = client.get("/api/v1/status", timeout=10)
    assert response.status_code == 200
    items = [item for item in response.json() if item["job_id"] == id]
    assert len(items) == 1
