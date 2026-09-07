using IndexShelf.DbMigrator;
using IndexShelf.Application.Abstractions;

try
{
    var environment = Environment.GetEnvironmentVariable("INDEXSHELF_ENVIRONMENT") ?? "local";
    new HostRuntimeOptions { Environment = environment }.Validate();
    await MigrationRunner.RunAsync();
    return 0;
}
catch (InvalidOperationException exception)
{
    Console.Error.WriteLine(exception.Message);
    return 2;
}
