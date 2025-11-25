# fixtures_dbt.py
# pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name
import os
import json
import time
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from pytest import fixture
from fastapi import FastAPI, Request
from xform.api.v1.helper.lock import Lock
from xform.api.v1.helper.touch import Touch
from shared.log.helpers.api_log_serializer import LogSerializer
from shared.log.writer import Writer
from shared.log.helpers.error import Error

test_data = Path.cwd() / "tests" / "data" / "xform_runs"


@asynccontextmanager
async def _build_app_with_state(config_log, config_xform):
    app = FastAPI()

    s = app.state
    s.subprocess = asyncio.subprocess
    s.log = Writer(config_log)
    s.log_error_helper = Error()
    s.config_log = config_log
    s.config_xform = config_xform
    s.create_task = asyncio.create_task
    s.format_log = LogSerializer()
    s.app_version = config_xform.AppVersion

    # Test-local paths (isolated per test run)
    s.run_result_path = test_data / "run_results.json"
    s.path_fresh = test_data / "sources.json"
    s.lock_path = test_data / ".dbt.lock"
    s.ready_path = test_data / ".ready.lock"

    # Inject stdlib helpers exactly like main
    s.load = json.load
    s.dump = json.dump
    s.time = time.time
    s.os = os

    # for testing set lock expiration to 4 seconds
    s.lock_expiration = 4
    s.lock = Lock(s)
    s.lock.release()
    s.touch = Touch(s)

    try:
        yield app
    finally:
        s.lock.release()
        s.touch.unlink()


@fixture
async def xform_with_state(config_log, config_xform):
    async with _build_app_with_state(config_log, config_xform) as app:
        yield app


@fixture
def dbt_request(xform_with_state: FastAPI) -> Request:
    scope = {
        "type": "http",
        "app": xform_with_state,
        "headers": [],
        "method": "GET",
        "path": "/_test",
        "query_string": b"",
    }
    return Request(scope)
