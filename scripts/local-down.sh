#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
volume_flag=""
if [ "${1:-}" = "--volumes" ] || [ "${1:-}" = "-v" ]; then volume_flag="--volumes"; fi
docker compose --project-directory "$root/local" -f "$root/local/compose.yaml" -f "$root/local/compose.services.yaml" down --remove-orphans $volume_flag
