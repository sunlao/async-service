from shared.models.api import InfoResponse


async def test_api_info(xform_api_client):
    response = await xform_api_client.get("info")
    assert response.status_code == 200
    doc = response.json()
    assert InfoResponse.model_validate(doc)
