#!/bin/bash

## Prepare front environment
while read ENV_VAR; do
  export $ENV_VAR > /dev/null
done < .env
envsubst \
  -no-unset -no-empty \
  -i front/.env.production.template \
  -o front/.env.production


docker compose down
git pull origin develop
docker compose up --build -d
