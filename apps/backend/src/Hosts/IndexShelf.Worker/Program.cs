using IndexShelf.Application.Abstractions;
using IndexShelf.Modules.Bookmarks;
using IndexShelf.Modules.Identity;
using IndexShelf.Modules.Operations;
using IndexShelf.Modules.Reminders;
using IndexShelf.Modules.Search;
using IndexShelf.Persistence;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var builder = Host.CreateApplicationBuilder(args);
var runtimeOptions = new HostRuntimeOptions
{
    Environment = Environment.GetEnvironmentVariable("INDEXSHELF_ENVIRONMENT") ?? "local"
};
runtimeOptions.Validate();
builder.Services.AddHostedService<BootstrapWorker>();
builder.Services.AddIndexShelfRuntimePersistence();
builder.Services.AddIdentityModule()
    .AddBookmarksModule()
    .AddRemindersModule()
    .AddSearchModule()
    .AddOperationsModule();
await builder.Build().RunAsync();

internal sealed class BootstrapWorker(ILogger<BootstrapWorker> logger) : BackgroundService
{
    private static readonly Action<ILogger, Exception?> PipelineNotConfigured =
        LoggerMessage.Define(LogLevel.Warning, new EventId(1000, nameof(PipelineNotConfigured)),
            "Worker bootstrap is running; no product pipeline is configured yet.");

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        PipelineNotConfigured(logger, null);
        await Task.Delay(Timeout.InfiniteTimeSpan, stoppingToken);
    }
}
