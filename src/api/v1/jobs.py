from fastapi import APIRouter, status, HTTPException
from src.helpers.worker import job_submit
from src.helpers.worker.models import JobExecution, JobSubmit


router = APIRouter()


@router.post(
    "/jobs",
    response_model=JobSubmit,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_job(post_data: JobExecution):
    response = await job_submit(post_data)
    if response["status"].startswith("Job Id:") and response["status"].endswith(
        "already submitted"
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=response["status"],
        )
    return response
