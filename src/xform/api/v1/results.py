from fastapi import APIRouter, Request, status, Response
from shared.models.xform import ParseRunRequest, ResultsResponse
from xform.api.v1.helper.parser import Parser

router = APIRouter()


@router.post("/results", response_model=ResultsResponse, status_code=status.HTTP_200_OK)
async def results(request: Request, data: ParseRunRequest) -> ResultsResponse:
    """Return DBT reults by RunID by action type if available"""
    response = Parser(request).run(data)
    if response.Status is True:
        return ResultsResponse(
            RunId=response.RunId,
            Command=response.Command,
            ModelResults=response.RunResults,
            Duration=response.Duration,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
