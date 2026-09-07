import ast

from architecture.rules import (
    imported_modules,
    layer_dependencies,
    layer_dependencies_for_modules,
    source_files,
)


def test_data_layers_only_depend_inward() -> None:
    violations = {
        f"{path}:{sorted(dependencies)}"
        for path in source_files()
        if (dependencies := layer_dependencies(path))
    }
    assert not violations


def test_layer_direction_negative_fixture() -> None:
    fixture = ast.parse("from indexshelf_data.apps import runner")
    imports = imported_modules(fixture)
    assert layer_dependencies_for_modules("domain", imports) == {"apps"}
