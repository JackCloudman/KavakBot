from typing import Callable, Dict, Optional

from app.entities.tool import ToolName
from app.services.tools.tool_service_interface import ToolServiceInterface


class ToolService(ToolServiceInterface):

    def __init__(self, tools: Dict[ToolName, Callable]) -> None:
        self._tools: Dict[ToolName, Callable] = tools

    def get_tool(self, tool_name: ToolName) -> Optional[Callable]:
        return self._tools.get(tool_name)
