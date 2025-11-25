from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler

router = APIRouter()


async def tag_enum_to_404(request: Request, exc: RequestValidationError):
    for err in exc.errors():
        loc = tuple(err.get("loc", ()))
        msg = err.get("msg", "")
        if (
            "tag" in loc
            and err.get("type") == "enum"
            and isinstance(msg, str)
            and msg.startswith("Input should be")
        ):
            bad_input = err.get("input", request.path_params.get("tag"))
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "unknown tag", "input": bad_input},
            )
    return await request_validation_exception_handler(request, exc)
