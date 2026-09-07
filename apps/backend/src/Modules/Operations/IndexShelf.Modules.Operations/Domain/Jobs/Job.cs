namespace IndexShelf.Modules.Operations.Domain.Jobs;

public enum JobStatus { DeferredAdmission, Queued, Dispatching, Dispatched, Running, WaitingRetry, Completed, PartiallyCompleted, Failed, Canceled, DeadLetter, Expired }

public sealed class Job
{
    private Job() { }

    public Guid Id { get; private set; }
    public Guid? UserId { get; private set; }
    public string JobType { get; private set; } = null!;
    public string QueueProfile { get; private set; } = null!;
    public Guid IdempotencyKey { get; private set; }
    public JobStatus State { get; private set; }
    public int AttemptCount { get; private set; }
    public int MaxAttempts { get; private set; }
    public Guid? CurrentExecutionId { get; private set; }
    public DateTimeOffset AvailableAt { get; private set; }
    public DateTimeOffset HardExpiresAt { get; private set; }
    public DateTimeOffset CreatedAt { get; private set; }
    public DateTimeOffset UpdatedAt { get; private set; }
    public long Version { get; private set; } = 1;
    public ICollection<JobAttempt> Attempts { get; private set; } = new List<JobAttempt>();

    public static Job Create(string jobType, string queueProfile, int maxAttempts, Guid? userId = null)
    {
        if (string.IsNullOrWhiteSpace(jobType) || string.IsNullOrWhiteSpace(queueProfile) || maxAttempts < 1)
            throw new ArgumentException("Job type, queue profile and positive max attempts are required.");
        var now = DateTimeOffset.UtcNow;
        return new Job { Id = Guid.CreateVersion7(), IdempotencyKey = Guid.CreateVersion7(), JobType = jobType, QueueProfile = queueProfile, MaxAttempts = maxAttempts, UserId = userId, State = JobStatus.DeferredAdmission, AvailableAt = now, HardExpiresAt = now.AddHours(1), CreatedAt = now, UpdatedAt = now };
    }

    public JobAttempt StartAttempt(string strategy, Guid executionId)
    {
        if (State is JobStatus.Completed or JobStatus.Failed or JobStatus.Canceled or JobStatus.DeadLetter or JobStatus.Expired)
            throw new InvalidOperationException("Terminal jobs cannot start an attempt.");
        if (AttemptCount >= MaxAttempts)
            throw new InvalidOperationException("Job attempt limit reached.");
        AttemptCount++;
        CurrentExecutionId = executionId;
        State = JobStatus.Running;
        UpdatedAt = DateTimeOffset.UtcNow;
        var attempt = JobAttempt.Create(Id, AttemptCount, executionId, strategy);
        Attempts.Add(attempt);
        return attempt;
    }
}
