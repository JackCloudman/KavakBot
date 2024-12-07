from abc import ABC
from typing import Optional

from app.entities.conversation import Conversation


class ConversationRepositoryInterface(ABC):
    async def get_conversation(self, phone_number: str) -> Optional[Conversation]:
        raise NotImplementedError

    async def save_conversation(self, conversation: Conversation) -> None:
        raise NotImplementedError
