from typing import Optional

from app.components.cache.cache_interface import CacheInterface
from app.entities.conversation import Conversation
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface


class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, db: CacheInterface):
        self._db: CacheInterface = db
        self._prefix: str = 'conversation'

    async def save_conversation(self, conversation: Conversation) -> None:
        await self._db.set(f'{self._prefix}:{conversation.phone_number}', conversation.json())

    async def get_conversation(self, phone_number: str) -> Optional[Conversation]:
        # Get the conversation data from the cache
        conversation_data_str: Optional[str] = await self._db.get(f'{self._prefix}:{phone_number}')

        if not conversation_data_str:
            return None

        return Conversation.parse_raw(conversation_data_str)
