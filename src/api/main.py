from os import environ
from logging import info as log_info
from time import sleep
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.metadata import tags
from src.helpers.db import (
    open_database,
    close_database,
    MAX_DB_CONNECT_ATTEMPTS,
    DB_CONNECT_RETRY_DELAY,
)
from src.api.v1 import info, ready, version_app, jobs, status
from src.api.app.v1 import status as app_status

api = FastAPI(
    title="Hello Service Api", version=f"Version: {version_app()}", openapi_tags=tags()
)

api.mount("/static", StaticFiles(directory=environ["API_STATIC_DIR"]), name="static")


@api.on_event("startup")
async def startup():
    """Create database connections pool"""
    conn_attempts = 0
    while True:
        if conn_attempts == MAX_DB_CONNECT_ATTEMPTS:
            raise ValueError("Database connection attempts exceeded")
        try:
            conn_attempts += 1
            await open_database()
            break
        except:  # pylint: disable=W0702
            log_info("Database is not ready, sleeping for %ss", DB_CONNECT_RETRY_DELAY)
            sleep(DB_CONNECT_RETRY_DELAY)


@api.on_event("shutdown")
async def shutdown():
    """Close database connections pool"""
    log_info("^^^ SHUTDOWN EVENT")
    await close_database()


@api.get("/")
async def root():
    return {"message": "Heath check good!"}


# routing
api.include_router(info.router, prefix="/api/v1", tags=["info"])
api.include_router(ready.router, prefix="/api/v1", tags=["ready"])
api.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
api.include_router(status.router, prefix="/api/v1", tags=["status"])
api.include_router(app_status.router, prefix="/app/v1", tags=["status"])
