using IndexShelf.Application.Abstractions;
using IndexShelf.Modules.Bookmarks;
using IndexShelf.Modules.Identity;
using IndexShelf.Modules.Operations;
using IndexShelf.Modules.Reminders;
using IndexShelf.Modules.Search;
using IndexShelf.Persistence;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHealthChecks();
builder.Services.AddIndexShelfRuntimePersistence();
builder.Services.AddIdentityModule()
    .AddBookmarksModule()
    .AddRemindersModule()
    .AddSearchModule()
    .AddOperationsModule();
var runtimeOptions = new HostRuntimeOptions
{
    Environment = Environment.GetEnvironmentVariable("INDEXSHELF_ENVIRONMENT") ?? "local"
};
runtimeOptions.Validate();

var app = builder.Build();

app.MapGet("/health/live", () => Results.Ok(new { status = "live" }));
app.MapHealthChecks("/health/ready");

app.Run();

public partial class Program;
