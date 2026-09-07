def main() -> int:
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    config = Config(str(Path(__file__).parents[3] / "alembic.ini"))
    try:
        command.upgrade(config, "head")
    except Exception:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
