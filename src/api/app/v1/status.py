from os import environ
from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from src.helpers.worker import info_jobs
from src.api.app.v1.support import html_table


router = APIRouter()

template_path = f"{environ['API_STATIC_DIR']}/templates"
templates = Jinja2Templates(directory=template_path)


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
)
async def get_html_all_jobs_status(request: Request):
    rows = await info_jobs()
    return templates.TemplateResponse(
        "index.html", {"request": request, "table": html_table(rows)}
    )
