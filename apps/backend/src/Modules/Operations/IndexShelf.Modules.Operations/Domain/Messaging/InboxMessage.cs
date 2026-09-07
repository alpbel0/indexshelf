namespace IndexShelf.Modules.Operations.Domain.Messaging;

public sealed class InboxMessage
{
    private InboxMessage() { }
    public Guid Id { get; private set; }
    public string ConsumerKey { get; private set; } = null!;
    public Guid MessageId { get; private set; }
    public Guid? EventId { get; private set; }
    public Guid? JobId { get; private set; }
    public string MessageType { get; private set; } = "unknown";
    public short SchemaVersion { get; private set; } = 1;
    public long? SourceSequence { get; private set; }
    public byte[] PayloadHash { get; private set; } = null!;
    public int PayloadSizeBytes { get; private set; }
    public string State { get; private set; } = "received";
    public InboxPayload? Payload { get; private set; }

    public static InboxMessage Create(string consumerKey, Guid messageId, byte[] payloadHash, int payloadSizeBytes, string messageType = "unknown", short schemaVersion = 1)
    {
        if (string.IsNullOrWhiteSpace(consumerKey) || messageId == Guid.Empty || payloadHash.Length != 32 || payloadSizeBytes is < 1 or > 262144 || schemaVersion < 1) throw new ArgumentException("Inbox envelope is outside its bounded contract.");
        return new InboxMessage { Id = Guid.CreateVersion7(), ConsumerKey = consumerKey, MessageId = messageId, MessageType = messageType, SchemaVersion = schemaVersion, PayloadHash = payloadHash, PayloadSizeBytes = payloadSizeBytes, State = "received" };
    }
}
