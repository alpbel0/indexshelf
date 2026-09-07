namespace IndexShelf.Modules.Operations.Domain.Messaging;

public sealed class OutboxMessage
{
    private OutboxMessage() { }
    public Guid Id { get; private set; }
    public Guid MessageId { get; private set; }
    public string MessageType { get; private set; } = null!;
    public string State { get; private set; } = "pending";
    public string ExchangeName { get; private set; } = "indexshelf.data.events";
    public string RoutingKey { get; private set; } = "data.events";
    public short SchemaVersion { get; private set; }
    public byte[] PayloadHash { get; private set; } = null!;
    public int PayloadSizeBytes { get; private set; }
    public DateTimeOffset? PublishedAt { get; private set; }
    public DateTimeOffset AvailableAt { get; private set; }
    public int AttemptCount { get; private set; }
    public DateTimeOffset CreatedAt { get; private set; }
    public OutboxPayload? Payload { get; private set; }

    public static OutboxMessage Create(string messageType, short schemaVersion, byte[] payloadHash, int payloadSizeBytes)
    {
        if (string.IsNullOrWhiteSpace(messageType) || schemaVersion < 1 || payloadHash.Length != 32 || payloadSizeBytes is < 1 or > 262144)
            throw new ArgumentException("Outbox envelope is outside its bounded contract.");
        return new OutboxMessage { Id = Guid.CreateVersion7(), MessageId = Guid.CreateVersion7(), MessageType = messageType, SchemaVersion = schemaVersion, PayloadHash = payloadHash, PayloadSizeBytes = payloadSizeBytes, AvailableAt = DateTimeOffset.UtcNow, CreatedAt = DateTimeOffset.UtcNow };
    }

    public void MarkPublished() { if (PublishedAt is not null) throw new InvalidOperationException("Outbox message is already published."); PublishedAt = DateTimeOffset.UtcNow; }
}
