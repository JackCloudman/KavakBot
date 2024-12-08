import behavior_tree_cpp as bt

from app.entities.chat_role import ChatRole
from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.action_interface import ActionInterface


class StoreConversationAction(ActionInterface):
    def __init__(self, conversation_repository: ConversationRepositoryInterface):
        self._conversation_repository: ConversationRepositoryInterface = (
            conversation_repository
        )

    def execute(self, blackboard: bt.Blackboard) -> str:
        conversation: Conversation = blackboard.get("conversation")
        final_response: str = blackboard.get("final_response")

        conversation.messages.append(Message(
            role=ChatRole.ASSISTANT,
            content=final_response,
        ))

        if conversation is None:
            return "FAILURE"

        self._conversation_repository.save_conversation(conversation)
        return "SUCCESS"
