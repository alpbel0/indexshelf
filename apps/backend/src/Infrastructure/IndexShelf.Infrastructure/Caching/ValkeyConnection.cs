using StackExchange.Redis;
using IndexShelf.Infrastructure.Configuration;

namespace IndexShelf.Infrastructure.Caching;

public sealed class ValkeyConnection(ValkeyOptions options) : IAsyncDisposable
{
    private readonly ConnectionMultiplexer _connection = Connect(options);
    private static ConnectionMultiplexer Connect(ValkeyOptions options) { options.Validate(); return ConnectionMultiplexer.Connect(options.Endpoint); }
    public async Task<byte[]?> GetAsync(string key) => await _connection.GetDatabase().StringGetAsync(key);
    public async Task SetAsync(string key, byte[] value, TimeSpan ttl) { if (ttl <= TimeSpan.Zero || ttl > TimeSpan.FromMinutes(30)) throw new ArgumentOutOfRangeException(nameof(ttl)); await _connection.GetDatabase().StringSetAsync(key, value, ttl); }
    public ValueTask DisposeAsync() { _connection.Dispose(); return ValueTask.CompletedTask; }
}
