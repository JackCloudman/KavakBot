from unittest.mock import MagicMock

import pytest

from app.robot.actions.action_interface import ActionInterface
from app.robot.flows.chatbot_flow import \
    ChatBotFlow  # Ajustar el import si es necesario


class TestChatBotFlow:

    @pytest.fixture
    def mock_action(self):
        # Creamos una acción mock que simule la ejecución, por ejemplo,
        # seteando 'final_response' en el blackboard y devolviendo "SUCCESS"
        mock = MagicMock(spec=ActionInterface)

        def mock_execute(blackboard):
            blackboard.set('final_response', 'Hello from action!')
            return "SUCCESS"

        mock.execute.side_effect = mock_execute
        return mock

    def test_chatbot_flow_handle_message(self, mock_action):
        # Creamos un árbol XML de ejemplo.
        # Aquí asumimos que el árbol tiene un nodo del tipo ActionName.TEST_ACTION
        # por ejemplo, <Sequence><Action ID="TEST_ACTION"/></Sequence>
        # Debes ajustar esto a la definición real de tu árbol.
        tree_xml = """
        <root main_tree_to_execute="MainTree">
            <BehaviorTree ID="MainTree">
                <Sequence>
                    <Action ID="test_action"/>
                </Sequence>
            </BehaviorTree>
        </root>
        """

        # Creamos un diccionario con las acciones
        actions = {"test_action": mock_action}

        chatbot_flow = ChatBotFlow(tree_xml=tree_xml, actions=actions)

        response = chatbot_flow.handle_message(
            phone_number="+521234567890", content="Hola")

        # Verificamos que la acción se ejecutó
        mock_action.execute.assert_called_once()

        # Verificamos que el resultado sea el que pusimos en el blackboard en la acción
        assert response == "Hello from action!"
