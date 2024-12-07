from typing import Callable, Optional

from fastapi import APIRouter, Depends

from app.dependencies.services import get_tools_service
from app.entities.tool_name import ToolName
from app.services.tools.tool_service_interface import ToolServiceInterface

router: APIRouter = APIRouter()


@router.get('/webhook/{tool_name}')
async def webhook(
        tool_name: ToolName,
        tools_service: ToolServiceInterface = Depends(get_tools_service)
):
    print(tool_name)
    tool: Optional[Callable] = await tools_service.get_tool(tool_name)

    if not tool:
        return {'message': 'Tool not found!'}

    tool({})

    return {'message': 'Tool executed!'}
