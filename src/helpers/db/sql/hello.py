class Hello:
    hello_count = "select count(*) from aserv.hello_world"

    hello_cron_count = "select count(*) from aserv.hello_job where job_id like 'cron:%'"

    hello_delete_job = "delete from aserv.hello_job where job_id = :bv1"

    hello_insert = "INSERT INTO aserv.hello_world(col1, col2) VALUES (:bv1, :bv2)"

    hello_get_job = """
SELECT job_id, execution_time
FROM
aserv.hello_job
where
job_id = :bv1
    """

    hello_insert_job = """
INSERT INTO aserv.hello_job(job_id, execution_time)
VALUES (:bv1, :bv2)
    """

    hello_postgres = "select 'hello_postgres'"

    hello_select = "select * from aserv.hello_world where col1 = :bv1"

    hello_select_many = "select * from aserv.hello_world order by col1"

    hello_single_job = """
select job_id from aserv.hello_job where job_id not like 'cron:%' limit 1
"""

    hello_truncate = "truncate table aserv.hello_world"

    hello_update = """
update aserv.hello_world
set
col2 = :bv2
where
col1 = :bv1
"""

    def get(self, p_name: str) -> str:
        return getattr(self, p_name)
