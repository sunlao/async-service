# pylint: disable=duplicate-code
from asyncio import sleep, timeout
from shared.models.constants import ActionTypes


tag = "test"
job_id = 102


async def test_hello_state(db_get_one, db_execute, arq_client):
    """
    asserts:
      - dbt seed for hello path hasn't been ran
      - job for hello_test_api hasn't been ran
    """
    result = await db_get_one("hello_seed_exists")
    exist_flg = result[0] == 1
    if exist_flg is True:
        await db_execute("hello_seed_drop")
    result = await db_get_one("hello_seed_exists")
    exist_flg = result[0] == 1
    assert exist_flg is False

    await db_execute("hello_test_trunc")
    result = await db_get_one("hello_test_api_cnt")
    assert result[0] == 0
    await arq_client.delete_by_job_id(job_id)


async def test_hello_not_ready_seed(xform_api_client):
    """
    asserts execution:
        - xform run by tag
          - 412 fail because data not fresh
        - Execute seed 1x submitt success
        - Execute seed again before getting results
          - 423 fail because xform locked
        - Get Seed results
    """

    # cant execute cause source seed data not fresh
    response = await xform_api_client.post(f"run/{tag}", timeout=30)
    status = response.status_code
    assert status == 412  # 412 Precondition Fail - data not ready

    # seed after failure
    async with timeout(300):
        status = 423
        while status == 423:  # loop if other jobs have locked system
            response = await xform_api_client.post(f"seed/{tag}", timeout=30)
            status = response.status_code
            await sleep(5)
    assert response.status_code == 202  # accept
    doc = response.json()
    run_id = doc["RunId"]

    # cant execute cause locked
    response = await xform_api_client.post(f"seed/{tag}", timeout=30)
    status = response.status_code
    assert status == 423  # locked cant submit twice

    # get seed results to unlock and validate
    async with timeout(300):
        seed_data = {"RunId": run_id, "ActionType": ActionTypes.SEED}
        status = 204
        while status == 204:  # sleep watining for content
            response = await xform_api_client.post(
                "results", json=seed_data, timeout=30
            )
            status = response.status_code
            await sleep(3)
    assert status == 200  # got results and unlocked
    doc = response.json()
    models = doc["ModelResults"]
    assert len(models) == 1  # seeded 1 model
    assert models[0]["Name"] == "hello_seed"


async def test_hello_not_ready_job(xform_api_client, aserv_api_client):
    """
    asserts execution:
        - xform run by tag
          - 412 fail because data not fresh
        - Enqueue hello_test_api
          - get results
          - assert event status is true
    """

    # cant execute cause source job data not fresh
    response = await xform_api_client.post(f"run/{tag}", timeout=30)
    status = response.status_code
    assert status == 412  # fail data not fresh

    # run source job  graceful failure
    response = await aserv_api_client.post(f"enqueue/{job_id}")
    doc = response.json()
    # sumbitted or already submitted
    assert response.status_code == 202
    run_id = doc["RunID"]
    status = "unknown"
    # check status till complete
    async with timeout(300):
        while status != "complete":
            await sleep(5)
            response = await aserv_api_client.get(f"runs/{run_id}")
            doc = response.json()
            status = doc["Status"]
    assert status == "complete"
    assert doc["Info"]["Event"]["Status"] is True


async def test_xform_data_fresh(xform_api_client):
    # run xform for test tag data now fresh
    async with timeout(300):
        status = 423
        while status == 423:  # wait if locked by other jobs
            response = await xform_api_client.post(f"run/{tag}", timeout=30)
            status = response.status_code
            await sleep(5)
    doc = response.json()
    assert response.status_code == 202

    run_id = doc["RunId"]

    # get xform results to unlock
    async with timeout(300):
        payload = {"RunId": run_id, "ActionType": ActionTypes.RUN}
        status = 204
        while status == 204:
            response = await xform_api_client.post("results", json=payload, timeout=30)
            status = response.status_code
            await sleep(2)
    doc = response.json()
    models = doc["ModelResults"]
    for model in models:
        assert model["ModelStatus"] == "success"
        if model["Name"] == "working.test_hello_seed":
            assert model["RowsAffected"] == 1
