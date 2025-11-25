FROM flyway/flyway:11.11-alpine

USER root
RUN apk add --update python3 py3-pip postgresql jq
COPY deploy/db-deploy/sql /ops/sql
COPY deploy/db-deploy/deploy.sh /ops/deploy.sh

ENTRYPOINT [ "/ops/deploy.sh" ]