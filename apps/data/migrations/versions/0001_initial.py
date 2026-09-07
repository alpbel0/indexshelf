from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    uuid = postgresql.UUID(as_uuid=True); ts = sa.DateTime(timezone=True)
    op.create_table("job_execution_records", sa.Column("id", uuid, primary_key=True), sa.Column("job_id", uuid, nullable=False), sa.Column("state", sa.String(32), nullable=False, server_default="received"), sa.Column("execution_version", sa.BigInteger(), nullable=False, server_default="1"), sa.Column("lease_token", uuid), sa.Column("lease_expires_at", ts), sa.Column("available_at", ts, nullable=False, server_default=sa.func.now()), sa.Column("last_error_code", sa.String(96)), sa.Column("created_at", ts, nullable=False, server_default=sa.func.now()), sa.Column("updated_at", ts, nullable=False, server_default=sa.func.now()), sa.UniqueConstraint("job_id", name="uq_job_execution_records_job_id"))
    op.create_index("ix_job_execution_records_state_available_at", "job_execution_records", ["state", "available_at"])
    op.create_table("extraction_attempt_records", sa.Column("id", uuid, primary_key=True), sa.Column("execution_id", uuid, sa.ForeignKey("job_execution_records.id", ondelete="CASCADE"), nullable=False), sa.Column("attempt_number", sa.Integer(), nullable=False), sa.Column("strategy", sa.String(64), nullable=False), sa.Column("state", sa.String(32), nullable=False, server_default="started"), sa.Column("error_code", sa.String(96)), sa.Column("result_ref", sa.String(512)), sa.Column("started_at", ts, nullable=False, server_default=sa.func.now()), sa.Column("finished_at", ts), sa.Column("created_at", ts, nullable=False, server_default=sa.func.now()), sa.UniqueConstraint("execution_id", "attempt_number", name="uq_attempt_execution_number"))
    op.create_index("ix_attempt_records_state_created_at", "extraction_attempt_records", ["state", "created_at"])
    op.create_table("event_outbox_records", sa.Column("id", uuid, primary_key=True), sa.Column("event_id", uuid, nullable=False), sa.Column("job_id", uuid, nullable=False), sa.Column("event_type", sa.String(96), nullable=False), sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"), sa.Column("payload", postgresql.JSONB(), nullable=False), sa.Column("payload_hash", sa.LargeBinary(32), nullable=False), sa.Column("published_at", ts), sa.Column("available_at", ts, nullable=False, server_default=sa.func.now()), sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("created_at", ts, nullable=False, server_default=sa.func.now()), sa.UniqueConstraint("event_id", name="uq_event_outbox_records_event_id"))
    op.create_index("ix_event_outbox_records_pending", "event_outbox_records", ["published_at", "available_at"])

def downgrade() -> None:
    op.drop_table("event_outbox_records"); op.drop_table("extraction_attempt_records"); op.drop_table("job_execution_records")
