import logging
from typing import Dict
from databases import Database
from src.helpers.db.models import DatabaseUserContext, DatabaseConnectionProfile
from src.helpers.db.secrets import Secrets
from src.helpers.db.query import Query


# database connection settings
MAX_DB_CONNECT_ATTEMPTS = 10
DB_CONNECT_RETRY_DELAY = 3
DB_CONN_TIMEOUT = 10
DB_CONN_POOL_SIZE_MIN_APP = 5
DB_CONN_POOL_SIZE_MAX_APP = 20
DB_CONN_POOL_SIZE_MIN_DATA = 5
DB_CONN_POOL_SIZE_MAX_DATA = 20


# database connection pool objects
db_conn_pools: Dict[DatabaseUserContext, Database] = {
    DatabaseUserContext.APP: None,
    DatabaseUserContext.DATA: None,
}


def _postgres_database_obj(
    conn_profile: DatabaseConnectionProfile,
    conn_pool_size_min: int,
    conn_pool_size_max: int,
):
    user = conn_profile.USER
    passwd = conn_profile.PASSWORD
    host = conn_profile.HOST
    db_name = conn_profile.DB_NAME
    port = conn_profile.PORT
    db_conn_str = f"postgresql+asyncpg://{user}:{passwd}@{host}:{port}/{db_name}"
    return Database(
        db_conn_str,
        min_size=conn_pool_size_min,
        max_size=conn_pool_size_max,
        timeout=DB_CONN_TIMEOUT,
    )


def _query(p_query_name: str) -> str:
    return Query().get(p_query_name)


async def open_database(
    user_context: DatabaseUserContext = DatabaseUserContext.APP,
) -> Database:
    """Create and return a connected Database object to the database,
    with the app user by default.

    The Database object that is returned includes a connection pool. This connection
    pool is closed during FastAPI's shutdown event.
    """
    global db_conn_pools  # pylint: disable=W0602

    # If connection pool is None, create it and connect
    if not db_conn_pools[user_context]:
        secrets = Secrets().db(user_context)
        db_conn_profile = DatabaseConnectionProfile(**secrets)
        db_conn_pools[user_context] = _postgres_database_obj(
            db_conn_profile,
            conn_pool_size_min=DB_CONN_POOL_SIZE_MIN_APP,
            conn_pool_size_max=DB_CONN_POOL_SIZE_MAX_APP,
        )
        logging.debug(
            "Creating initial connection to the database for %d", user_context.value
        )
        await db_conn_pools[user_context].connect()

    # if connection pool is created but not connected, attempt to reconnect
    elif db_conn_pools[user_context].is_connected is False:
        logging.debug(
            "Database object for %d is created, but is reconnecting...",
            user_context.value,
        )
        await db_conn_pools[user_context].connect()

    # otherwise, do nothing
    else:
        logging.debug(
            "Database connection pool for %d is being reused as expected",
            user_context.value,
        )

    return db_conn_pools[user_context]


async def close_database(
    user_context: DatabaseUserContext = DatabaseUserContext.APP,
) -> Database:
    """Close the database connection pool for the given user context"""
    global db_conn_pools  # pylint: disable=W0602

    if db_conn_pools[user_context].is_connected is True:
        await db_conn_pools[user_context].disconnect()
        db_conn_pools[user_context] = None
        logging.debug(
            "Database connection pool for %d has been closed", user_context.value
        )
    else:
        db_conn_pools[user_context] = None
        logging.debug(
            "Database connection pool for %d is already closed", user_context.value
        )


# methods below are convenance wrappers for non fast api use


async def get_one(
    p_user_context: DatabaseUserContext, p_query_name: str, p_values=None
) -> tuple:
    database: Database = await open_database(p_user_context)
    row = await database.fetch_one(query=_query(p_query_name), values=p_values)
    await close_database(p_user_context)
    if row is None:
        return tuple
    return tuple(row.values())


async def get_many(
    p_user_context: DatabaseUserContext, p_query_name: str, p_values=None
) -> tuple:
    database: Database = await open_database(p_user_context)
    rows = await database.fetch_all(query=_query(p_query_name), values=p_values)
    await close_database(p_user_context)
    if rows is None:
        return tuple
    return rows


async def execute_one(
    p_user_context: DatabaseUserContext, p_query_name: str, p_values=None
) -> tuple:
    database: Database = await open_database(p_user_context)
    await database.execute(query=_query(p_query_name), values=p_values)
    await close_database(p_user_context)


async def put_many(
    p_user_context: DatabaseUserContext, p_query_name: str, p_values=None
) -> tuple:
    database: Database = await open_database(p_user_context)
    await database.execute_many(query=_query(p_query_name), values=p_values)
    await close_database(p_user_context)
