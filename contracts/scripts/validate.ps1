$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    npm run validate
    & (Join-Path $PSScriptRoot 'validate-data-contracts.ps1')
    & (Join-Path $PSScriptRoot 'compatibility.ps1')
} finally {
    Pop-Location
}
