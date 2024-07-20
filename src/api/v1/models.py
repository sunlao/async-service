from pydantic import BaseModel


class Info(BaseModel):
    FastApiVersion: str
    CD_Version: str
    DB_HealthCheck: str


class Ready(BaseModel):
    DB_Check: str
    Queue_Check: str
