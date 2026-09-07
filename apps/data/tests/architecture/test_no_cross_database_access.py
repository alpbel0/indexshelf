import tempfile
from pathlib import Path

from architecture.rules import database_violations, source_files


def test_data_source_does_not_use_product_database_access() -> None:
    violations = {
        f"{path}:{sorted(imports)}"
        for path in source_files()
        if (imports := database_violations(path))
    }
    assert not violations


def test_product_database_fixture_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "fixture.py"
        path.write_text("PRODUCT_DATABASE_URL = 'postgres://example'", encoding="utf-8")
        assert database_violations(path) == {"PRODUCT_DATABASE_URL"}
