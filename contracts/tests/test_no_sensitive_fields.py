import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, RefResolver  # type: ignore[attr-defined]

ROOT = Path(__file__).parents[1]
SCHEMA_ROOT = ROOT / "jsonschema/data/v1"


def validator_for(name: str) -> Draft202012Validator:
    schema = json.loads(next(SCHEMA_ROOT.rglob(name)).read_text(encoding="utf-8"))
    store = {}
    for path in (SCHEMA_ROOT / "common").glob("*.schema.json"):
        common = json.loads(path.read_text(encoding="utf-8"))
        store[common["$id"]] = common
    return Draft202012Validator(schema, resolver=RefResolver.from_schema(schema, store=store), format_checker=FormatChecker())


def test_allowed_event_has_no_raw_secret_fields() -> None:
    example = json.loads((ROOT / "tests/fixtures/data-sensitive-allowed.json").read_text(encoding="utf-8"))
    validator_for("job-failed.schema.json").validate(example)
    serialized = json.dumps(example).lower()
    assert not any(marker in serialized for marker in ("password", "cookie", "proxy_credential", "api_key"))


def test_sensitive_or_unknown_error_code_is_rejected() -> None:
    example = json.loads((ROOT / "tests/fixtures/data-sensitive-invalid.json").read_text(encoding="utf-8"))
    with pytest.raises(Exception):
        validator_for("job-failed.schema.json").validate(example)
