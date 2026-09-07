using IndexShelf.Persistence.Context;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

namespace IndexShelf.Persistence.Migrations;

[DbContext(typeof(IndexShelfDbContext))]
[Migration("202609070002_OperationsContractAlignment")]
public sealed class OperationsContractAlignment : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder) => migrationBuilder.Sql("ALTER TABLE operations.outbox_messages ADD COLUMN IF NOT EXISTS state varchar(24) NOT NULL DEFAULT 'pending', ADD COLUMN IF NOT EXISTS exchange_name varchar(160) NOT NULL DEFAULT 'indexshelf.data.events', ADD COLUMN IF NOT EXISTS routing_key varchar(160) NOT NULL DEFAULT 'data.events'; ALTER TABLE operations.inbox_messages ADD COLUMN IF NOT EXISTS message_type varchar(200) NOT NULL DEFAULT 'unknown', ADD COLUMN IF NOT EXISTS schema_version smallint NOT NULL DEFAULT 1; ALTER TABLE operations.idempotency_records DROP CONSTRAINT IF EXISTS ux_idempotency_scope_user_key; CREATE UNIQUE INDEX IF NOT EXISTS ux_idempotency_scope_principal_key ON operations.idempotency_records (scope, principal_fingerprint, idempotency_key) NULLS NOT DISTINCT;");
    protected override void Down(MigrationBuilder migrationBuilder) => migrationBuilder.Sql("DROP INDEX IF EXISTS operations.ux_idempotency_scope_principal_key; ALTER TABLE operations.inbox_messages DROP COLUMN IF EXISTS message_type, DROP COLUMN IF EXISTS schema_version; ALTER TABLE operations.outbox_messages DROP COLUMN IF EXISTS state, DROP COLUMN IF EXISTS exchange_name, DROP COLUMN IF EXISTS routing_key;");
}
