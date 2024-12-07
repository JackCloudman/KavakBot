from abc import ABC, abstractmethod
from typing import Callable, Optional

from app.entities.tool_name import ToolName


class ToolServiceInterface(ABC):
    @abstractmethod
    async def get_tool(self, tool_name: ToolName) -> Optional[Callable]:
        raise NotImplementedError
