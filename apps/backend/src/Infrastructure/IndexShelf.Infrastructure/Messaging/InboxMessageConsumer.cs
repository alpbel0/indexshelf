using RabbitMQ.Client;

namespace IndexShelf.Infrastructure.Messaging;

public sealed class InboxMessageConsumer(IChannel channel) : IInboxMessageConsumer
{
    private readonly IChannel _channel = channel;
    public async Task ConsumeAsync(ulong deliveryTag, ReadOnlyMemory<byte> payload, Func<CancellationToken, Task> durableHandler, CancellationToken cancellationToken = default)
    {
        if (payload.Length is < 1 or > 262144) throw new ArgumentException("Message is outside the bounded contract.");
        await durableHandler(cancellationToken);
        DeliveryPolicy.EnsureDurableBeforeAck(true);
        await _channel.BasicAckAsync(deliveryTag, multiple: false, cancellationToken);
    }
}
