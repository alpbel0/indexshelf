namespace IndexShelf.Modules.Operations.Domain.Messaging;

public sealed class OutboxPayload
{
    private OutboxPayload() { }
    public Guid OutboxMessageId { get; private set; }
    public byte[] PayloadCiphertext { get; private set; } = null!;
    public short EncryptionKeyVersion { get; private set; }
    public DateTimeOffset CreatedAt { get; private set; }
    public DateTimeOffset HardExpiresAt { get; private set; }

    public static OutboxPayload Create(Guid messageId, byte[] ciphertext, short keyVersion, DateTimeOffset hardExpiresAt)
    {
        if (messageId == Guid.Empty || ciphertext.Length == 0 || keyVersion < 1 || hardExpiresAt <= DateTimeOffset.UtcNow) throw new ArgumentException("Outbox payload is outside its bounded contract.");
        return new OutboxPayload { OutboxMessageId = messageId, PayloadCiphertext = ciphertext, EncryptionKeyVersion = keyVersion, CreatedAt = DateTimeOffset.UtcNow, HardExpiresAt = hardExpiresAt };
    }
}
