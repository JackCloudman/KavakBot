from fastapi import Depends
from openai import OpenAI

from app.components.components import Components
from app.components.configuration.configuration_interface import \
    ConfigurationInterface
from app.dependencies.components import get_components
from app.dependencies.repositories import get_conversation_repository
from app.entities.actions import ActionName
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.action_interface import ActionInterface
from app.robot.actions.call_openai_action import CallOpenAIAction
from app.robot.actions.fetch_conversation_action import \
    FetchConversationHistoryAction
from app.robot.actions.prepare_prompt_action import PreparePromptAction


def get_prepare_prompt_action(
        components: Components = Depends(get_components),
) -> ActionInterface:
    configuration: ConfigurationInterface = components.get_component("configuration")
    return PreparePromptAction(
        system_prompt=configuration.get_configuration("SYSTEM_PROMPT", str),
    )


def get_fetch_conversation_action(
        conversation_repository: ConversationRepositoryInterface = Depends(get_conversation_repository),
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

    return CallOpenAIAction(
        model_name=configuration.get_configuration("OPENAI_MODEL_NAME", str),
        openai_client=openai_client,
    )


def get_actions(
        fetch_conversation_action: ActionInterface = Depends(
            get_fetch_conversation_action),
        call_openai_action: ActionInterface = Depends(get_call_openai_action),
        prepare_prompt_action: ActionInterface = Depends(get_prepare_prompt_action),
) -> dict[str, ActionInterface]:
    return {
        ActionName.FETCH_CONVERSATION_HISTORY: fetch_conversation_action,
        ActionName.CALL_OPENAI: call_openai_action,
        ActionName.PREPARE_PROMPT: prepare_prompt_action,
    }
