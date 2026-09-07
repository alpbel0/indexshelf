namespace IndexShelf.Modules.Operations.Domain.Jobs;

public enum JobAttemptStatus { Claimed, Dispatched, Running, Succeeded, Failed, Canceled, Stale }

public sealed class JobAttempt
{
    private JobAttempt() { }
    public Guid Id { get; private set; }
    public Guid JobId { get; private set; }
    public int AttemptNumber { get; private set; }
    public Guid ExecutionId { get; private set; }
    public string Strategy { get; private set; } = null!;
    public JobAttemptStatus State { get; private set; }
    public DateTimeOffset StartedAt { get; private set; }
    public DateTimeOffset? FinishedAt { get; private set; }
    public string? ErrorCode { get; private set; }
    public long Version { get; private set; } = 1;
    public Job Job { get; private set; } = null!;

    public static JobAttempt Create(Guid jobId, int number, Guid executionId, string strategy)
    {
        if (number < 1 || executionId == Guid.Empty || string.IsNullOrWhiteSpace(strategy))
            throw new ArgumentException("Attempt identity and strategy are required.");
        return new JobAttempt { Id = Guid.CreateVersion7(), JobId = jobId, AttemptNumber = number, ExecutionId = executionId, Strategy = strategy, State = JobAttemptStatus.Claimed, StartedAt = DateTimeOffset.UtcNow };
    }

    public void Succeed() { EnsureActive(); State = JobAttemptStatus.Succeeded; FinishedAt = DateTimeOffset.UtcNow; }
    public void Fail(string errorCode) { EnsureActive(); ErrorCode = errorCode; State = JobAttemptStatus.Failed; FinishedAt = DateTimeOffset.UtcNow; }
    private void EnsureActive() { if (FinishedAt is not null) throw new InvalidOperationException("Attempt is terminal."); }
}
