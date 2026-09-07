$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$local = Join-Path $root 'local'
docker compose --project-directory $local -f (Join-Path $local 'compose.yaml') -f (Join-Path $local 'compose.services.yaml') up -d --wait
