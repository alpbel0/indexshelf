using RabbitMQ.Client;
using IndexShelf.Infrastructure.Configuration;

namespace IndexShelf.Infrastructure.Messaging;

public sealed class RabbitMqConnection : IAsyncDisposable
{
    private readonly ConnectionFactory _factory;
    private IConnection? _connection;
    public RabbitMqConnection(RabbitMqOptions options) { options.Validate(); _factory = new ConnectionFactory { Uri = new Uri(options.Uri), AutomaticRecoveryEnabled = true, TopologyRecoveryEnabled = true }; }
    public async Task<IChannel> OpenChannelAsync(CancellationToken cancellationToken = default) { _connection ??= await _factory.CreateConnectionAsync(cancellationToken); return await _connection.CreateChannelAsync(cancellationToken: cancellationToken); }
    public async ValueTask DisposeAsync() { if (_connection is not null) await _connection.DisposeAsync(); }
}
