from datetime import datetime
from typing import Any, Dict, Optional

import typesense
from typesense.exceptions import ObjectNotFound

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface


class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, typesense_client: typesense.Client, collection_name: str) -> None:
        self._client: typesense.Client = typesense_client
        self._collection_name: str = collection_name

    def save_conversation(self, conversation: Conversation) -> None:
        # Actualizar la fecha de actualización
        conversation.updated_at = datetime.utcnow()

        # Convertir la conversación a un diccionario
        conversation_dict: Dict[str, Any] = conversation.model_dump()
        conversation_dict["updated_at"] = int(
            conversation.updated_at.timestamp())
        conversation_dict["created_at"] = int(
            conversation.created_at.timestamp())

        # Guardar o actualizar la conversación en Typesense
        try:
            self._client.collections[self._collection_name].documents[conversation.id].update(
                conversation_dict)
        except ObjectNotFound:
            conversation_dict["created_at"] = int(
                datetime.utcnow().timestamp())
            self._client.collections[self._collection_name].documents.create(
                conversation_dict)

    def get_conversation(self, phone_number: str) -> Optional[Conversation]:
        # Buscar la conversación por número de teléfono
        search_parameters: Dict[str, Any] = {
            "q": phone_number,
            "query_by": "phone_number",
            "filter_by": f"phone_number:={phone_number}",
            "per_page": 1,
        }

        try:
            search_result: Dict[str, Any] = self._client.collections[
                self._collection_name
            ].documents.search(search_parameters)
            if search_result["found"] > 0:
                conversation_data = search_result["hits"][0]["document"]
                # Convertir timestamps a datetime
                conversation_data["created_at"] = datetime.fromtimestamp(
                    conversation_data["created_at"])
                conversation_data["updated_at"] = datetime.fromtimestamp(
                    conversation_data["updated_at"])
                # Convertir messages de STR a objetos Message
                conversation_data["messages"] = [
                    Message.from_str(msg)
                    for msg in conversation_data["messages"]
                ]
                # Limit messages history to 10
                conversation_data["messages"] = conversation_data["messages"][-10]
                return Conversation.model_validate(conversation_data)
            else:
                return None
        except Exception as e:
            print(f"Error retrieving conversation: {e}")
            return None
