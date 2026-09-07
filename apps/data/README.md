# Data

The Data area targets Python 3.12 and uses separate process entrypoints for
the worker, outbox relay, migration command, and health API. This task creates
only lifecycle and wiring foundations; extraction and provider pipelines arrive
in later phases.

```text
uv sync --locked
uv run ruff check .
uv run mypy
uv run pytest
```

Build local Data profiles from the repository root:

```text
docker buildx bake --allow=fs.read=C:\Users -f apps/data/build/docker-bake.hcl
```

The headless browser profile is the default browser runtime. Headful is local-debug only; browser
profiles remain non-root and do not disable Chromium's sandbox.
