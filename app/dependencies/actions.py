from typing import Dict, List

from fastapi import Depends
from openai import OpenAI

from app.components.components import Components
from app.components.configuration.configuration_interface import \
    ConfigurationInterface
from app.components.logger.logger import Logger
from app.dependencies.components import get_components
from app.dependencies.repositories import get_conversation_repository
from app.dependencies.services import get_tools_service
from app.entities.actions import ActionName
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.action_interface import ActionInterface
from app.robot.actions.call_openai_action import CallOpenAIAction
from app.robot.actions.execute_tool_action import ExecuteToolAction
from app.robot.actions.fetch_conversation_action import \
    FetchConversationHistoryAction
from app.robot.actions.has_tool_call import HasToolCall
from app.robot.actions.prepare_prompt_action import PreparePromptAction
from app.robot.actions.use_response_action import UseResponseAction
from app.services.tools.tool_service_interface import ToolServiceInterface


def get_prepare_prompt_action(
        components: Components = Depends(get_components),
) -> ActionInterface:
    configuration: ConfigurationInterface = components.get_component(
        "configuration")
    return PreparePromptAction(
        system_prompt=configuration.get_configuration("SYSTEM_PROMPT", str),
    )


def get_fetch_conversation_action(
        conversation_repository: ConversationRepositoryInterface = Depends(
            get_conversation_repository),
) -> ActionInterface:
    return FetchConversationHistoryAction(
        conversation_repository=conversation_repository,
    )


def get_call_openai_action(
        components: Components = Depends(get_components),
) -> ActionInterface:
    openai_client: OpenAI = components.get_component("openai")
    configuration: ConfigurationInterface = components.get_component(
        "configuration")

    tools: List[Dict] = configuration.get_configuration(
        "TOOLS_DESCRIPTIONS", list)

    return CallOpenAIAction(
        model_name=configuration.get_configuration("OPENAI_MODEL_NAME", str),
        functions=tools,
        openai_client=openai_client,
    )


def get_has_tool_action(
) -> ActionInterface:
    return HasToolCall()


def get_use_response_action(
) -> ActionInterface:
    return UseResponseAction()


def get_execute_tool_action(
        components: Components = Depends(get_components),
        tool_service: ToolServiceInterface = Depends(get_tools_service),
) -> ActionInterface:
    logger: Logger = components.get_component("logger")

    return ExecuteToolAction(
        logger=logger.get_logger(ExecuteToolAction.__name__),
        tool_service=tool_service,
    )


def get_actions(
        fetch_conversation_action: ActionInterface = Depends(
            get_fetch_conversation_action),
        call_openai_action: ActionInterface = Depends(get_call_openai_action),
        prepare_prompt_action: ActionInterface = Depends(
            get_prepare_prompt_action),
        execute_tool_action: ActionInterface = Depends(
            get_execute_tool_action),
        has_tool_action: ActionInterface = Depends(get_has_tool_action),
        use_response_action: ActionInterface = Depends(
            get_use_response_action),
) -> dict[str, ActionInterface]:
    return {
        ActionName.FETCH_CONVERSATION_HISTORY: fetch_conversation_action,
        ActionName.CALL_OPENAI: call_openai_action,
        ActionName.PREPARE_PROMPT: prepare_prompt_action,
        ActionName.EXECUTE_FUNCTION: execute_tool_action,
        ActionName.RESPONSE_HAS_FUNCTION_CALL: has_tool_action,
        ActionName.USE_RESPONSE: use_response_action,
    }
