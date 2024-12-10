from datetime import datetime

import behavior_tree_cpp as bt
import pytest

from app.entities.chat_role import ChatRole
from app.entities.conversation import Conversation
from app.entities.message import Message
from app.robot.actions.prepare_prompt_action import \
    PreparePromptAction  # Ajustar el import si es necesario


class TestPreparePromptAction:

    @pytest.fixture
    def mock_blackboard(self):
        bb = bt.Blackboard.create()
        return bb

    @pytest.fixture
    def conversation(self):
        # Creamos un objeto conversación con algunos mensajes
        messages = [
            Message(role=ChatRole.USER, content="Hola, ¿cómo estás?"),
            Message(role=ChatRole.ASSISTANT,
                    content="Estoy bien, gracias por preguntar."),
            Message(role=ChatRole.USER,
                    content="Por que existe algo en lugar de nada?")
        ]
        return Conversation(messages=messages, phone_number="1234567890")

    def test_prepare_prompt_action_with_history(self, mock_blackboard, conversation):
        # Agregar la conversación al blackboard
        mock_blackboard.set('conversation', conversation)

        # Crear la acción con un system_prompt
        system_prompt = "Este es el prompt del sistema."
        action = PreparePromptAction(system_prompt=system_prompt)

        # Ejecutar la acción y verificar el resultado
        result = action.execute(mock_blackboard)
        assert result == "SUCCESS"

        # Obtener y verificar el openai_payload
        openai_payload = mock_blackboard.get('openai_payload')
        assert len(openai_payload) == 4

        roles = [message['role'] for message in openai_payload]
        assert roles == [
            ChatRole.SYSTEM,
            ChatRole.USER,
            ChatRole.ASSISTANT,
            ChatRole.USER
        ]

        system_content = openai_payload[0]['content']
        assert "este es el prompt del sistema." in system_content.lower()
        current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        assert current_date in system_content

        # Verificar el contenido de los mensajes anteriores
        user_message = openai_payload[1]['content'][0]['text']
        assistant_message = openai_payload[2]['content'][0]['text']
        assert "hola, ¿cómo estás?" in user_message.lower()
        assert "estoy bien, gracias por preguntar." in assistant_message.lower()

        # Verificar el último mensaje del usuario
        user_content = openai_payload[3]['content']
        assert isinstance(user_content, list)
        assert len(user_content) == 1
        assert user_content[0]['text'] == "Por que existe algo en lugar de nada?"

        # Verificar que la conversación haya sido restaurada correctamente
        restored_conversation = mock_blackboard.get('conversation')
        assert len(restored_conversation.messages) == 3
        assert restored_conversation.messages[-1].content == "Por que existe algo en lugar de nada?"

    def test_prepare_prompt_action_no_history(self, mock_blackboard):
        # Conversación con un solo mensaje
        conversation = Conversation(messages=[
            Message(role=ChatRole.USER, content="Solo un mensaje")
        ],
            phone_number="1234567890"
        )
        mock_blackboard.set('conversation', conversation)
        system_prompt = "Prompt del sistema."
        action = PreparePromptAction(system_prompt=system_prompt)

        result = action.execute(mock_blackboard)
        assert result == "SUCCESS"

        openai_payload = mock_blackboard.get('openai_payload')
        assert len(openai_payload) == 2

        # Solo un mensaje, por lo tanto no hay historial (se hace pop del último y queda nada)
        system_content = openai_payload[0]['content']
        assert system_prompt in system_content
        # No debe haber roles previos, solo el system_prompt y la fecha
        assert "USER:" not in system_content
        assert "ASSISTANT:" not in system_content
        current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        assert current_date in system_content

        # El usuario con su único mensaje
        user_content = openai_payload[1]['content']
        assert user_content[0]['text'] == "Solo un mensaje"
