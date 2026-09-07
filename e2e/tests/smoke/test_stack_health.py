import os
import json
import subprocess
from urllib.error import HTTPError
from urllib.request import urlopen
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
COMPOSE = [
    "docker",
    "compose",
    "--project-directory",
    str(ROOT / "local"),
    "-f",
    str(ROOT / "local/compose.yaml"),
    "-f",
    str(ROOT / "local/compose.services.yaml"),
]


def compose(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*COMPOSE, *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_compose_configuration_is_valid_and_scoped() -> None:
    result = compose("config", "--quiet")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "indexshelf-local" in compose("config").stdout


@pytest.mark.skipif(
    os.getenv("INDEXSHELF_RUN_STACK_SMOKE") != "1",
    reason="set INDEXSHELF_RUN_STACK_SMOKE=1 after local-up to run live stack checks",
)
def test_dependency_services_are_healthy() -> None:
    result = compose("ps", "--format", "json")
    assert result.returncode == 0, result.stdout + result.stderr
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    services = {row.get("Service"): row for row in rows}
    for service in ("postgres", "rabbitmq", "valkey", "minio", "wiremock", "mailpit"):
        assert services[service]["State"] == "running"
        assert services[service].get("Health") in (None, "healthy")


@pytest.mark.skipif(
    os.getenv("INDEXSHELF_RUN_STACK_SMOKE") != "1",
    reason="set INDEXSHELF_RUN_STACK_SMOKE=1 after local-up to run live stack checks",
)
def test_wrong_database_credentials_are_rejected() -> None:
    product_with_data_password = compose(
        "exec",
        "-T",
        "-e",
        "PGPASSWORD=indexshelf_data_runtime_dummy",
        "postgres",
        "psql",
        "-h",
        "127.0.0.1",
        "-U",
        "indexshelf_data_runtime",
        "-d",
        "indexshelf",
        "-c",
        "select 1",
        check=False,
    )
    data_with_backend_password = compose(
        "exec",
        "-T",
        "-e",
        "PGPASSWORD=indexshelf_backend_runtime_dummy",
        "postgres",
        "psql",
        "-h",
        "127.0.0.1",
        "-U",
        "indexshelf_backend_runtime",
        "-d",
        "indexshelf_data",
        "-c",
        "select 1",
        check=False,
    )
    assert product_with_data_password.returncode != 0
    assert data_with_backend_password.returncode != 0


@pytest.mark.skipif(
    os.getenv("INDEXSHELF_RUN_STACK_SMOKE") != "1",
    reason="set INDEXSHELF_RUN_STACK_SMOKE=1 after local-up to run live stack checks",
)
def test_wrong_rabbitmq_and_object_storage_credentials_are_rejected() -> None:
    rabbit = compose(
        "exec", "-T", "rabbitmq", "rabbitmqctl", "authenticate_user",
        "indexshelf_backend", "wrong-password", check=False,
    )
    assert rabbit.returncode != 0

    with pytest.raises(HTTPError) as response:
        urlopen("http://127.0.0.1:59010/indexshelf-temporary", timeout=5)
    assert response.value.code in (401, 403)
