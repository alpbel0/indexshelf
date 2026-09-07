import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, RefResolver  # type: ignore[attr-defined]

ROOT = Path(__file__).parents[1]
SCHEMA_ROOT = ROOT / "jsonschema/data/v1"


def test_partial_completion_preserves_component_outcomes() -> None:
    schema = json.loads((SCHEMA_ROOT / "events/job-completed.schema.json").read_text(encoding="utf-8"))
    example = json.loads((SCHEMA_ROOT / "examples/job-completed.json").read_text(encoding="utf-8"))
    store = {}
    for path in (SCHEMA_ROOT / "common").glob("*.schema.json"):
        common = json.loads(path.read_text(encoding="utf-8"))
        store[common["$id"]] = common
    resolver = RefResolver.from_schema(schema, store=store)
    Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker()).validate(example)
    components = {item["name"]: item["status"] for item in example["payload"]["components"]}
    assert components == {"metadata": "completed", "static": "failed", "media": "skipped"}
    assert example["payload"]["partial"] is True


def test_message_lineage_is_monotonic_across_example_sequence() -> None:
    examples = [
        "component-failed.json",
        "job-completed.json",
    ]
    messages = [json.loads((SCHEMA_ROOT / "examples" / name).read_text(encoding="utf-8")) for name in examples]
    assert messages[0]["correlation_id"] == messages[1]["correlation_id"]
    assert messages[0]["message_id"] == messages[1]["causation_id"]
    assert all(message["message_version"] == 1 for message in messages)


def test_cancellation_is_a_separate_terminal_flow() -> None:
    command = json.loads((SCHEMA_ROOT / "examples/cancel-job.json").read_text(encoding="utf-8"))
    cancelled = json.loads((SCHEMA_ROOT / "examples/job-cancelled.json").read_text(encoding="utf-8"))
    assert command["message_id"] == cancelled["causation_id"]
    assert command["correlation_id"] == cancelled["correlation_id"]
    assert cancelled["message_type"] == "job.cancelled"
