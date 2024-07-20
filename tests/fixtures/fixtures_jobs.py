from pytest import fixture
from src.jobs.hello import Hello
from src.helpers.worker import info_job, info_jobs


@fixture
def hello_job():
    return Hello


@fixture(scope="module")
def worker_info_job():
    return info_job


@fixture
async def worker_info_jobs():
    return await info_jobs()
