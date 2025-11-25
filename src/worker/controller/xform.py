# pylint: disable=duplicate-code
from datetime import UTC
from worker.connector.api.connector import Connector as API
from worker.enqueuer.route import Route
from shared.models.constants import JobTypes
from shared.models.xform import ParseRunRequest, XFormServiceResult
from shared.models.worker import (
    XFormEvent,
    ExecutionConfig,
    XFormJobResult,
    JobConfig,
)


class XForm:
    """XForm Controller: Executes jobs transform raw data into the curated"""

    def __init__(self, ctx):
        self.ctx = ctx
        self.config_log = self.ctx["config_log"]
        self.api = API(self.ctx)
        self.time_counter = self.config_log.TimeCounter
        self.asleep = ctx["asleep"]

    def _event(
        self, config_exe: ExecutionConfig, msg: str, results: XFormJobResult | None
    ) -> XFormEvent:
        config_job = config_exe.JobConfig
        return XFormEvent(
            JobId=config_job.Id,
            JobName=config_job.Name,
            Message=msg,
            Status=True,
            Results=results,
            Start=config_exe.Start,
            End=self.config_log.Now(UTC),
            DurationMs=int((self.time_counter() - config_exe.StartCounter) * 1000),
        )

    async def _enqueue(
        self,
        config_exe: ExecutionConfig,
        msg: str,
        result: XFormJobResult = None,
        **kwargs,
    ) -> XFormEvent:
        config_job = config_exe.JobConfig
        enqueue_dto = JobConfig(Type=JobTypes.XFORM, Config=config_job, KWARGS=kwargs)
        enqueue = await Route(self.ctx).execute(True, JobTypes.XFORM, enqueue_dto)
        e_msg = f"{msg}" f" - {enqueue.Message} with status {enqueue.Status}"
        return self._event(config_exe, e_msg, result)

    async def _results(
        self, response: XFormServiceResult, config_exe: ExecutionConfig
    ) -> XFormJobResult:
        """Get XForm results from api by Run ID"""
        action_type = config_exe.JobConfig.ActionType
        param = ParseRunRequest(RunId=response.RunId, ActionType=action_type)
        starter = self.time_counter()
        while int(self.time_counter() - starter) < 1800:
            await self.asleep(5)
            try:
                results = await self.api.xform_job_results(param)
                return XFormJobResult(
                    RunId=results.RunId,
                    Status=True,
                    Results=results.ModelResults,
                    Command=results.Command,
                    Duration=results.Duration,
                    LockAquired=False,
                    Fresh=response.Fresh,
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                if str(e) == "XForm results API returned no data":
                    continue
                raise e
        raise RuntimeError("XForm results API returned no data")

    @staticmethod
    def _short_delay(config: ExecutionConfig) -> ExecutionConfig:
        """Execution Config with a short delay used when dbt is locked"""
        new = config.JobConfig.model_copy(update={"Delay": 60})
        return ExecutionConfig(
            JobConfig=new,
            Start=config.Start,
            StartCounter=config.StartCounter,
        )

    async def execute(self, config_exe: ExecutionConfig, **kwargs) -> XFormEvent:
        """Controler to execute XForm jobs"""
        response = await self.api.xform_exe_jobs(config_exe.JobConfig.Cmd)
        if response.Fresh is False:
            return await self._enqueue(
                self._short_delay(config_exe),
                "dbt not Ready - re-enqueue with short delay",
                XFormJobResult(
                    RunId="n/a",
                    Status=False,
                    Command="n/a",
                    Duration=0,
                    LockAquired=False,
                    Fresh=response.Fresh,
                ),
                **kwargs,
            )
        if response.LockAquired is False:
            return await self._enqueue(
                self._short_delay(config_exe),
                "dbt locked - re-enqueue with short delay",
                XFormJobResult(
                    RunId="n/a",
                    Status=False,
                    Command="n/a",
                    Duration=0,
                    LockAquired=response.LockAquired,
                    Fresh=response.Fresh,
                ),
                **kwargs,
            )
        try:
            results = await self._results(response, config_exe)
            msg = "dbt completed"
            return await self._enqueue(config_exe, msg, results, **kwargs)
        except Exception as e:
            raise e
