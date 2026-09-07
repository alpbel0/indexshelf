using RabbitMQ.Client;

namespace IndexShelf.Infrastructure.Messaging;

public sealed class OutboxMessagePublisher(IChannel channel) : IOutboxMessagePublisher
{
    public async Task PublishAsync(ReadOnlyMemory<byte> payload, string messageType, CancellationToken cancellationToken = default)
    {
        if (payload.Length is < 1 or > 262144 || string.IsNullOrWhiteSpace(messageType)) throw new ArgumentException("Message is outside the bounded contract.");
        var properties = new BasicProperties { Persistent = true, MessageId = Guid.NewGuid().ToString("N"), Type = messageType };
        await channel.BasicPublishAsync("indexshelf.data.events", "data.events", mandatory: true, properties, payload, cancellationToken);
    }
}
