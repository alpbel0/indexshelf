import os
import json
import subprocess
import time
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


@pytest.mark.skipif(
    os.getenv("INDEXSHELF_RUN_MIGRATOR_SMOKE") != "1",
    reason="set INDEXSHELF_RUN_MIGRATOR_SMOKE=1 with the local PostgreSQL stack",
)
def test_backend_migrator_creates_empty_baseline_database() -> None:
    database = f"indexshelf_migrator_smoke_{int(time.time())}"
    create = compose(
        "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", "postgres",
        "-v", "ON_ERROR_STOP=1", "-c", f"CREATE DATABASE {database};",
    )
    assert create.returncode == 0, create.stdout + create.stderr
    grant = compose(
        "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", "postgres",
        "-v", "ON_ERROR_STOP=1", "-c",
        f"GRANT CONNECT, CREATE ON DATABASE {database} TO indexshelf_product_migrator;",
    )
    assert grant.returncode == 0, grant.stdout + grant.stderr
    schema_grant = compose(
        "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", database,
        "-v", "ON_ERROR_STOP=1", "-c",
        "GRANT USAGE, CREATE ON SCHEMA public TO indexshelf_product_migrator;",
    )
    assert schema_grant.returncode == 0, schema_grant.stdout + schema_grant.stderr
    try:
        environment = os.environ.copy()
        environment["INDEXSHELF_MIGRATOR_CONNECTION"] = (
            f"Host=localhost;Port=55433;Database={database};"
            "Username=indexshelf_product_migrator;Password=indexshelf_product_migrator_dummy"
        )
        result = subprocess.run(
            [
                "dotnet", "run", "--project",
                str(ROOT / "apps/backend/src/Hosts/IndexShelf.DbMigrator"),
                "--configuration", "Release", "--no-restore",
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=180,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        tables = compose(
            "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", database,
            "-At", "-c", "SELECT count(*) FROM pg_tables WHERE schemaname='operations';",
        )
        assert tables.stdout.strip() == "7", tables.stdout + tables.stderr
    finally:
        compose(
            "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", "postgres",
            "-c", f"DROP DATABASE IF EXISTS {database};", check=False,
        )


@pytest.mark.skipif(
    os.getenv("INDEXSHELF_RUN_BACKEND_SCHEMA_SMOKE") != "1",
    reason="set INDEXSHELF_RUN_BACKEND_SCHEMA_SMOKE=1 after running DbMigrator",
)
def test_operations_schema_constraints_and_indexes_exist() -> None:
    query = compose(
        "exec", "-T", "postgres", "psql", "-U", "postgres", "-d", "indexshelf", "-At", "-c",
        "SELECT (SELECT count(*) FROM information_schema.columns WHERE table_schema='operations' AND table_name='jobs' AND column_name IN ('source_type','contract_version','lease_token','correlation_id','purge_after')) || ':' || (SELECT count(*) FROM pg_indexes WHERE schemaname='operations' AND indexname IN ('ux_job_attempts_execution_id','ux_inbox_consumer_event','ux_inbox_consumer_job_sequence','ix_jobs_scheduler','ix_outbox_dispatch','ix_inbox_process')) || ':' || (SELECT count(*) FROM pg_constraint WHERE connamespace='operations'::regnamespace AND conname IN ('ck_jobs_attempts','ck_jobs_contract_version','ck_job_attempts_number','ck_outbox_payload_hash','ck_inbox_payload_hash'));",
    )
    assert query.stdout.strip() == "5:6:5", query.stdout + query.stderr
