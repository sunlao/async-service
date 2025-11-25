from fastapi import APIRouter, status, Request
from shared.models.api import Countries

router = APIRouter()


@router.get(
    "/countries",
    response_model=Countries,
    status_code=status.HTTP_200_OK,
)
async def get_countries(request: Request) -> Countries:
    """Search for a list of countries to support resolving a location"""
    db = request.app.state.db
    sql = "select distinct country from aserv.location order by country"
    async with db.client() as conn:
        rows = await conn.fetch(sql)
    countries = tuple(sorted({row["country"] for row in rows}))
    return Countries(Countries=countries, Count=len(rows))
