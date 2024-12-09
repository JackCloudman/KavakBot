from unittest.mock import Mock

import behavior_tree_cpp as bt
import pytest

from app.robot.actions.use_response_action import UseResponseAction


class TestUseResponseAction:
    @pytest.fixture
    def mock_blackboard(self):
        blackboard = bt.Blackboard.create()
        blackboard.set("openai_response", Mock(
            choices=[Mock(message=Mock(content="This is a test response"))]))
        return blackboard

    @pytest.fixture
    def action(self):
        return UseResponseAction()

    def test_execute_success(self, action, mock_blackboard):
        result = action.execute(mock_blackboard)
        assert result == "SUCCESS"
        assert mock_blackboard.get(
            "final_response") == "This is a test response"

    def test_execute_failure(self, action):
        blackboard = bt.Blackboard.create()
        result = action.execute(blackboard)
        assert result == "FAILURE"
