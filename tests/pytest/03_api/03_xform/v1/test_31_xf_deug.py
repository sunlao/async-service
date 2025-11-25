from shared.models.xform import DebugResults


async def test_debug(xform_api_client):
    response = await xform_api_client.get("debug", timeout=30)
    assert response.status_code == 200
    doc = response.json()
    assert DebugResults.model_validate(doc)
    assert doc["Status"] == "ok"
    assert doc["Host"] == "aserv-postgres"
    assert doc["DBName"] == "db_aserv"
    assert doc["User"] == "aserv_data"
