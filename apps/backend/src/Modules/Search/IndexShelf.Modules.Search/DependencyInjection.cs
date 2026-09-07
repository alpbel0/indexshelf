using Microsoft.Extensions.DependencyInjection;

namespace IndexShelf.Modules.Search;

public static class DependencyInjection
{
    public static IServiceCollection AddSearchModule(this IServiceCollection services) => services;
}
