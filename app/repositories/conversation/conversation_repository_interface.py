from abc import ABC, abstractmethod
from typing import Optional

from app.entities.conversation import Conversation


class ConversationRepositoryInterface(ABC):
    @abstractmethod
    def get_conversation(self, phone_number: str) -> Optional[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def save_conversation(self, conversation: Conversation) -> None:
        raise NotImplementedError
