param([switch]$Volumes)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$local = Join-Path $root 'local'
$volumeFlag = if ($Volumes) { @('--volumes') } else { @() }
docker compose --project-directory $local -f (Join-Path $local 'compose.yaml') -f (Join-Path $local 'compose.services.yaml') down --remove-orphans @volumeFlag
