# pylint: disable=duplicate-code
from asyncio import sleep, timeout
from shared.models.xform import XFormServiceResult, ResultsResponse


async def test_tag(xform_api_client):
    block_flag = None
    status = 423
    async with timeout(300):
        while status == 423:
            response = await xform_api_client.post("tag/test", timeout=30)
            status = response.status_code
            if status == 423:
                block_flag = True
            print("****sleep 1 seconds while waiting for dbt to unlock")
            await sleep(1)
    assert response.status_code == 202
    doc = response.json()
    assert XFormServiceResult.model_validate(doc)
    run_id = doc["RunId"]
    run = {"RunId": run_id, "ActionType": "run"}

    # assert dbt locks until results are retrieved
    if block_flag is None:
        response = await xform_api_client.post("tag/test", timeout=30)
        status = response.status_code
        assert status == 423

    status = 204
    async with timeout(300):
        while status == 204:
            response = await xform_api_client.post("results", json=run, timeout=30)
            status = response.status_code
            print("****sleep 2 seconds while waiting for dbt to finish")
            await sleep(2)
    doc = response.json()
    assert ResultsResponse.model_validate(doc)
    models = doc["ModelResults"]
    model = [m for m in models if m.get("Name") == "working.test_hello"][0]
    assert model["ModelStatus"] == "success"
    assert model["RowsAffected"] == 1
    assert model["Failures"] is None
