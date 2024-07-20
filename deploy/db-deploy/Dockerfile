FROM flyway/flyway:10.11.0-alpine

USER root
RUN apk add --update python3 py3-pip postgresql jq
RUN pip3 install --upgrade pip
COPY deploy/db-deploy/sql /ops/sql
COPY deploy/db-deploy/deploy.sh /ops/deploy.sh

ENTRYPOINT [ "/ops/deploy.sh" ]