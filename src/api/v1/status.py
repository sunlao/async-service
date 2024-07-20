from typing import List
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from arq.jobs import JobResult
from src.helpers.worker import info_jobs, info_job


router = APIRouter()


@router.get(
    "/status",
    response_model=List[JobResult],
    status_code=status.HTTP_200_OK,
)
async def get_all_jobs_status():
    records = await info_jobs()
    return [jsonable_encoder(record) for record in records]


@router.get(
    "/status/{job_id}", response_model=JobResult, status_code=status.HTTP_200_OK
)
async def get_job_status(job_id: str):
    try:
        response = await info_job(job_id)
    except KeyError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        ) from exception
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return response
