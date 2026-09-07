#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
docker compose --project-directory "$root/local" -f "$root/local/compose.yaml" -f "$root/local/compose.services.yaml" up -d --wait
