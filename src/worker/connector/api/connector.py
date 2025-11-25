# edge-allow: pathlib, open, httpx
from pathlib import Path
from hashlib import sha256
from httpx import HTTPStatusError
from fastapi import status
from shared.models.constants import ActionTypes
from shared.models.worker import BinaryOutput
from shared.models.xform import XFormServiceResult, ResultsResponse, ParseRunRequest


class Connector:
    # pylint: disable=duplicate-code
    def __init__(self, ctx):
        self.ctx = ctx
        cwd_parent = Path(self.ctx["data_dir"])
        self.zip_path = cwd_parent.joinpath("zip")
        self.ready_path = cwd_parent.joinpath("ready")
        self.http_client = ctx["http_client"]

    async def download(
        self, command: str, name: str, action_type: ActionTypes
    ) -> BinaryOutput:
        file_hash = sha256()
        size_bytes = 0
        async with self.http_client.stream("GET", command) as response:
            response.raise_for_status()
            path = None
            if action_type == ActionTypes.BINC:
                path = self.zip_path.joinpath(name)
            if action_type == ActionTypes.BINU:
                path = self.ready_path.joinpath(name)
            if path is None:
                raise RuntimeError(f"Action type: {action_type} is not supported")
            with open(path, "wb") as file:
                async for chunk in response.aiter_bytes(chunk_size=1 << 20):  # 1 MiB
                    if not chunk:
                        continue
                    file.write(chunk)
                    file_hash.update(chunk)
                    size_bytes += len(chunk)
        return BinaryOutput(BytesSHA256=file_hash.hexdigest(), BytesLen=size_bytes)

    async def xform_exe_jobs(self, cmd: str) -> XFormServiceResult:
        try:
            response = await self.http_client.post(cmd)
            response.raise_for_status()
        except HTTPStatusError as exc:
            if exc.response.status_code == status.HTTP_423_LOCKED:
                return XFormServiceResult(LockAquired=False, RunId=None, Fresh=None)
            if exc.response.status_code == status.HTTP_412_PRECONDITION_FAILED:
                return XFormServiceResult(LockAquired=False, RunId=None, Fresh=False)
            raise
        doc = response.json()
        return XFormServiceResult(
            RunId=doc["RunId"], LockAquired=doc["LockAquired"], Fresh=doc["Fresh"]
        )

    async def xform_job_results(self, param: ParseRunRequest) -> ResultsResponse:
        cmd = "http://aserv-dbt:81/api/v1/results"
        response = await self.http_client.post(cmd, json=param.model_dump())
        response.raise_for_status()
        if response.status_code == 200:
            doc = response.json()
            return ResultsResponse(
                RunId=doc["RunId"],
                Command=doc["Command"],
                ModelResults=doc["ModelResults"],
                Duration=doc["Duration"],
            )
        if response.status_code == 204:
            raise RuntimeError("XForm results API returned no data")
        raise RuntimeError(f"Unexpected Status: {response.status_code}")
