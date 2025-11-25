from asyncio import timeout, sleep
from shared.models.api import Countries, States, Counties, Cities, Location


async def test_api_country(aserv_api_client):
    cnt = 0
    async with timeout(300):
        while cnt == 0:
            response = await aserv_api_client.get("location/countries")
            assert response.status_code == 200
            doc = response.json()
            cnt = doc["Count"]
            await sleep(3)
    assert Countries.model_validate(doc)
    assert doc["Count"] > 200


async def test_api_states(aserv_api_client):
    param = {"Country": "United States"}
    cnt = 0
    async with timeout(300):
        while cnt == 0:
            response = await aserv_api_client.post("location/states/search", json=param)
            assert response.status_code == 200
            doc = response.json()
            cnt = doc["Count"]
            await sleep(3)
    assert States.model_validate(doc)
    assert doc["Count"] == 51


async def test_api_counties(aserv_api_client):
    cnt = 0
    param = {"Country": "United States", "State": "Oregon"}
    async with timeout(300):
        while cnt == 0:
            response = await aserv_api_client.post(
                "location/counties/search", json=param
            )
            assert response.status_code == 200
            doc = response.json()
            cnt = doc["Count"]
            await sleep(3)
    assert Counties.model_validate(doc)
    assert doc["Count"] >= 36


async def test_api_cities(aserv_api_client):
    cnt = 0
    param = {
        "Country": "United States",
        "State": "Oregon",
        "County": "Multnomah County",
    }
    async with timeout(300):
        while cnt == 0:
            response = await aserv_api_client.post("location/cities/search", json=param)
            assert response.status_code == 200
            doc = response.json()
            cnt = doc["Count"]
            await sleep(3)
    assert Cities.model_validate(doc)
    assert doc["Count"] >= 8


async def test_api_location(aserv_api_client):
    param = {
        "Country": "United States",
        "State": "Oregon",
        "County": "Multnomah County",
        "City": "Portland",
    }
    response = await aserv_api_client.post("location/resolve", json=param)
    assert response.status_code == 200
    assert Location.model_validate(response.json())
