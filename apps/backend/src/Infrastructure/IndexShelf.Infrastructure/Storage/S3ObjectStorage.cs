using Amazon.S3;
using Amazon.S3.Model;
using IndexShelf.Infrastructure.Configuration;

namespace IndexShelf.Infrastructure.Storage;

public sealed class S3ObjectStorage(IAmazonS3 client, ObjectStorageOptions options)
{
    public async Task PutAsync(string key, ReadOnlyMemory<byte> content, string contentType, CancellationToken cancellationToken = default)
    { options.Validate(); if (string.IsNullOrWhiteSpace(key) || content.Length == 0 || string.IsNullOrWhiteSpace(contentType)) throw new ArgumentException("Object is outside the bounded contract."); await client.PutObjectAsync(new PutObjectRequest { BucketName = options.Bucket, Key = key, InputStream = new MemoryStream(content.ToArray()), ContentType = contentType }, cancellationToken); }
    public string PresignedGet(string key) { options.Validate(); if (string.IsNullOrWhiteSpace(key)) throw new ArgumentException("Object key is required."); return client.GetPreSignedURL(new GetPreSignedUrlRequest { BucketName = options.Bucket, Key = key, Verb = HttpVerb.GET, Expires = DateTime.UtcNow.AddSeconds(options.PresignedUrlSeconds) }); }
}
