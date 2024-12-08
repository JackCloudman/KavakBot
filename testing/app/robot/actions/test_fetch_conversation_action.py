from unittest.mock import Mock

import behavior_tree_cpp as bt
import pytest

from app.entities.conversation import Conversation
from app.entities.message import Message
from app.repositories.conversation.conversation_repository_interface import \
    ConversationRepositoryInterface
from app.robot.actions.fetch_conversation_action import \
    FetchConversationHistoryAction


class TestFetchConversationHistoryAction:
    @pytest.fixture
    def setup(self):
        self.conversation_repository = Mock(
            spec=ConversationRepositoryInterface)
        self.action = FetchConversationHistoryAction(
            self.conversation_repository)
        self.blackboard = bt.Blackboard.create()
        self.blackboard.set('phone_number', '1234567890')
        self.blackboard.set('message', Message(content='Hello'))

    def test_execute_with_existing_conversation(self, setup):
        conversation = Conversation(phone_number='1234567890', messages=[])
        self.conversation_repository.get_conversation.return_value = conversation

        result = self.action.execute(self.blackboard)

        assert result == "SUCCESS"
        assert len(conversation.messages) == 1
        assert conversation.messages[0].content == 'Hello'
        assert self.blackboard.get('conversation') == conversation

    def test_execute_with_new_conversation(self, setup):
        self.conversation_repository.get_conversation.return_value = None

        result = self.action.execute(self.blackboard)

        conversation = self.blackboard.get('conversation')
        assert result == "SUCCESS"
        assert conversation is not None
        assert conversation.phone_number == '1234567890'
        assert len(conversation.messages) == 1
        assert conversation.messages[0].content == 'Hello'
