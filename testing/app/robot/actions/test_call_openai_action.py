import pytest
from unittest.mock import MagicMock
from app.robot.actions.call_openai_action import CallOpenAIAction
import behavior_tree_cpp as bt


class TestCallOpenAIAction:
    @pytest.fixture
    def setup(self):
        model_name = "gpt-4o-mini"
        functions = [{"name": "test_function", "description": "A test function"}]
        openai_client = MagicMock()
        action = CallOpenAIAction(model_name, functions, openai_client)
        blackboard = bt.Blackboard.create()
        return action, blackboard, openai_client

    def test_execute_success(self, setup):
        action, blackboard, openai_client = setup
        openai_payload = [{"role": "user", "content": "Hello, world!"}]
        blackboard.set('openai_payload', openai_payload)

        response_mock = {"choices": [{"message": {"content": "Hello!"}}]}
        openai_client.chat.completions.create.return_value = response_mock

        result = action.execute(blackboard)

        assert result == "SUCCESS"
        assert blackboard.get('openai_response') == response_mock

    def test_execute_failure(self, setup):
        action, blackboard, openai_client = setup
        openai_payload = [{"role": "user", "content": "Hello, world!"}]
        blackboard.set('openai_payload', openai_payload)

        openai_client.chat.completions.create.side_effect = Exception("API error")

        result = action.execute(blackboard)

        assert result == "FAILURE"
        assert blackboard.get('error') == "API error"