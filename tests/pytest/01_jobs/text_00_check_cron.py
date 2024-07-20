from time import sleep
from tests.fixtures.fixtures_db import db_get_one, data_context


# run last because the first cron job takes about a minute or so to complete.
async def test_cron_ran(db_get_one, data_context):
    count = 0
    row = await db_get_one(data_context.DATA, "hello_cron_count")
    while row[0] == 0 and count < 90:
        sleep(1)
        count += 1
        row = await db_get_one(data_context.DATA, "hello_cron_count")
    assert row[0] > 0
