from typing import Optional

from redis import Redis

from app.components.cache.cache_interface import CacheInterface


class AsyncCache(CacheInterface):

    def __init__(self, client: Redis):
        self._client: Redis = client

    def expire(self, key: str, seconds: int) -> None:
        self._client.expire(key, seconds)

    def set(self, key: str, value: str) -> None:
        self._client.set(key, value)

    def get(self, key: str) -> Optional[str]:
        return self._client.get(key)

    def delete(self, key: str) -> None:
        self._client.delete(key)

    def exists(self, key: str) -> bool:
        return self._client.exists(key) == 1
