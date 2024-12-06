from typing import Callable, Dict, Optional

from app.services.tool_service_interface import ToolServiceInterface


class ToolService(ToolServiceInterface):

    def __init__(self, tools: Dict[str, Callable]) -> None:
        self._tools = tools

    async def get_tool(self, tool_name: str) -> Optional[Callable]:
        return self._tools.get(tool_name)
