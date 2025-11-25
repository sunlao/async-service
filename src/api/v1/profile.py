from fastapi import APIRouter, status, Request
from shared.models.api import ProfileRequest, Profile

router = APIRouter()


@router.post(
    "/create",
    response_model=Profile,
    status_code=status.HTTP_200_OK,
)
async def post_profile(request: Request, param: ProfileRequest) -> Profile:
    """Create a profile"""
    db = request.app.state.db
    sql = "select profile_pk, action from aserv.merge_profile($1, $2, $3)"
    args = (param.LocationId, param.Name, param.BirthDateTime)
    async with db.client() as conn:
        row = await conn.fetchrow(sql, *args)
    return Profile(ProfileId=row["profile_pk"], Action=row["action"])
