import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, RefResolver  # type: ignore[attr-defined]

ROOT = Path(__file__).parents[1]
SCHEMA_ROOT = ROOT / "jsonschema/data/v1"


def load_schemas() -> dict[str, dict]:
    schemas = {}
    for path in SCHEMA_ROOT.rglob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[schema["$id"]] = schema
    return schemas


def validate_example(schema_name: str, example_name: str) -> None:
    schemas = load_schemas()
    schema_path = next(SCHEMA_ROOT.rglob(schema_name))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads((SCHEMA_ROOT / "examples" / example_name).read_text(encoding="utf-8"))
    resolver = RefResolver.from_schema(schema, store=schemas)
    Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker()).validate(example)


def test_all_positive_examples_validate() -> None:
    pairs = [
        ("cancel-job.schema.json", "cancel-job.json"),
        ("component-failed.schema.json", "component-failed.json"),
        ("job-completed.schema.json", "job-completed.json"),
        ("job-failed.schema.json", "job-failed.json"),
        ("job-cancelled.schema.json", "job-cancelled.json"),
    ]
    for schema_name, example_name in pairs:
        validate_example(schema_name, example_name)
