from src.helpers.db.models import DatabaseUserContext
from tests.fixtures.fixtures_db import (
    db_execute_one,
    db_get_one,
    db_get_many,
    db_put_many,
)


async def test_hello_postgres_app(db_get_one):
    await db_get_one(DatabaseUserContext.APP, "hello_postgres")


async def test_hello_postgres_data(db_get_one):
    assert await db_get_one(DatabaseUserContext.DATA, "hello_postgres")


async def test_hello_truncate(db_execute_one, db_get_one):
    await db_execute_one(DatabaseUserContext.DATA, "hello_truncate")
    row = await db_get_one(DatabaseUserContext.DATA, "hello_count")
    assert row[0] == 0


async def test_hello_insert_one(db_execute_one, db_get_one):
    values = {"bv1": "abc", "bv2": 123}
    await db_execute_one(DatabaseUserContext.DATA, "hello_insert", values)
    row = await db_get_one(DatabaseUserContext.DATA, "hello_count")
    assert row[0] == 1


async def test_hello_insert_many(db_put_many, db_get_one):
    values = [
        {"bv1": "def", "bv2": 456},
        {"bv1": "ghi", "bv2": 789},
    ]
    await db_put_many(DatabaseUserContext.DATA, "hello_insert", values)
    row = await db_get_one(DatabaseUserContext.DATA, "hello_count")
    assert row[0] == 3


async def test_hello_select(db_get_one):
    values = {"bv1": "abc"}
    row = await db_get_one(DatabaseUserContext.DATA, "hello_select", values)
    assert row == ("abc", 123)


async def test_hello_select_many(db_get_many):
    result = await db_get_many(DatabaseUserContext.DATA, "hello_select_many")
    rows = [tuple(row.values()) for row in result]
    assert rows == [("abc", 123), ("def", 456), ("ghi", 789)]


async def test_hello_update(db_execute_one, db_get_one):
    values1 = {"bv1": "abc", "bv2": -99}
    await db_execute_one(DatabaseUserContext.DATA, "hello_update", values1)
    values2 = {"bv1": "abc"}
    row = await db_get_one(DatabaseUserContext.DATA, "hello_select", values2)
    assert row == ("abc", -99)
