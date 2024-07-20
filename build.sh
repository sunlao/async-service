#!/bin/bash

if [ -f ".env" ]; then
    source .env
fi

echo "app code: [$APP_CODE]"

# launch app services
docker-compose -f docker-compose.yml up --build --remove-orphans --detach api db-deploy postgres redis worker
./deploy/db-deploy/wait.sh

echo "Local Environment UP"
