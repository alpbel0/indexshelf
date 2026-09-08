using IndexShelf.Persistence.Context;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

namespace IndexShelf.Persistence.Migrations;

[DbContext(typeof(IndexShelfDbContext))]
[Migration("202609080003_OperationsSchemaParity")]
public sealed class OperationsSchemaParity : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            ALTER TABLE operations.jobs
                ADD COLUMN IF NOT EXISTS source_type text NOT NULL DEFAULT 'unknown',
                ADD COLUMN IF NOT EXISTS source_id uuid,
                ADD COLUMN IF NOT EXISTS source_revision bigint,
                ADD COLUMN IF NOT EXISTS contract_version smallint NOT NULL DEFAULT 1,
                ADD COLUMN IF NOT EXISTS priority smallint NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS current_attempt_number integer,
                ADD COLUMN IF NOT EXISTS lease_token uuid,
                ADD COLUMN IF NOT EXISTS lease_expires_at timestamptz,
                ADD COLUMN IF NOT EXISTS last_heartbeat_at timestamptz,
                ADD COLUMN IF NOT EXISTS cancel_requested_at timestamptz,
                ADD COLUMN IF NOT EXISTS last_error_code text,
                ADD COLUMN IF NOT EXISTS correlation_id uuid NOT NULL DEFAULT gen_random_uuid(),
                ADD COLUMN IF NOT EXISTS started_at timestamptz,
                ADD COLUMN IF NOT EXISTS terminal_at timestamptz,
                ADD COLUMN IF NOT EXISTS purge_after timestamptz;
            ALTER TABLE operations.job_attempts
                ADD COLUMN IF NOT EXISTS worker_pool text NOT NULL DEFAULT 'default',
                ADD COLUMN IF NOT EXISTS provider_key text,
                ADD COLUMN IF NOT EXISTS proxy_class text,
                ADD COLUMN IF NOT EXISTS country_code char(2),
                ADD COLUMN IF NOT EXISTS retry_action text,
                ADD COLUMN IF NOT EXISTS last_error_code text,
                ADD COLUMN IF NOT EXISTS safe_metrics jsonb NOT NULL DEFAULT '{}',
                ADD COLUMN IF NOT EXISTS last_heartbeat_at timestamptz,
                ADD COLUMN IF NOT EXISTS terminal_at timestamptz;
            ALTER TABLE operations.outbox_messages
                ADD COLUMN IF NOT EXISTS user_id uuid,
                ADD COLUMN IF NOT EXISTS job_id uuid,
                ADD COLUMN IF NOT EXISTS aggregate_type text,
                ADD COLUMN IF NOT EXISTS aggregate_id uuid,
                ADD COLUMN IF NOT EXISTS aggregate_sequence bigint,
                ADD COLUMN IF NOT EXISTS correlation_id uuid NOT NULL DEFAULT gen_random_uuid(),
                ADD COLUMN IF NOT EXISTS causation_message_id uuid,
                ADD COLUMN IF NOT EXISTS replay_of_message_id uuid,
                ADD COLUMN IF NOT EXISTS headers jsonb NOT NULL DEFAULT '{}',
                ADD COLUMN IF NOT EXISTS terminal_at timestamptz,
                ADD COLUMN IF NOT EXISTS purge_after timestamptz;
            ALTER TABLE operations.inbox_messages
                ADD COLUMN IF NOT EXISTS user_id uuid,
                ADD COLUMN IF NOT EXISTS source_attempt_number integer,
                ADD COLUMN IF NOT EXISTS source_execution_id uuid,
                ADD COLUMN IF NOT EXISTS source_revision bigint,
                ADD COLUMN IF NOT EXISTS attempt_count integer NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS available_at timestamptz NOT NULL DEFAULT now(),
                ADD COLUMN IF NOT EXISTS lease_token uuid,
                ADD COLUMN IF NOT EXISTS lease_expires_at timestamptz,
                ADD COLUMN IF NOT EXISTS result_code text,
                ADD COLUMN IF NOT EXISTS last_error_code text,
                ADD COLUMN IF NOT EXISTS received_at timestamptz NOT NULL DEFAULT now(),
                ADD COLUMN IF NOT EXISTS processed_at timestamptz,
                ADD COLUMN IF NOT EXISTS purge_after timestamptz;
            ALTER TABLE operations.idempotency_records
                ADD COLUMN IF NOT EXISTS version bigint NOT NULL DEFAULT 1;
            ALTER TABLE operations.jobs
                ADD CONSTRAINT ck_jobs_attempts CHECK (attempt_count >= 0 AND attempt_count <= max_attempts),
                ADD CONSTRAINT ck_jobs_contract_version CHECK (contract_version > 0),
                ADD CONSTRAINT ck_jobs_priority CHECK (priority BETWEEN -32768 AND 32767);
            ALTER TABLE operations.job_attempts
                ADD CONSTRAINT ck_job_attempts_number CHECK (attempt_number > 0),
                ADD CONSTRAINT ck_job_attempts_safe_metrics_object CHECK (jsonb_typeof(safe_metrics) = 'object');
            ALTER TABLE operations.outbox_messages
                ADD CONSTRAINT ck_outbox_payload_hash CHECK (octet_length(payload_hash) = 32),
                ADD CONSTRAINT ck_outbox_payload_size CHECK (payload_size_bytes BETWEEN 1 AND 262144),
                ADD CONSTRAINT ck_outbox_headers_object CHECK (jsonb_typeof(headers) = 'object');
            ALTER TABLE operations.inbox_messages
                ADD CONSTRAINT ck_inbox_payload_hash CHECK (octet_length(payload_hash) = 32),
                ADD CONSTRAINT ck_inbox_payload_size CHECK (payload_size_bytes BETWEEN 1 AND 262144),
                ADD CONSTRAINT ck_inbox_attempt_count CHECK (attempt_count >= 0);
            CREATE UNIQUE INDEX IF NOT EXISTS ux_job_attempts_execution_id ON operations.job_attempts (execution_id);
            CREATE UNIQUE INDEX IF NOT EXISTS ux_inbox_consumer_event
                ON operations.inbox_messages (consumer_key, event_id) WHERE event_id IS NOT NULL;
            CREATE UNIQUE INDEX IF NOT EXISTS ux_inbox_consumer_job_sequence
                ON operations.inbox_messages (consumer_key, job_id, source_sequence)
                WHERE job_id IS NOT NULL AND source_sequence IS NOT NULL;
            CREATE INDEX IF NOT EXISTS ix_jobs_scheduler
                ON operations.jobs (state, available_at, priority, created_at, id);
            CREATE INDEX IF NOT EXISTS ix_outbox_dispatch
                ON operations.outbox_messages (state, available_at, created_at, id);
            CREATE INDEX IF NOT EXISTS ix_inbox_process
                ON operations.inbox_messages (state, available_at, received_at, id);
            """);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
        => migrationBuilder.Sql("DROP INDEX IF EXISTS operations.ux_job_attempts_execution_id; DROP INDEX IF EXISTS operations.ux_inbox_consumer_event; DROP INDEX IF EXISTS operations.ux_inbox_consumer_job_sequence; DROP INDEX IF EXISTS operations.ix_jobs_scheduler; DROP INDEX IF EXISTS operations.ix_outbox_dispatch; DROP INDEX IF EXISTS operations.ix_inbox_process;");
}
