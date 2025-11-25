from fastapi import APIRouter, status, Request, HTTPException
from xform.api.v1.helper.execution import Execution
from shared.models.constants import DebugStatus, TouchStatuses
from shared.models.xform import ReadyResponse

router = APIRouter()


@router.get(
    "/ready",
    response_model=ReadyResponse,
    status_code=status.HTTP_200_OK,
)
async def get_ready(request: Request) -> ReadyResponse:
    """Fast API Ready"""
    touch = request.app.state.touch
    state = touch.execute()
    if state == TouchStatuses.NEW:
        try:
            results = Execution(request).debug()
        except Exception as e:
            touch.unlink()
            raise HTTPException(  # pylint: disable=raise-missing-from
                status_code=503, detail=f"Debug raised: {e!s}"
            )
        if results.Status != DebugStatus.OK:
            touch.unlink()
            raise HTTPException(status_code=503, detail="Debug status not OK")
    return ReadyResponse(Status=True)
