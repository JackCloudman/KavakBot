import pytest
from unittest.mock import Mock
from app.robot.actions.store_conversation_action import StoreConversationAction
from app.entities.conversation import Conversation
from app.entities.message import Message
from app.entities.chat_role import ChatRole
import behavior_tree_cpp as bt


class TestStoreConversationAction:
    @pytest.fixture
    def mock_conversation_repository(self):
        return Mock()

    @pytest.fixture
    def action(self, mock_conversation_repository):
        return StoreConversationAction(conversation_repository=mock_conversation_repository)

    @pytest.fixture
    def blackboard(self):
        blackboard = bt.Blackboard.create()
        blackboard.set("conversation", Conversation(messages=[],phone_number="1234567890"))
        blackboard.set("final_response", "This is a test response")
        return blackboard

    def test_execute_success(self, action, blackboard, mock_conversation_repository):
        result = action.execute(blackboard)
        assert result == "SUCCESS"
        conversation = blackboard.get("conversation")
        assert len(conversation.messages) == 1
        assert conversation.messages[0].role == ChatRole.ASSISTANT
        assert conversation.messages[0].content == "This is a test response"
        mock_conversation_repository.save_conversation.assert_called_once_with(conversation)

    def test_execute_failure(self, action, blackboard, mock_conversation_repository):
        blackboard.set("conversation", None)
        result = action.execute(blackboard)
        assert result == "FAILURE"
        mock_conversation_repository.save_conversation.assert_not_called()
