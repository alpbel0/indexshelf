#pragma warning disable CA1725
using IndexShelf.Modules.Operations.Domain.Idempotency;
using IndexShelf.Modules.Operations.Domain.Jobs;
using IndexShelf.Modules.Operations.Domain.Messaging;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace IndexShelf.Persistence.Configurations.Operations;

public sealed class JobConfiguration : IEntityTypeConfiguration<Job>
{
    public void Configure(EntityTypeBuilder<Job> b)
    {
        b.ToTable("jobs", "operations"); b.HasKey(x => x.Id);
        b.Property(x => x.JobType).HasMaxLength(160).IsRequired(); b.Property(x => x.QueueProfile).HasMaxLength(80).IsRequired();
        b.Property(x => x.State).HasConversion<string>().HasMaxLength(32).IsRequired();
        b.HasIndex(x => new { x.State, x.AvailableAt }); b.HasIndex(x => x.IdempotencyKey).IsUnique();
        b.HasMany(x => x.Attempts).WithOne().HasForeignKey(x => x.JobId).OnDelete(DeleteBehavior.Cascade);
    }
}

public sealed class JobAttemptConfiguration : IEntityTypeConfiguration<JobAttempt>
{
    public void Configure(EntityTypeBuilder<JobAttempt> b)
    {
        b.ToTable("job_attempts", "operations"); b.HasKey(x => x.Id);
        b.Property(x => x.Strategy).HasMaxLength(80).IsRequired(); b.Property(x => x.State).HasConversion<string>().HasMaxLength(24);
        b.HasIndex(x => new { x.JobId, x.AttemptNumber }).IsUnique(); b.HasOne(x => x.Job).WithMany().HasForeignKey(x => x.JobId);
    }
}

public sealed class OutboxMessageConfiguration : IEntityTypeConfiguration<OutboxMessage>
{
    public void Configure(EntityTypeBuilder<OutboxMessage> b)
    {
        b.ToTable("outbox_messages", "operations"); b.HasKey(x => x.Id);
        b.Property(x => x.MessageType).HasMaxLength(200).IsRequired(); b.Property(x => x.State).HasMaxLength(24).IsRequired(); b.Property(x => x.ExchangeName).HasMaxLength(160).IsRequired(); b.Property(x => x.RoutingKey).HasMaxLength(160).IsRequired(); b.Property(x => x.PayloadHash).HasMaxLength(32).IsRequired();
        b.HasIndex(x => x.MessageId).IsUnique(); b.HasIndex(x => new { x.PublishedAt, x.AvailableAt });
        b.HasOne(x => x.Payload).WithOne().HasForeignKey<OutboxPayload>(x => x.OutboxMessageId).OnDelete(DeleteBehavior.Cascade);
    }
}

public sealed class OutboxPayloadConfiguration : IEntityTypeConfiguration<OutboxPayload>
{
    public void Configure(EntityTypeBuilder<OutboxPayload> b) { b.ToTable("outbox_payloads", "operations"); b.HasKey(x => x.OutboxMessageId); b.Property(x => x.PayloadCiphertext).IsRequired(); b.Property(x => x.EncryptionKeyVersion).IsRequired(); }
}

public sealed class InboxMessageConfiguration : IEntityTypeConfiguration<InboxMessage>
{
    public void Configure(EntityTypeBuilder<InboxMessage> b)
    {
        b.ToTable("inbox_messages", "operations"); b.HasKey(x => x.Id);
        b.Property(x => x.ConsumerKey).HasMaxLength(160).IsRequired(); b.Property(x => x.MessageType).HasMaxLength(200).IsRequired(); b.Property(x => x.State).HasMaxLength(24).IsRequired();
        b.HasIndex(x => new { x.ConsumerKey, x.MessageId }).IsUnique(); b.HasOne(x => x.Payload).WithOne().HasForeignKey<InboxPayload>(x => x.InboxId).OnDelete(DeleteBehavior.Cascade);
    }
}

public sealed class InboxPayloadConfiguration : IEntityTypeConfiguration<InboxPayload>
{
    public void Configure(EntityTypeBuilder<InboxPayload> b) { b.ToTable("inbox_payloads", "operations"); b.HasKey(x => x.InboxId); b.Property(x => x.PayloadCiphertext).IsRequired(); b.Property(x => x.EncryptionKeyVersion).IsRequired(); }
}

public sealed class IdempotencyRecordConfiguration : IEntityTypeConfiguration<IdempotencyRecord>
{
    public void Configure(EntityTypeBuilder<IdempotencyRecord> b) { b.ToTable("idempotency_records", "operations"); b.HasKey(x => x.Id); b.Property(x => x.Scope).HasMaxLength(120).IsRequired(); b.Property(x => x.PrincipalFingerprint).HasMaxLength(32).IsRequired(); b.Property(x => x.RequestHash).HasMaxLength(32).IsRequired(); b.HasIndex(x => new { x.Scope, x.PrincipalFingerprint, x.IdempotencyKey }).IsUnique().HasDatabaseName("ux_idempotency_scope_principal_key"); }
}
