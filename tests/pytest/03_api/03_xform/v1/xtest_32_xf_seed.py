from pathlib import Path
from asyncio import sleep, timeout
from shared.models.xform import XFormServiceResult, ResultsResponse


test_data = Path("/data/xform_runs")
lock_file = test_data / ".dbt.lock"


async def test_seed(xform_api_client):
    lock_flg = lock_file.is_file()
    print(f"lock flg: {lock_flg}")
    for f in sorted(test_data.iterdir()):
        print(f"**dir item: {f}")
    async with timeout(300):
        status = 423
        while status == 423:
            response = await xform_api_client.post("seed", timeout=30)
            status = response.status_code
            doc = response.json()
            print(f"****Status: {status} -  doc:{doc}")
            print("****sleep 1 seconds while waiting for dbt to unlock")
            await sleep(1)
    assert response.status_code == 202
    doc = response.json()
    assert XFormServiceResult.model_validate(doc)
    run_id = doc["RunId"]
    assert doc["Locked"] is False
    seed = {"RunId": run_id, "ActionType": "seed"}
    status = 204
    async with timeout(300):
        while status == 204:
            response = await xform_api_client.post("results", json=seed, timeout=30)
            status = response.status_code
            print("****sleep 2 seconds while waiting for dbt to finish")
            await sleep(2)
    doc = response.json()
    assert ResultsResponse.model_validate(doc)
    models = doc["ModelResults"]
    model = [m for m in models if m.get("Name") == "hello"][0]
    assert model["ModelStatus"] == "success"
    assert model["RowsAffected"] == 1
    assert model["Failures"] is None
