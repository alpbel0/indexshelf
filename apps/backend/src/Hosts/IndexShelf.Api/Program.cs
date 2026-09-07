using IndexShelf.Application.Abstractions;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHealthChecks();
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
