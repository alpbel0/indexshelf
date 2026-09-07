#pragma warning disable CA1725
using IndexShelf.Persistence.Context;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

namespace IndexShelf.Persistence.Migrations;

[DbContext(typeof(IndexShelfDbContext))]
[Migration("202609070001_OperationsFoundation")]
public sealed class OperationsFoundation : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            CREATE SCHEMA IF NOT EXISTS operations;
            CREATE TABLE operations.jobs (id uuid NOT NULL PRIMARY KEY, user_id uuid NULL, job_type varchar(160) NOT NULL, queue_profile varchar(80) NOT NULL, idempotency_key uuid NOT NULL UNIQUE, state varchar(32) NOT NULL, attempt_count integer NOT NULL, max_attempts integer NOT NULL, current_execution_id uuid NULL, available_at timestamptz NOT NULL, hard_expires_at timestamptz NOT NULL, created_at timestamptz NOT NULL, updated_at timestamptz NOT NULL, version bigint NOT NULL);
            CREATE INDEX ix_jobs_state_available_at ON operations.jobs (state, available_at);
            CREATE TABLE operations.job_attempts (id uuid NOT NULL PRIMARY KEY, job_id uuid NOT NULL REFERENCES operations.jobs(id) ON DELETE CASCADE, attempt_number integer NOT NULL, execution_id uuid NOT NULL, strategy varchar(80) NOT NULL, state varchar(24) NOT NULL, started_at timestamptz NOT NULL, finished_at timestamptz NULL, error_code text NULL, version bigint NOT NULL, CONSTRAINT ux_job_attempts_job_number UNIQUE(job_id, attempt_number));
            CREATE TABLE operations.outbox_messages (id uuid NOT NULL PRIMARY KEY, message_id uuid NOT NULL UNIQUE, message_type varchar(200) NOT NULL, schema_version smallint NOT NULL, payload_hash bytea NOT NULL, payload_size_bytes integer NOT NULL, published_at timestamptz NULL, available_at timestamptz NOT NULL, attempt_count integer NOT NULL, created_at timestamptz NOT NULL);
            CREATE TABLE operations.outbox_payloads (outbox_message_id uuid NOT NULL PRIMARY KEY REFERENCES operations.outbox_messages(id) ON DELETE CASCADE, payload_ciphertext bytea NOT NULL, encryption_key_version smallint NOT NULL, created_at timestamptz NOT NULL, hard_expires_at timestamptz NOT NULL);
            CREATE TABLE operations.inbox_messages (id uuid NOT NULL PRIMARY KEY, consumer_key varchar(160) NOT NULL, message_id uuid NOT NULL, event_id uuid NULL, job_id uuid NULL, source_sequence bigint NULL, payload_hash bytea NOT NULL, payload_size_bytes integer NOT NULL, state varchar(24) NOT NULL, CONSTRAINT ux_inbox_consumer_message UNIQUE(consumer_key, message_id));
            CREATE TABLE operations.inbox_payloads (inbox_id uuid NOT NULL PRIMARY KEY REFERENCES operations.inbox_messages(id) ON DELETE CASCADE, payload_ciphertext bytea NOT NULL, encryption_key_version smallint NOT NULL, created_at timestamptz NOT NULL, hard_expires_at timestamptz NOT NULL);
            CREATE TABLE operations.idempotency_records (id uuid NOT NULL PRIMARY KEY, scope varchar(120) NOT NULL, user_id uuid NULL, principal_fingerprint bytea NOT NULL, idempotency_key uuid NOT NULL, request_hash bytea NOT NULL, state varchar(24) NOT NULL, expires_at timestamptz NOT NULL, version bigint NOT NULL, CONSTRAINT ux_idempotency_scope_user_key UNIQUE(scope, user_id, idempotency_key));
            """);
    }

    protected override void Down(MigrationBuilder migrationBuilder) => migrationBuilder.Sql("DROP SCHEMA IF EXISTS operations CASCADE;");
}
