import json
from unittest.mock import MagicMock

import behavior_tree_cpp as bt
import pytest

from app.entities.chat_role import ChatRole
from app.robot.actions.execute_tool_action import \
    ExecuteToolAction  # Ajustar el import si es necesario
from app.services.tools.tool_service_interface import ToolServiceInterface


class TestExecuteToolAction:

    @pytest.fixture
    def mock_logger(self):
        return MagicMock()

    @pytest.fixture
    def mock_tool_service(self):
        return MagicMock(spec=ToolServiceInterface)

    @pytest.fixture
    def mock_blackboard(self):
        # Creamos un blackboard de behavior_tree_cpp
        bb = bt.Blackboard.create()

        # Simulamos la respuesta de openai_response
        bb.set('openai_response', MagicMock())
        bb.get('openai_response').choices = [
            MagicMock()
        ]
        bb.get('openai_response').choices[0].message = MagicMock()
        bb.get(
            'openai_response').choices[0].message.function_call = MagicMock()
        bb.get(
            'openai_response').choices[0].message.function_call.name = 'test_tool'
        bb.get('openai_response').choices[0].message.function_call.arguments = json.dumps(
            {"param": "value"})

        # Simulamos el openai_payload, inicialmente una lista vacía
        bb.set('openai_payload', [])

        return bb

    def test_execute_tool_action_success(self, mock_logger, mock_tool_service, mock_blackboard):
        # Creamos una función mock para el tool
        def mock_tool(**kwargs):
            return {"result": "ok"}

        # Preparamos el mock_tool_service
        mock_tool_service.get_tool.return_value = mock_tool

        action = ExecuteToolAction(mock_logger, mock_tool_service)
        result = action.execute(mock_blackboard)

        assert result == "SUCCESS"
        openai_payload = mock_blackboard.get('openai_payload')
        assert len(openai_payload) == 1
        assert openai_payload[0]['role'] == ChatRole.FUNCTION
        assert openai_payload[0]['name'] == 'test_tool'
        assert openai_payload[0]['content'] == str({"result": "ok"})
        mock_logger.info.assert_called_once()

    def test_execute_tool_action_failure_no_tool(self, mock_logger, mock_tool_service, mock_blackboard):
        # Si no se encuentra el tool
        mock_tool_service.get_tool.return_value = None

        action = ExecuteToolAction(mock_logger, mock_tool_service)
        result = action.execute(mock_blackboard)

        assert result == "FAILURE"
        openai_payload = mock_blackboard.get('openai_payload')
        # No se añade nada en el payload si falla
        assert openai_payload == []
        mock_logger.info.assert_not_called()
