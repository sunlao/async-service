from uuid import uuid4
from time import sleep
from src.helpers.db.models import DatabaseUserContext
from tests.fixtures.fixtures_db import db_execute_one, db_get_one
from tests.fixtures.fixtures_jobs import hello_job


async def test_hello(hello_job, db_execute_one, db_get_one):
    id = str(uuid4())
    empty_ctx = {}
    response = await hello_job(id).execute(empty_ctx)
    assert response["status_code"] == 0
    assert response["message"] == "complete"
    assert response["function"] == "Hello.execute"
    sleep(2)
    # This is ONLY testing the manual execution of the hello job
    # Sleeping is not a best practice for async testing of a platform/service
    print("\n\n** Sleep 2 second to let db and job get in sync\n\n")
    values = {"bv1": id}
    response = await db_get_one(DatabaseUserContext.DATA, "hello_get_job", values)
    assert response[0] == id
    # delete job that isn't ran through redis
    await db_execute_one(DatabaseUserContext.DATA, "hello_delete_job", values)
    response = await db_get_one(DatabaseUserContext.DATA, "hello_get_job", values)
    assert response == tuple
