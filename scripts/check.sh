#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

run_step() {
  local name="$1"
  shift
  printf '==> %s\n' "$name"
  "$@"
}

run_backend() {
  pushd "$ROOT/apps/backend" >/dev/null
  dotnet restore IndexShelf.Backend.slnx
  dotnet build IndexShelf.Backend.slnx --no-restore --configuration Release
  dotnet test tests/Architecture/IndexShelf.ArchitectureTests/IndexShelf.ArchitectureTests.csproj --no-build --configuration Release
  popd >/dev/null
}

run_data() {
  pushd "$ROOT/apps/data" >/dev/null
  uv sync --frozen
  uv run ruff check .
  uv run mypy
  uv run pytest
  popd >/dev/null
}

run_android() {
  pushd "$ROOT/apps/android" >/dev/null
  [[ -x ./gradlew ]] || { echo 'Android Gradle wrapper is missing.' >&2; return 1; }
  ./gradlew --no-daemon assembleDebug lint detekt spotlessCheck test
  popd >/dev/null
}

run_contracts() {
  local validator="$ROOT/contracts/scripts/validate.sh"
  [[ -x "$validator" ]] || {
    echo "Contract validation prerequisite is missing: contracts/scripts/validate.sh" >&2
    return 1
  }
  "$validator"
}

run_local_definitions() {
  uv run --project "$ROOT/contracts" pytest "$ROOT/e2e/tests/smoke/test_local_dependency_definitions.py" "$ROOT/e2e/tests/smoke/test_stack_health.py"
}

run_step 'Backend restore/build/test' run_backend
run_step 'Data sync/lint/type/test' run_data
run_step 'Android assemble/lint/test/quality' run_android
run_step 'Contract validation' run_contracts
run_step 'Local dependency definition smoke' run_local_definitions
printf 'All checks passed.\n'
