from fastapi import APIRouter, status, Request
from shared.models.api import LocationRequest, Location

router = APIRouter()


@router.post(
    "/resolve",
    response_model=Location,
    status_code=status.HTTP_200_OK,
)
async def post_location(request: Request, param: LocationRequest) -> Location:
    """resolve location id by country, state, county, city to support creating
    a profile"""
    db = request.app.state.db
    sql = """
        select location_pk
        from aserv.location
        where country = $1
        and state = $2
        and county = $3
        and city = $4
        """
    args = (param.Country, param.State, param.County, param.City)
    async with db.client() as conn:
        row = await conn.fetchrow(sql, *args)
    return Location(LocationId=row["location_pk"])
