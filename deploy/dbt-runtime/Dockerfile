FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY VERSION /app/VERSION
COPY deploy/sitecustomize.py /app/src/sitecustomize.py
RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq-dev python3-dev
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends git

RUN pip install --upgrade pip
COPY ./deploy/dbt-runtime/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./deploy/dbt-runtime/profiles.yml /opt/dbt/profiles.yml

RUN echo $
RUN touch /tmp/healthy
