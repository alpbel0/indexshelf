import json
from pathlib import Path

ROOT = Path(__file__).parents[3]


def test_rabbitmq_definitions_are_isolated_and_durable() -> None:
    definitions = json.loads((ROOT / "local/rabbitmq/definitions.json").read_text(encoding="utf-8"))
    assert {item["name"] for item in definitions["vhosts"]} == {"/indexshelf"}
    assert all(item["durable"] for item in definitions["exchanges"] + definitions["queues"])
    assert {item["vhost"] for item in definitions["permissions"]} == {"/indexshelf"}


def test_local_configuration_has_no_real_provider_credentials() -> None:
    env_example = (ROOT / "local/.env.example").read_text(encoding="utf-8")
    assert "dummy" in env_example
    assert "sk-" not in env_example
    assert "AIza" not in env_example

    compose = (ROOT / "local/compose.yaml").read_text(encoding="utf-8")
    assert ":-55433}:5432" in compose
    assert "5432:5432" not in compose


def test_minio_lifecycle_is_private_and_bounded() -> None:
    lifecycle = json.loads((ROOT / "local/minio/lifecycle.json").read_text(encoding="utf-8"))
    assert {rule["Expiration"]["Days"] for rule in lifecycle["Rules"]} == {1, 7}
    assert "anonymous set none" in (ROOT / "local/minio/create-buckets.sh").read_text(encoding="utf-8")
