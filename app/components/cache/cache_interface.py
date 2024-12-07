from abc import ABC, abstractmethod
from typing import Optional


class CacheInterface(ABC):
    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def expire(self, key: str, seconds: int) -> None:
        pass
