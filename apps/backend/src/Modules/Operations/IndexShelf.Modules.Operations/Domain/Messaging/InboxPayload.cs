namespace IndexShelf.Modules.Operations.Domain.Messaging;

public sealed class InboxPayload
{
    private InboxPayload() { }
    public Guid InboxId { get; private set; }
    public byte[] PayloadCiphertext { get; private set; } = null!;
    public short EncryptionKeyVersion { get; private set; }
    public DateTimeOffset CreatedAt { get; private set; }
    public DateTimeOffset HardExpiresAt { get; private set; }

    public static InboxPayload Create(Guid inboxId, byte[] ciphertext, short keyVersion, DateTimeOffset hardExpiresAt)
    {
        if (inboxId == Guid.Empty || ciphertext.Length == 0 || keyVersion < 1 || hardExpiresAt <= DateTimeOffset.UtcNow) throw new ArgumentException("Inbox payload is outside its bounded contract.");
        return new InboxPayload { InboxId = inboxId, PayloadCiphertext = ciphertext, EncryptionKeyVersion = keyVersion, CreatedAt = DateTimeOffset.UtcNow, HardExpiresAt = hardExpiresAt };
    }
}
