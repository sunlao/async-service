from src.helpers.db import get_one
from src.helpers.db.models import DatabaseUserContext


async def db_single_job() -> tuple:
    record = await get_one(DatabaseUserContext.DATA, "hello_single_job")
    return record[0]
