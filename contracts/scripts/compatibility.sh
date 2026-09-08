#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
npm test
uv run pytest tests/test_jsonschema_examples.py tests/test_event_sequence_contract.py tests/test_forward_compatibility.py tests/test_no_sensitive_fields.py tests/test_codegen_smoke.py
