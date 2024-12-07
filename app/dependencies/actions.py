from fastapi import Depends
from openai import OpenAI

from app.components.components import Components
from app.components.configuration.configuration_interface import \
    ConfigurationInterface
from app.dependencies.components import get_components
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.action_interface import ActionInterface
from app.robot.actions.call_openai_action import CallOpenAIAction
from app.robot.actions.fetch_conversation_action import \
    FetchConversationHistoryAction


def get_fetch_conversation_action(
        conversation_repository: ConversationRepositoryInterface,
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
