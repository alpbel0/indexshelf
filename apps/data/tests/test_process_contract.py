from pytest import MonkeyPatch

from indexshelf_data.apps.migrate import main
from indexshelf_data.apps.worker_profile import DEFAULT_WORKER_PROFILE


def test_migration_entrypoint_does_not_report_fake_success(monkeypatch: MonkeyPatch) -> None:
    def fail(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr("alembic.command.upgrade", fail)
    assert main() == 2


def test_bootstrap_worker_profile_is_explicit() -> None:
    assert DEFAULT_WORKER_PROFILE.name == "bootstrap"
    assert DEFAULT_WORKER_PROFILE.enabled is True
