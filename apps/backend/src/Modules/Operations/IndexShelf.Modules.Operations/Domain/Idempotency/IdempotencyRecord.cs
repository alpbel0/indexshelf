namespace IndexShelf.Modules.Operations.Domain.Idempotency;

public sealed class IdempotencyRecord
{
    private IdempotencyRecord() { }
    public Guid Id { get; private set; }
    public string Scope { get; private set; } = null!;
    public Guid? UserId { get; private set; }
    public byte[] PrincipalFingerprint { get; private set; } = null!;
    public Guid IdempotencyKey { get; private set; }
    public byte[] RequestHash { get; private set; } = null!;
    public string State { get; private set; } = "in_progress";
    public DateTimeOffset ExpiresAt { get; private set; }
    public long Version { get; private set; } = 1;

    public static IdempotencyRecord Create(string scope, byte[] principalFingerprint, Guid key, byte[] requestHash, DateTimeOffset expiresAt, Guid? userId = null)
    {
        if (string.IsNullOrWhiteSpace(scope) || principalFingerprint.Length != 32 || key == Guid.Empty || requestHash.Length != 32 || expiresAt <= DateTimeOffset.UtcNow) throw new ArgumentException("Idempotency record is outside its bounded contract.");
        return new IdempotencyRecord { Id = Guid.CreateVersion7(), Scope = scope, PrincipalFingerprint = principalFingerprint, IdempotencyKey = key, RequestHash = requestHash, ExpiresAt = expiresAt, UserId = userId };
    }
}
