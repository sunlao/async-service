from time import sleep
from uuid import uuid4
from fastapi.testclient import TestClient
from src.helpers.db.models import DatabaseUserContext
from src.api.main import api
from tests.fixtures.fixtures_queue import queue_keys
from tests.fixtures.fixtures_db import db_get_one
from tests.fixtures.fixtures_jobs import worker_info_job


id = str(uuid4())


async def test_post_jobs(worker_info_job):
    job_data = {"id": id, "function": "hello_job"}
    with TestClient(api) as client:
        response = client.post(
            "/api/v1/jobs",
            json=job_data,
        )
    assert response.status_code == 202
    assert response.json()["job_id"] == id
    keep_looping = True
    while keep_looping:
        sleep(1)
        print("** Sleep 1 for local queue performance\n")
        try:
            job_info = await worker_info_job(id)
            keep_looping = False
        except KeyError:
            pass
    assert job_info.success is True


async def test_job_success_via_db(db_get_one):
    values = {"bv1": id}
    response = await db_get_one(DatabaseUserContext.DATA, "hello_get_job", values)
    assert response[0] == id


async def test_job_success_via_client(queue_keys):
    assert id in queue_keys
