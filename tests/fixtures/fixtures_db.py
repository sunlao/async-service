from pytest import fixture
from src.helpers.db.models import DatabaseUserContext
from src.helpers.db import get_one, get_many, execute_one, put_many


@fixture
def db_execute_one():
    return execute_one


@fixture
def db_get_one():
    return get_one


@fixture
def db_get_many():
    return get_many


@fixture
def db_put_many():
    return put_many


@fixture
def data_context():
    return DatabaseUserContext


@fixture
async def db_hello_insert_many() -> tuple:
    values = [
        {"bv1": "def", "bv2": 456},
        {"bv1": "ghi", "bv2": 789},
    ]
    return await put_many(DatabaseUserContext.DATA, "hello_insert", values)
