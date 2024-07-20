from os import getenv
from time import time
from arq import create_pool
from arq.connections import RedisSettings
from arq import cron
from src.helpers.worker.models import JobExecution, JobSubmit
from src.jobs.hello import Hello


def settings():
    return RedisSettings(
        host=getenv("REDIS_HOST", "localhost"),
        port=int(getenv("REDIS_PORT", "6379")),
    )


# pylint: disable=unused-argument
async def hello_job(ctx, **kwarg):
    return await Hello(ctx["job_id"]).execute(ctx, **kwarg)


# pylint: disable=protected-access
async def info_job(p_uuid):
    pool = await create_pool(settings())
    key = bytes(f"arq:result:{p_uuid}", encoding="utf-8")
    return await pool._get_job_result(key)


async def info_jobs():
    pool = await create_pool(settings())
    return await pool.all_job_results()


# using _job_id as below enforces the client to submit a unique job_execution.id one
# and only one time. The api will return a 409 when an id is already submitted
async def job_submit(job_execution: JobExecution) -> JobSubmit:
    pool = await create_pool(settings())
    if job_execution.input_params is None:
        job = await pool.enqueue_job(
            job_execution.function,
            _job_id=str(job_execution.id),
        )
    else:
        job = await pool.enqueue_job(
            job_execution.function,
            _job_id=str(job_execution.id),
            **job_execution.input_params,
        )
    if job is None:
        return {
            "status": f"Job Id: {job_execution.id} already submitted",
            "job_info": None,
            "job_id": None,
        }
    return {
        "status": await job.status(),
        "job_info": await job.info(),
        "job_id": job.job_id,
    }


class WorkerSettings:
    functions = [hello_job]
    cron_jobs = [cron(hello_job, second=10)]
    keep_result = 14400
    health_check_interval = 1
    redis_settings = settings()
