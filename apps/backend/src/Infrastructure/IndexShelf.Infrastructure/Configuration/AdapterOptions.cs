namespace IndexShelf.Infrastructure.Configuration;

public sealed record RabbitMqOptions(string Uri, string Exchange, int RetryAttempts = 3)
{
    public void Validate()
    {
        if (!Uri.StartsWith("amqp://", StringComparison.OrdinalIgnoreCase) && !Uri.StartsWith("amqps://", StringComparison.OrdinalIgnoreCase)) throw new InvalidOperationException("RabbitMQ URI must use amqp or amqps.");
        if (string.IsNullOrWhiteSpace(Exchange) || RetryAttempts is < 1 or > 8) throw new InvalidOperationException("RabbitMQ exchange and bounded retry attempts are required.");
    }
}

public sealed record ValkeyOptions(string Endpoint, string Namespace, int DefaultTtlSeconds = 300)
{
    public void Validate()
    {
        if (string.IsNullOrWhiteSpace(Endpoint) || !Endpoint.Contains(':')) throw new InvalidOperationException("Valkey endpoint must include host and port.");
        if (string.IsNullOrWhiteSpace(Namespace) || !Namespace.EndsWith(':')) throw new InvalidOperationException("Valkey namespace must end with a separator.");
        if (DefaultTtlSeconds is < 1 or > 1800) throw new InvalidOperationException("Valkey TTL must be positive and bounded.");
    }
}

public sealed record ObjectStorageOptions(string Endpoint, string Bucket, int PresignedUrlSeconds = 300)
{
    public void Validate()
    {
        if (!Uri.TryCreate(Endpoint, UriKind.Absolute, out var uri) || uri.Scheme is not ("http" or "https")) throw new InvalidOperationException("Object storage endpoint must be HTTP(S).");
        if (string.IsNullOrWhiteSpace(Bucket) || PresignedUrlSeconds is < 1 or > 900) throw new InvalidOperationException("Object storage bucket and bounded URL expiry are required.");
    }
}
