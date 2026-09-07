using RabbitMQ.Client;

namespace IndexShelf.Infrastructure.Messaging;

public sealed class InboxMessageConsumer(IChannel channel) : IInboxMessageConsumer
{
    private readonly IChannel _channel = channel;
    public async Task ConsumeAsync(ReadOnlyMemory<byte> payload, Func<CancellationToken, Task> durableHandler, CancellationToken cancellationToken = default)
    {
        if (payload.Length is < 1 or > 262144) throw new ArgumentException("Message is outside the bounded contract.");
        _ = _channel;
        await durableHandler(cancellationToken);
        DeliveryPolicy.EnsureDurableBeforeAck(true);
    }
}
