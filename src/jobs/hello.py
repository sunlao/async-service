from logging import info, error
from traceback import format_exc
from datetime import datetime
from src.jobs.models import JobResult
from src.helpers.db.models import DatabaseUserContext
from src.helpers.db import execute_one


class TestErrorHandling(Exception):
    def __init__(self, p_job_id):
        super().__init__(f"{p_job_id} failed as part of testing error handling")


class Hello:
    def __init__(self, p_job_id):
        self.now = datetime.now()
        self.function = "Hello.execute"
        self.job_id = p_job_id
        start_response = {
            "job_id": self.job_id,
            "function": self.function,
            "message": "start",
            "init_ts": self.now,
        }
        info(f"start: {start_response}")

    # pylint: disable=unused-argument
    async def _insert(self, p_job_id, ctx, **kwargs):
        if kwargs.get("key1", "pass") == "fail":
            raise TestErrorHandling(p_job_id)
        values = {"bv1": p_job_id, "bv2": self.now}
        await execute_one(DatabaseUserContext.DATA, "hello_insert_job", values)

    # pylint: disable=broad-exception-caught
    # pylint: disable=unused-variable
    # Catch all errors in execution of private job methods for application logging
    # without disruption
    async def execute(self, ctx, **kwargs) -> JobResult:
        result = {
            "job_id": self.job_id,
            "function": self.function,
        }
        try:
            await self._insert(self.job_id, ctx, **kwargs)
        except Exception as e:
            result["message"] = format_exc()
            result["status_code"] = -1
            result["now"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            error(result)
            result.pop("job_id")
            return result

        result["status_code"] = 0
        result["message"] = "complete"
        result["now"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        info(f"complete: {result}")
        result.pop("job_id")
        return result
