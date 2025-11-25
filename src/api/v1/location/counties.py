from fastapi import APIRouter, status, Request
from shared.models.api import CountiesRequest, Counties

router = APIRouter()


@router.post(
    "/counties/search",
    response_model=Counties,
    status_code=status.HTTP_200_OK,
)
async def post_counties(request: Request, param: CountiesRequest) -> Counties:
    """Search for a list of counties by country, state to support resolving a location"""
    db = request.app.state.db
    sql = """
        select distinct country, state, county
        from aserv.location
        where country = $1
        and state = $2
        order by country, state, county
        """
    args = (param.Country, param.State)
    async with db.client() as conn:
        rows = await conn.fetch(sql, *args)
    counties = tuple(
        sorted({(row["country"], row["state"], row["county"]) for row in rows})
    )
    return Counties(Counties=counties, Count=len(rows))
