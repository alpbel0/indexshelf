from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import cast

import aioboto3  # type: ignore[import-untyped]
from botocore.client import Config  # type: ignore[import-untyped]


@dataclass(frozen=True, slots=True)
class ObjectStorageSettings:
    endpoint_url: str
    access_key: str
    secret_key: str
    bucket: str
    expiration: timedelta = timedelta(minutes=10)

    def validate(self) -> None:
        if not self.endpoint_url.startswith(("http://", "https://")):
            raise ValueError("Object storage endpoint must be HTTP(S)")
        if not self.access_key or not self.secret_key or not self.bucket:
            raise ValueError("Object storage credentials and bucket are required")
        if self.expiration <= timedelta(0) or self.expiration > timedelta(minutes=15):
            raise ValueError("Temporary object URL expiration must be 15 minutes or less")


class S3TemporaryObjectStorage:
    def __init__(self, settings: ObjectStorageSettings) -> None:
        settings.validate()
        self._settings = settings
        self._session = aioboto3.Session()

    async def put(self, key: str, body: bytes, content_type: str) -> None:
        if not key or "/" not in key or not content_type:
            raise ValueError("Object key and content type are required")
        async with self._session.client(
            "s3",
            endpoint_url=self._settings.endpoint_url,
            aws_access_key_id=self._settings.access_key,
            aws_secret_access_key=self._settings.secret_key,
            config=Config(signature_version="s3v4"),
        ) as client:
            await client.put_object(
                Bucket=self._settings.bucket, Key=key, Body=body, ContentType=content_type
            )

    async def presigned_get(self, key: str) -> str:
        if not key or "/" not in key:
            raise ValueError("Object key is required")
        async with self._session.client(
            "s3",
            endpoint_url=self._settings.endpoint_url,
            aws_access_key_id=self._settings.access_key,
            aws_secret_access_key=self._settings.secret_key,
            config=Config(signature_version="s3v4"),
        ) as client:
            return cast(str, await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._settings.bucket, "Key": key},
                ExpiresIn=int(self._settings.expiration.total_seconds()),
            ))
