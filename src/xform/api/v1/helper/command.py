from os import environ
from typing import Optional
from asyncio import wait_for, TimeoutError as ATimeoutError
from shared.models.xform import RunResults


class Command:
    def __init__(self, request):
        self.proc = request.app.state.subprocess
        self.config_xform = request.app.state.config_xform
        self.create_task = request.app.state.create_task
        self.config_log = request.app.state.config_log

    async def _background_run(self, cmd: list[str], env: dict[str, str]) -> None:
        await self.run(cmd, env)

    @staticmethod
    def _text(b: Optional[bytes]) -> str:
        return b.decode("utf-8", "replace").strip() if b else ""

    async def run(self, cmd: str, env: Optional[dict] = None) -> RunResults:
        proc = await self.proc.create_subprocess_shell(
            cmd,
            cwd=str(self.config_xform.Dir),
            env=env,
            stdout=self.proc.PIPE,
            stderr=self.proc.PIPE,
        )
        try:
            out, err = await wait_for(proc.communicate(), timeout=30)
            return_code = proc.returncode or 0
        except ATimeoutError:
            proc.kill()
            out, err = await proc.communicate()
            return_code = 124
        return RunResults(
            ReturnCode=return_code, Output=self._text(out), Error=self._text(err)
        )

    async def run_with_run_id(self, cmd: str) -> str:
        run_id = str(self.config_log.UUID4())
        env = dict(environ)
        env["DBT_ENV_CUSTOM_ENV_RUN_ID"] = run_id
        self.create_task(self._background_run(cmd, env))
        return run_id
