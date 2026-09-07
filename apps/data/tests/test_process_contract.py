from indexshelf_data.apps.migrate import main
from indexshelf_data.apps.worker_profile import DEFAULT_WORKER_PROFILE


def test_migration_entrypoint_does_not_report_fake_success() -> None:
    assert main() == 2


def test_bootstrap_worker_profile_is_explicit() -> None:
    assert DEFAULT_WORKER_PROFILE.name == "bootstrap"
    assert DEFAULT_WORKER_PROFILE.enabled is True
