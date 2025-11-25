from pytest import fixture
from httpx import AsyncClient


@fixture
async def aserv_api_client():
    test_api = "http://aserv-api:80/api/v1/"
    async with AsyncClient(base_url=test_api, timeout=10) as client:
        yield client


@fixture
async def xform_api_client():
    test_api = "http://aserv-dbt:81/api/v1/"
    async with AsyncClient(base_url=test_api, timeout=10) as client:
        yield client
