#!/bin/bash

sleep 3
echo "--sleeping 3 seconds till db-deploy is done"

CONTAINER_ID="notset"
until [[ $CONTAINER_ID == "" ]]; do
    CONTAINER_ID=$(echo $CONTAINER_ID | docker ps -q -f name=aserv-db-deploy)
    if [[ $CONTAINER_ID != "" ]]; then
        sleep 3
        echo "--sleeping 3 seconds till db-deploy is done"
    fi
done