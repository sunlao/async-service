from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from shared.models.constants import Tags
from shared.models.xform import XFormServiceResult
from xform.api.v1.helper.execution import Execution

router = APIRouter()


@router.post(
    "/run/{tag}",
    response_model=XFormServiceResult,
    status_code=status.HTTP_202_ACCEPTED,
)
# pylint: disable=duplicate-code
async def post_run(request: Request, tag: Tags) -> XFormServiceResult:
    """Execute DBT run command with tag if not locked"""
    response = await Execution(request).tag(tag)
    if response.Fresh is False:
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            content={
                "Fresh": response.Fresh,
                "Error": "Source data is not Fresh",
            },
        )
    if response.LockAquired is False:
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={
                "LockAquired": response.LockAquired,
                "Error": "Service already locked for execution",
            },
        )
    return response
