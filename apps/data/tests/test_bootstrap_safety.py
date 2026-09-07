import json
import logging

import pytest

from indexshelf_data.bootstrap.logging import RedactingFormatter
from indexshelf_data.bootstrap.settings import DataSettings


def test_missing_secret_reference_fails_fast() -> None:
    with pytest.raises(ValueError, match="secret_reference"):
        DataSettings(secret_reference="missing-secret-file")


def test_non_local_environment_requires_a_secret_reference() -> None:
    with pytest.raises(ValueError, match="secret_reference"):
        DataSettings(environment="production")


def test_unknown_environment_fails_fast() -> None:
    with pytest.raises(ValueError, match="environment"):
        DataSettings(environment="unknown")


def test_sensitive_log_values_are_redacted() -> None:
    record = logging.LogRecord("test", logging.INFO, "", 0, "token=abc123", (), None)

    output = RedactingFormatter("%(message)s").format(record)
    assert json.loads(output)["message"] == "token=[REDACTED]"
