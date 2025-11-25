async def test_aserv(aserv_api_client):
    response = await aserv_api_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert response.json() == {"Message": "AsyncServ API Service is up!"}


async def test_xform(xform_api_client):
    response = await xform_api_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert response.json() == {"Message": "XForm API Service for AsyncServ is up!"}
