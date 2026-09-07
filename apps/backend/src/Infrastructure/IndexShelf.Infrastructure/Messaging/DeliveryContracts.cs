namespace IndexShelf.Infrastructure.Messaging;

public interface IOutboxMessagePublisher
{
    Task PublishAsync(ReadOnlyMemory<byte> payload, string messageType, CancellationToken cancellationToken = default);
}

public interface IInboxMessageConsumer
{
    Task ConsumeAsync(ReadOnlyMemory<byte> payload, Func<CancellationToken, Task> durableHandler, CancellationToken cancellationToken = default);
}

public static class DeliveryPolicy
{
    public static void EnsureDurableBeforeAck(bool durable) { if (!durable) throw new InvalidOperationException("Message acknowledgement requires a durable inbox transaction."); }
}
