from abc import ABC, abstractmethod
from typing import Any, Dict, List


class CarCatalogRepositoryInterface(ABC):
    @abstractmethod
    def search(self, search_query: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def get_unique_values(self, column: str) -> List[Any]:
        raise NotImplementedError

    def get_columns(self) -> List[str]:
        raise NotImplementedError
