from datetime import datetime
from logging import info as log_info
from fastapi import APIRouter, status
from databases import Database
from src.helpers.db import open_database
from src.helpers.queue.client import Client
from src.api.v1.models import Ready

router = APIRouter()


@router.get(
    "/ready",
    response_model=Ready,
    status_code=status.HTTP_200_OK,
)
async def get_ready():
    database: Database = await open_database()
    row = await database.fetch_one(query="select count(*) from aserv.hello_world")
    queue_health = Client().health()
    if (
        queue_health["status-length"] == 7
        and queue_health["complete"] >= 0
        and queue_health["queued"] >= 0
        # health checks run every hour by default
        and ((datetime.utcnow() - queue_health["date-time"]).seconds / 60 / 60) <= 1
    ):
        queue_result = 0
    else:
        queue_result = -1
        log_info("Worker not ready\n queue_health: %s", queue_health)

    if row[0] >= 0 and queue_result == 0:
        return {
            "DB_Check": "ready",
            "Queue_Check": "ready",
        }
