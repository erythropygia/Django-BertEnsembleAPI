#!/usr/bin/bash

### CONFIG ###
CONTAINER_NAME="cer-nlp"
DOCKER_FILE="docker-compose.yml"

docker-compose stop
docker-compose -f ${DOCKER_FILE} rm --force
docker-compose -f ${DOCKER_FILE} build
docker-compose -f ${DOCKER_FILE} up -d --remove-orphans
docker exec -it ${CONTAINER_NAME} /bin/bash

