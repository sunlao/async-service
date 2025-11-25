# pylint: disable=duplicate-code
async def test_tag(xform_api_client):
    bad_tag = "invalid"
    response = await xform_api_client.post(f"tag/{bad_tag}", timeout=30)
    status = response.status_code
    assert status == 404
    doc = response.json()
    assert doc["input"] == bad_tag
