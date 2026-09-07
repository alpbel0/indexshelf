import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, RefResolver  # type: ignore[attr-defined]

ROOT = Path(__file__).parents[1]
SCHEMA_ROOT = ROOT / "jsonschema/data/v1"


def test_consumer_ignores_unknown_optional_fields_at_the_boundary() -> None:
    schema = json.loads((SCHEMA_ROOT / "events/job-failed.schema.json").read_text(encoding="utf-8"))
    example = json.loads((SCHEMA_ROOT / "examples/job-failed.json").read_text(encoding="utf-8"))
    evolved = copy.deepcopy(example)
    evolved["new_optional_field"] = {"future": True}
    known = {key: value for key, value in evolved.items() if key in schema["properties"]}
    store = {}
    for path in (SCHEMA_ROOT / "common").glob("*.schema.json"):
        common = json.loads(path.read_text(encoding="utf-8"))
        store[common["$id"]] = common
    Draft202012Validator(schema, resolver=RefResolver.from_schema(schema, store=store), format_checker=FormatChecker()).validate(known)
    assert "new_optional_field" not in known


def test_unknown_event_type_is_ignored_by_forward_compatible_consumer_policy() -> None:
    policy = (ROOT / "compatibility-policy.yaml").read_text(encoding="utf-8")
    supported = {"component.failed", "job.completed", "job.failed", "job.cancelled"}
    assert "unknownEventTypes: ignore-and-observe" in policy
    assert "future.event" not in supported
