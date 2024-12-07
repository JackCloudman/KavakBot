from abc import ABC, abstractmethod
from typing import Optional


class CacheInterface(ABC):
    @abstractmethod
    def set(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def expire(self, key: str, seconds: int) -> None:
        pass
