# pylint: disable=duplicate-code
from asyncio import sleep, timeout

name = "TestHelloAPI"
job_id = 102


# pylint: disable=duplicate-code
async def test_enqueue_and_runs_pass(aserv_api_client):
    response = await aserv_api_client.post(f"enqueue/{job_id}")
    doc = response.json()
    assert response.status_code == 202
    run_id = doc["RunID"]
    response = await aserv_api_client.get(f"runs/{run_id}")
    assert response.status_code == 200
    doc = response.json()
    status = doc["Status"]
    async with timeout(300):
        while status != "complete":
            await sleep(5)
            response = await aserv_api_client.get(f"runs/{run_id}")
            doc = response.json()
            status = doc["Status"]
    assert status == "complete"
    assert doc["Info"]["Event"]["Status"] is True
    assert doc["Info"]["Core"]["Message"] == f"aserv-worker Execute Job: {name}"
