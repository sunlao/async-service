from fastapi import APIRouter, status, Request
from shared.models.api import StatesRequest, States

router = APIRouter()


@router.post(
    "/states/search",
    response_model=States,
    status_code=status.HTTP_200_OK,
)
async def post_states(request: Request, param: StatesRequest) -> States:
    """Search for a list of states by country to support resolving a location"""
    db = request.app.state.db
    sql = """
        select distinct country, state
        from aserv.location
        where country = $1
        order by country, state
        """
    args = (param.Country,)
    async with db.client() as conn:
        rows = await conn.fetch(sql, *args)
    states = tuple(sorted({(row["country"], row["state"]) for row in rows}))
    return States(States=states, Count=len(rows))
