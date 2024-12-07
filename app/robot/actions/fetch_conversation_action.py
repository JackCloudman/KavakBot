import asyncio
from typing import Optional

import behavior_tree_cpp as bt

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.action_interface import ActionInterface


class FetchConversationHistoryAction(ActionInterface):
    def __init__(self,
                 conversation_repository: ConversationRepositoryInterface,
                 ) -> None:
        self._conversation_repository: ConversationRepositoryInterface = conversation_repository

    def execute(self, blackboard: bt.Blackboard) -> str:
        phone_number: str = blackboard.get('phone_number')
        message: Message = blackboard.get('message')

        # Use asyncio.run to execute the coroutine and get the result
        conversation: Optional[Conversation] = asyncio.run(
            self._conversation_repository.get_conversation(phone_number))

        if conversation is None:
            conversation = Conversation(
                phone_number=phone_number,
                messages=[]
            )

        conversation.messages.append(message)

        blackboard.set('conversation', conversation)

        return "SUCCESS"
