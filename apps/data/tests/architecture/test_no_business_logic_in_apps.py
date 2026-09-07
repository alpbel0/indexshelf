from architecture.rules import SOURCE_ROOT, has_pipeline_branch


def test_app_entrypoints_do_not_select_processing_pipeline() -> None:
    apps_root = SOURCE_ROOT / "apps"
    violations = {
        str(path)
        for path in apps_root.glob("*.py")
        if has_pipeline_branch(path.read_text(encoding="utf-8"))
    }
    assert not violations


def test_pipeline_branch_fixture_is_rejected() -> None:
    assert has_pipeline_branch("if job.status == 'ready':\n    route_to_pipeline()")
