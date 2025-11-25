# pylint: disable=duplicate-code
import os
from json import load, dump
from time import time
from pathlib import Path
from contextlib import asynccontextmanager
from asyncio import subprocess, create_task
from starlette.responses import PlainTextResponse
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from xform.api.v1 import debug, info, run, seed, results, ready, flush
from xform.api.v1.validators.tag import tag_enum_to_404
from xform.api.v1.helper.lock import Lock
from xform.api.v1.helper.touch import Touch
from shared.config.locker import Locker
from shared.log.helpers.api_log_serializer import LogSerializer
from shared.log.writer import Writer
from shared.log.helpers.error import Error
from shared.log.helpers.core import build as core_log
from shared.models.api import RootResponse, ASGIEvent
from shared.models.constants import Events, LogLevel
from shared.models.log import EventError

locker = Locker()
config_xform = locker.xform()
config_log = locker.log()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.subprocess = subprocess
    app.state.log = Writer(config_log)
    app.state.log_error_helper = Error()
    app.state.config_log = config_log
    app.state.config_xform = config_xform
    app.state.create_task = create_task
    app.state.format_log = LogSerializer()
    app.state.app_version = config_xform.AppVersion
    app.state.run_result_path = Path("/data/xform_runs/run_results.json")
    app.state.lock_path = Path("/data/xform_runs/.dbt.lock")
    app.state.ready_path = Path("/data/xform_runs/.ready.lock")
    app.state.path_fresh = Path("/data/xform_runs/sources.json")
    app.state.load = load
    app.state.dump = dump
    app.state.time = time
    app.state.os = os
    msg = "dbt API Service Startup complete"
    core = core_log(config_log, LogLevel.INFO, Events.STARTUP, msg)
    app.state.log.write_core(core)
    app.state.lock_expiration = 1800
    app.state.lock = Lock(app.state)
    app.state.lock.release()
    app.state.touch = Touch(app.state)
    try:
        yield
    finally:
        msg = "dbt API Service Shutdown complete"
        core = core_log(config_log, LogLevel.INFO, Events.SHUTDOWN, msg)
        app.state.log.write_core(core)
        app.state.lock.release()
        app.state.touch.unlink()


def create_api() -> FastAPI:
    _api = FastAPI(
        title="dbt Service for AsyncServ",
        version=f"Version: {config_xform.AppVersion}",
        lifespan=lifespan,
    )

    # used for central api logging events
    @_api.middleware("http")
    async def _access_mw(
        request: Request, call_next
    ):  # pylint: disable=too-many-locals
        start = config_log.TimeCounter()
        request.app.state.txid = request.app.state.format_log.transaction_id(request)
        try:
            response: Response = await call_next(request)
            error = None
            trace_back_nfo = None
        except Exception as e:  # pylint: disable=broad-except
            response = PlainTextResponse(
                "Unknown Internal Server Error", status_code=500
            )
            error = e
            trace_back_nfo = request.app.state.log_error_helper.trace_back_nfo(e)
        finally:
            duration = int((config_log.TimeCounter() - start) * 1000)
            msg = request.app.state.format_log.message(response)
            core_event = core_log(config_log, LogLevel.INFO, Events.ACCESS, msg)
            event_input = ASGIEvent(
                Request=request, Response=response, DurationMS=duration
            )
            log_dto = request.app.state.format_log.build(core_event, event_input)
            if error is None:
                request.app.state.log.write_event(dto=log_dto)
            else:
                err_core = core_log(
                    config_log, LogLevel.ERROR, Events.HTTP_ERROR, str(error)
                )
                error_event_input = ASGIEvent(
                    Request=request, Response=response, DurationMS=duration
                )
                error_event_dto = request.app.state.format_log.build(
                    err_core, error_event_input
                )
                error_event_error_dto = EventError(
                    Core=error_event_dto.Core,
                    Event=error_event_dto.Event,
                    Error=trace_back_nfo,
                )
                request.app.state.log.write_event_error(dto=error_event_error_dto)
        return response

    @_api.get("/api/v1")
    async def root() -> RootResponse:
        """Application Root"""
        return RootResponse(Message="XForm API Service for AsyncServ is up!")

    # routing
    _api.include_router(info.router, prefix="/api/v1", tags=["info"])
    _api.include_router(debug.router, prefix="/api/v1", tags=["debug"])
    _api.include_router(run.router, prefix="/api/v1", tags=["run"])
    _api.include_router(seed.router, prefix="/api/v1", tags=["seed"])
    _api.include_router(results.router, prefix="/api/v1", tags=["results"])
    _api.include_router(ready.router, prefix="/api/v1", tags=["ready"])
    _api.include_router(flush.router, prefix="/api/v1", tags=["flush"])
    _api.add_exception_handler(RequestValidationError, tag_enum_to_404)

    return _api


api = create_api()
