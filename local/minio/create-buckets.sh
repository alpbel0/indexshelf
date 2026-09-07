#!/usr/bin/env sh
set -eu
mc alias set local "${MINIO_ENDPOINT:-http://minio:9000}" "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"
mc mb --ignore-existing local/indexshelf-temporary
mc mb --ignore-existing local/indexshelf-durable
mc anonymous set none local/indexshelf-temporary
mc anonymous set none local/indexshelf-durable
mc ilm import local/indexshelf-temporary < /config/lifecycle.json
mc ilm import local/indexshelf-durable < /config/lifecycle.json
mc admin user add local "${MINIO_DATA_USER}" "${MINIO_DATA_PASSWORD}" || true
mc admin policy create local indexshelf-data /config/data-policy.json || true
mc admin policy attach local indexshelf-data --user "${MINIO_DATA_USER}"
