$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    uv run pytest
} finally {
    Pop-Location
}
