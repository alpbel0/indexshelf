using Microsoft.Extensions.DependencyInjection;

namespace IndexShelf.Modules.Reminders;

public static class DependencyInjection
{
    public static IServiceCollection AddRemindersModule(this IServiceCollection services) => services;
}
