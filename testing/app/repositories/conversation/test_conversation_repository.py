from datetime import datetime
from unittest.mock import MagicMock

import pytest
from typesense.exceptions import ObjectNotFound

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation.conversation_repository import \
    ConversationRepository


class TestConversationRepository:

    @pytest.fixture
    def typesense_client(self):
        return MagicMock()

    @pytest.fixture
    def repository(self, typesense_client):
        return ConversationRepository(typesense_client, "conversations")

    def test_save_conversation_update(self, repository, typesense_client):
        conversation = Conversation(
            id="1",
            phone_number="1234567890",
            messages=[Message(content="Hello", timestamp=datetime.utcnow())],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        conversation_dict = conversation.model_dump()
        conversation_dict["updated_at"] = int(
            conversation.updated_at.timestamp())
        conversation_dict["created_at"] = int(
            conversation.created_at.timestamp())

        repository.save_conversation(conversation)

        typesense_client.collections["conversations"].documents[conversation.id].update.assert_called_once_with(
            conversation_dict)

    def test_save_conversation_create(self, repository, typesense_client):
        conversation = Conversation(
            id="1",
            phone_number="1234567890",
            messages=[Message(content="Hello", timestamp=datetime.utcnow())],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        conversation_dict = conversation.model_dump()
        conversation_dict["updated_at"] = int(
            conversation.updated_at.timestamp())
        conversation_dict["created_at"] = int(
            conversation.created_at.timestamp())

        typesense_client.collections["conversations"].documents[conversation.id].update.side_effect = ObjectNotFound

        repository.save_conversation(conversation)

        typesense_client.collections["conversations"].documents.create.assert_called_once_with(
            conversation_dict)

    def test_get_conversation(self, repository, typesense_client):
        phone_number = "1234567890"
        search_result = {
            "found": 1,
            "hits": [{
                "document": {
                    "id": "1",
                    "phone_number": phone_number,
                    "messages": ["user: Hola", "assistant: Hello"],
                    "created_at": 1696932000,
                    "updated_at": 1696932000
                }
            }]
        }
        typesense_client.collections["conversations"].documents.search.return_value = search_result

        conversation = repository.get_conversation(phone_number)

        assert conversation is not None
        assert conversation.phone_number == phone_number
        assert len(conversation.messages) == 2
        assert conversation.messages[0].content == "Hola"

    def test_get_conversation_no_results(self, repository, typesense_client):
        phone_number = "1234567890"
        search_result = {
            "found": 0,
            "hits": []
        }

        typesense_client.collections["conversations"].documents.search.return_value = search_result

        conversation = repository.get_conversation(phone_number)

        assert conversation is None

    def test_get_conversation_error(self, repository, typesense_client):
        phone_number = "1234567890"
        search_result = {
            "found": 1,
            "hits": [{
                "document": {
                    "id": "1",
                    "phone_number": phone_number,
                    "messages": ["noop"],
                    "created_at": 1696932000,
                    "updated_at": 1696932000
                }
            }]
        }

        typesense_client.collections["conversations"].documents.search.return_value = search_result

        conversation = repository.get_conversation(phone_number)

        assert conversation is None
