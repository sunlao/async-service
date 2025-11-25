from fastapi import APIRouter, Request, status
from shared.models.xform import DebugResults
from xform.api.v1.helper.execution import Execution

router = APIRouter()


@router.get("/debug", response_model=DebugResults, status_code=status.HTTP_200_OK)
async def ready(request: Request) -> DebugResults:
    """Execute DBT debug command"""
    debug = await Execution(request).debug()
    return debug
