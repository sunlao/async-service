from re import compile as rcompile, Pattern
from typing import Optional
from xform.api.v1.helper.command import Command
from xform.api.v1.helper.fresh import Fresh
from shared.models.constants import Tags
from shared.models.xform import DebugResults, XFormServiceResult


class Execution:
    def __init__(self, request):
        self.command = Command(request)
        self.fresh = Fresh(request)
        self.config_log = request.app.state.config_log
        self.lock = request.app.state.lock
        self.request = request

    @staticmethod
    def _match_group(pattern: Pattern[str], text: str, idx: int) -> Optional[str]:
        m = pattern.search(text)
        return m.group(idx) if m else None

    def _debug_results(self, text) -> DebugResults:
        re_ok = rcompile(r"(?i)connection\s+test:.*OK")
        re_db = rcompile(r"(?i)\b(database|dbname)\s*:\s*([^\s]+)")
        re_user = rcompile(r"(?i)\buser\s*:\s*([^\s]+)")
        re_host = rcompile(r"(?i)\bhost\s*:\s*([^\s]+)")
        return DebugResults(
            Status="ok" if (re_ok.search(text)) else "error",
            Host=self._match_group(re_host, text, 1),
            DBName=self._match_group(re_db, text, 2),
            User=self._match_group(re_user, text, 1),
        )

    async def debug(self) -> DebugResults:
        cmd = "dbt debug"
        run = await self.command.run(cmd)
        if run.ReturnCode != 0:
            msg = (
                f"Debug return code: {run.ReturnCode}"
                f"Output: {run.Output} Error: {run.Error}"
            )
            raise RuntimeError(msg)
        out = run.Output
        res = self._debug_results(out)
        return res

    async def tag(self, tag: Tags) -> XFormServiceResult:
        is_fresh = await self.fresh.check(tag)
        if is_fresh is not True:
            return XFormServiceResult(RunId=None, LockAquired=False, Fresh=is_fresh)
        lock_aquired = self.lock.acquire()
        if lock_aquired is True:
            cmd = f"dbt run --select tag:{tag}"
            try:
                run_id = await self.command.run_with_run_id(cmd)
            except Exception as e:
                raise RuntimeError(f"Tag Failed: {str(e)}") from e
            return XFormServiceResult(
                RunId=run_id, LockAquired=lock_aquired, Fresh=is_fresh
            )
        return XFormServiceResult(RunId=None, LockAquired=lock_aquired, Fresh=is_fresh)

    async def seed(self, tag: Tags) -> XFormServiceResult:
        aquired = self.lock.acquire()
        if aquired:
            cmd = f"dbt seed --select path:seeds/{tag}"
            try:
                run_id = await self.command.run_with_run_id(cmd)
            except Exception as e:
                raise RuntimeError(f"Seed Failed: {str(e)}") from e
            return XFormServiceResult(RunId=run_id, LockAquired=aquired)
        return XFormServiceResult(RunId=None, LockAquired=aquired)
