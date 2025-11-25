from typing import Optional
from pydantic import BaseModel
from shared.models.constants import DBTTypes, DebugStatus, Tags, TouchStatuses
from shared.models.policy import DTO_CONFIG


class XFormConfig(BaseModel):
    model_config = DTO_CONFIG
    AppVersion: str
    Dir: str
    Timeout: int


class TouchResponse(BaseModel):
    """DTO for api output /info"""

    model_config = DTO_CONFIG
    Status: TouchStatuses


class ReadyResponse(BaseModel):
    model_config = DTO_CONFIG
    Status: bool


class DebugResults(BaseModel):
    model_config = DTO_CONFIG
    Status: DebugStatus
    Host: str
    DBName: str
    User: str


class RunResults(BaseModel):
    model_config = DTO_CONFIG
    ReturnCode: int
    Output: str
    Error: Optional[str] = None


class XFormServiceResult(BaseModel):
    model_config = DTO_CONFIG
    RunId: Optional[str] = None
    LockAquired: bool
    Fresh: Optional[bool] = None


class ParseRunRequest(BaseModel):
    model_config = DTO_CONFIG
    RunId: str
    ActionType: DBTTypes


class ModelResult(BaseModel):
    model_config = DTO_CONFIG
    ModelStatus: str
    ExecutionTime: Optional[float] = None
    RowsAffected: Optional[int] = None
    Name: Optional[str] = None
    Failures: Optional[int] = None


class ResultsResponse(BaseModel):
    model_config = DTO_CONFIG
    RunId: str
    Command: str
    ModelResults: tuple[ModelResult, ...]
    Duration: float


class ParseRunResponse(BaseModel):
    model_config = DTO_CONFIG
    Status: bool
    RunId: Optional[str] = None
    Command: Optional[str] = None
    RunResults: Optional[tuple[ModelResult, ...]] = None
    Duration: Optional[float] = None


class FreshResult(BaseModel):
    model_config = DTO_CONFIG
    Model: str
    FreshFlag: bool


class FreshResults(BaseModel):
    model_config = DTO_CONFIG
    Tag: Tags
    Result: tuple[FreshResult, ...]
