from datetime import datetime
from pydantic import BaseModel


class JobResult(BaseModel):
    status_code: int
    function: str
    message: str
    complete: datetime
