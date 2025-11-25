from fastapi import APIRouter, status, Request
from shared.models.api import CitiesRequest, Cities

router = APIRouter()


@router.post(
    "/cities/search",
    response_model=Cities,
    status_code=status.HTTP_200_OK,
)
async def post_cities(request: Request, param: CitiesRequest) -> Cities:
    """Search for a list of cities by country, state, county to support
    resolving a location"""
    db = request.app.state.db
    sql = """
        select distinct country, state, county, city
        from aserv.location
        where country = $1
        and state = $2
        and county = $3
        order by country, state, county, city
        """
    args = (param.Country, param.State, param.County)
    async with db.client() as conn:
        rows = await conn.fetch(sql, *args)
    cities = tuple(
        sorted(
            {(row["country"], row["state"], row["county"], row["city"]) for row in rows}
        )
    )
    return Cities(Cities=cities, Count=len(rows))
