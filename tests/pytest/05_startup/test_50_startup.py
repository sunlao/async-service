from asyncio import timeout, sleep
from asyncpg.exceptions import UndefinedTableError


async def test_sql(db_get_one):
    sqls = [
        "hello_job_cnt",
        "natal_cities_cnt",
        "natal_iso_country_cnt",
        "natal_iso_subdivision_cnt",
        "natal_location_cnt",
        "natal_admin1_cnt",
        "natal_admin2_cnt",
    ]
    for sql in sqls:
        cnt = 0
        async with timeout(300):
            while cnt == 0:
                try:
                    row = await db_get_one(sql)
                    cnt = row[0]
                except UndefinedTableError:
                    await sleep(30)
                except TypeError:
                    await sleep(30)
        assert cnt >= 1
