from abc import ABC, abstractmethod
from typing import Callable, Optional

from app.entities.tool import ToolName


class ToolServiceInterface(ABC):
    @abstractmethod
    def get_tool(self, tool_name: ToolName) -> Optional[Callable]:
        raise NotImplementedError
