from shared.models.xform import ReadyResponse


async def test_api_ready(xform_api_client):
    response = await xform_api_client.get("ready", timeout=30)
    assert response.status_code == 200
    doc = response.json()
    assert ReadyResponse.model_validate(doc)
