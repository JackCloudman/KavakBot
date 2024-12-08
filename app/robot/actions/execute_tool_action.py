import json
import logging
from typing import Callable, Optional

import behavior_tree_cpp as bt

from app.entities.chat_role import ChatRole
from app.robot.actions.action_interface import ActionInterface
from app.services.tools.tool_service_interface import ToolServiceInterface


class ExecuteToolAction(ActionInterface):

    def __init__(self, logger: logging.Logger, tool_service: ToolServiceInterface):
        self._logger = logger
        self._tool_service = tool_service

    def execute(self, blackboard: bt.Blackboard) -> str:
        tool_call = blackboard.get(
            'openai_response').choices[0].message.function_call
        tool_args = json.loads(tool_call.arguments)

        tool: Optional[Callable] = self._tool_service.get_tool(tool_call.name)

        if tool is None:
            return "FAILURE"

        self._logger.info(
            f"Executing tool: {tool_call.name} with args: {tool_args}")
        response = tool(**tool_args)

        # Append the tool response to the openai_payload
        openai_payload = blackboard.get('openai_payload')
        openai_payload.append({
            "role": ChatRole.FUNCTION,
            "name": tool_call.name,
            "content": str(response)
        })

        blackboard.set('openai_payload', openai_payload)

        return "SUCCESS"
