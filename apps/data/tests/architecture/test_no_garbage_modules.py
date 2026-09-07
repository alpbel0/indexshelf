from architecture.rules import SOURCE_ROOT


def test_generic_utility_modules_are_not_allowed() -> None:
    forbidden = {"utils", "helpers", "misc"}
    violations = {
        str(path)
        for path in SOURCE_ROOT.rglob("*")
        if path.name.casefold().removesuffix(".py") in forbidden
    }
    assert not violations


def test_generic_utility_module_fixture_is_rejected() -> None:
    assert "utils" in {"utils", "helpers", "misc"}
