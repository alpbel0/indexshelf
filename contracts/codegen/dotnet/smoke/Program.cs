using Newtonsoft.Json;

var commandType = typeof(IndexShelf.Contracts.Generated.CancelJob.CancelJob);
var eventType = typeof(IndexShelf.Contracts.Generated.JobCompleted.JobCompleted);
Console.WriteLine(JsonConvert.SerializeObject(new { commandName = commandType.FullName, eventName = eventType.FullName }));
