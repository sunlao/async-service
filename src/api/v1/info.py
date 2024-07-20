from fastapi import APIRouter, __version__ as version, status
from databases import Database
from src.helpers.db import open_database
from src.api.v1.models import Info
from src.api.v1 import version_app

router = APIRouter()


@router.get(
    "/info",
    response_model=Info,
    status_code=status.HTTP_200_OK,
)
async def get_info():
    database: Database = await open_database()
    row = await database.fetch_one(query="SELECT 'Connected'")
    return {
        "FastApiVersion": version,
        "CD_Version": version_app(),
        "DB_HealthCheck": row[0],
    }
