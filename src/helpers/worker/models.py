from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class JobExecution(BaseModel):
    id: str
    function: str
    input_params: Optional[dict] = None
    status_code: Optional[str] = None
    start_ts: Optional[datetime] = None
    end_ts: Optional[datetime] = None
    execution_start_ts: Optional[datetime] = None
    execution_end_ts: Optional[datetime] = None


class JobInfo(BaseModel):
    function: str
    args: List[JobExecution]
    kwargs: Optional[dict] = None
    job_try: Optional[str] = None
    enqueue_time: datetime
    score: int


class JobSubmit(BaseModel):
    status: str
    job_info: Optional[JobInfo] = None
    job_id: Optional[str] = None
