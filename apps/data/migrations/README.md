# Data migrations

Alembic migrations for the Data persistence schema live in `versions/`. The
current baseline migration creates the job execution, extraction attempt, and
event outbox tables.

The Data bootstrap process intentionally does not apply migrations. Run the
dedicated migration entrypoint with the target database configuration before
starting Data processes.
