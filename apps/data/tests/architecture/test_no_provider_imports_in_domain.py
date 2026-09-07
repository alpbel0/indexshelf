import ast

from architecture.rules import (
    PROVIDER_MODULES,
    SOURCE_ROOT,
    imported_modules,
    provider_imports,
    source_files,
)


def test_domain_and_application_do_not_import_providers() -> None:
    violations = {
        f"{path}:{sorted(imports)}"
        for path in source_files()
        if path.relative_to(SOURCE_ROOT).parts[0] in {"domain", "application"}
        and (imports := provider_imports(path))
    }
    assert not violations


def test_provider_import_fixture_is_rejected() -> None:
    modules = imported_modules(ast.parse("import scrapling.fetchers"))
    assert modules[0].split(".")[0] in PROVIDER_MODULES
