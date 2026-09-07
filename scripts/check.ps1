$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-CheckStep([string]$Name, [scriptblock]$Action) {
    Write-Host "==> $Name"
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "Check failed: $Name (exit code $LASTEXITCODE)"
    }
}

function Invoke-Native([scriptblock]$Action) {
    & $Action
    if ($LASTEXITCODE -ne 0) {
        $code = $LASTEXITCODE
        throw "Command failed with exit code $code"
    }
}

$root = Split-Path -Parent $PSScriptRoot

Invoke-CheckStep 'Backend restore/build/test' {
    Push-Location "$root\apps\backend"
    try {
        Invoke-Native { dotnet restore IndexShelf.Backend.slnx }
        Invoke-Native { dotnet build IndexShelf.Backend.slnx --no-restore --configuration Release }
        Invoke-Native { dotnet test IndexShelf.Backend.slnx --no-build --configuration Release }
    } finally { Pop-Location }
}

Invoke-CheckStep 'Data sync/lint/type/test' {
    Push-Location "$root\apps\data"
    try {
        Invoke-Native { uv sync --frozen }
        Invoke-Native { uv run ruff check . }
        Invoke-Native { uv run mypy }
        Invoke-Native { uv run pytest }
    } finally { Pop-Location }
}

Invoke-CheckStep 'Android assemble/lint/test/quality' {
    Push-Location "$root\apps\android"
    try {
        if (!(Test-Path -LiteralPath 'gradlew.bat')) { throw 'Android Gradle wrapper is missing.' }
        Invoke-Native { cmd /c gradlew.bat --no-daemon assembleDebug lint detekt spotlessCheck test }
    } finally { Pop-Location }
}

Invoke-CheckStep 'Contract validation' {
    $validator = "$root\contracts\scripts\validate.ps1"
    if (!(Test-Path -LiteralPath $validator)) {
        throw 'Contract validation prerequisite is missing: contracts/scripts/validate.ps1'
    }
    Invoke-Native { pwsh -NoProfile -File $validator }
}

Write-Host 'All checks passed.'
