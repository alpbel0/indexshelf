using Microsoft.Extensions.DependencyInjection;

namespace IndexShelf.Modules.Identity;

public static class DependencyInjection
{
    public static IServiceCollection AddIdentityModule(this IServiceCollection services) => services;
}
