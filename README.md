![CodeFormat](docs/code_coverage/black.svg)
![pylint](docs/code_coverage/pylint.svg)
![CodeStyle](docs/code_coverage/CodeStyle.svg)
![Coverage](docs/code_coverage/coverage.svg)
![Bandit](docs/code_coverage/bandit.svg)
![Safety](docs/code_coverage/safety.svg)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.3-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)

## What it does

A pythonic template repo for API based services that needs async workers for non blocking jobs. 

## Features

- Async FastAPI backend with PostgreSQL + Redis
- Automatic user setup from minimal  info
- Cached transit queries for fast response times
- API endpoints optimized for LLM consumption

---

![Chat](docs/engineering/Chat.svg)

---

## Prerequisites

Review the [Getting Started](https://github.com/sunlao/_chat/wiki/Getting-Started) for more info for Mac setup and virtual environment details.

Locally this repo uses the following environment variables in a `.env` file:

```text
APP_CODE=aserv
ENV=dev
API_PORT=80
API_PUB_PORT=8080
API_STATIC_DIR=/app/src/api/static
DB_PORT=5432
DB_PUB_PORT=5431
DB_MAX_POOL_API=5
DB_MAX_POOL_QUIESCE: 3
DB_MAX_POOL_WORKER=10
DB_ADMIN_USER=${APP_CODE}_admin
DB_ADMIN_PWD={manually replace with secret}
DB_DATA_PWD={manually replace with secret}
DB_APP_PWD={manually replace with secret}
REDIS_PORT=6379
REDIS_PUB_PORT=6378
DBT_API_PORT=81
DBT_API_PUB_PORT=8081
XFORM_DIR=/app/src/xform
DBT_PROF_DIR=/opt/dbt
XFORM_RUNS_DIR=/data/xform_runs
START_UP=true
JOB_PATH=/app
JOB_VERSION={manually replace with job config version i.e. 1.1.1}
GATE_CLOSE_PATH=/app/gate/.gate.close
```

Note: we do not store passwords in repos so `.env` files are in the `.gitignore` file

## Local Development

```SHELL
make up
```

```SHELL
docker ps 
```

### Deploys the following containers

- aserv-api
- aserv-db-deploy
- aserv-redis
- aserv-postgres
- aserv-worker
- aserv-dbt (with api endpoints)

Note: aserv-db-deploy terminates when db deploy is finished. Check logs with:

```SHELL
docker logs aserv-db-deploy 
```

Manually assert API's via insomnia.  Import yaml from `/docs/insomnia.yaml`.

Destroy the above running containers with:

```SHELL
make down
```

## Testing

See [Testing](https://github.com/sunlao/_chat/wiki/Testing) for more info.

Execute tests

```SHELL
make test
```

## API docs

- FastAPI dynamically generate docs using [OpenAPI Specifications](https://swagger.io/specification/)
- During local development use:
  - `http://localhost:8080/redoc`  new version for Chat API
  - `http://localhost:8080/docs`  "classic" version for Chat API
  - `http://localhost:8081/redoc`  new version for dbt API
  - `http://localhost:8081/docs`  "classic" version for dbt API

## Logs

Structured logs are written to `\logs` for each service

- api
- dbt
- worker

Note: tox will create a test service

## Data

during local development, docker compose maps data files to `/data` for

- read: files that have been unzipped
- xform_runs: dbt run information
- zip: down loaded zipped files

## Convieance Script

`/scripts/reset.py` removes ephemeral artifacts for a clean startup.
