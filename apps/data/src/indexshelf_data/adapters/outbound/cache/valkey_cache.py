from __future__ import annotations

from datetime import timedelta
from typing import cast

from redis.asyncio import Redis


class ValkeyCache:
    def __init__(self, client: Redis, *, namespace: str = "indexshelf:data") -> None:
        if not namespace or ":" not in namespace:
            raise ValueError("Valkey namespace must be explicit")
        self._client = client
        self._namespace = namespace

    def key(self, key: str) -> str:
        if not key or ":" in key:
            raise ValueError("Cache key must be a non-empty opaque segment")
        return f"{self._namespace}:{key}"

    async def get(self, key: str) -> bytes | None:
        return cast(bytes | None, await self._client.get(self.key(key)))

    async def set(self, key: str, value: bytes, ttl: timedelta) -> None:
        if ttl.total_seconds() <= 0 or ttl > timedelta(minutes=30):
            raise ValueError("Cache TTL must be positive and no longer than 30 minutes")
        await self._client.set(self.key(key), value, ex=ttl)
