from abc import ABC, abstractmethod
from typing import Callable, Optional


class ToolServiceInterface(ABC):
    @abstractmethod
    async def get_tool(self, tool_name: str) -> Optional[Callable]:
        raise NotImplementedError
