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
            Message(role=ChatRole.SYSTEM, content="Bienvenido al sistema"),
            Message(role=ChatRole.USER, content="Hola, ¿cómo estás?"),
            Message(role=ChatRole.ASSISTANT,
                    content="Estoy bien, gracias por preguntar."),
            Message(role=ChatRole.USER,
                    content="Por que existe algo en lugar de nada?")
        ]
        return Conversation(messages=messages, phone_number="1234567890")

    def test_prepare_prompt_action_with_history(self, mock_blackboard, conversation):
        # Agregamos la conversación al blackboard
        mock_blackboard.set('conversation', conversation)

        # Creamos la acción con un system_prompt
        system_prompt = "Este es el prompt del sistema."
        action = PreparePromptAction(system_prompt=system_prompt)

        # Ejecutamos la acción
        result = action.execute(mock_blackboard)
        assert result == "SUCCESS"

        # Revisamos el openai_payload
        openai_payload = mock_blackboard.get('openai_payload')
        assert len(openai_payload) == 2

        # Revisamos que el primer mensaje sea el SYSTEM con prompt + history + fecha
        system_content = openai_payload[0]['content']
        assert openai_payload[0]['role'] == ChatRole.SYSTEM
        assert system_prompt in system_content
        # Debe contener el historial
        assert "SYSTEM: Bienvenido al sistema".lower() in system_content.lower()
        assert "USER: Hola, ¿cómo estás?".lower() in system_content.lower()
        assert "ASSISTANT: Estoy bien, gracias por preguntar.".lower() in system_content.lower()
        # Debe contener la fecha actual formateada
        current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M")  # exclude seconds
        assert current_date in system_content

        # El segundo mensaje debe ser USER con el último mensaje
        assert openai_payload[1]['role'] == ChatRole.USER
        # El último mensaje del user antes de ejecutar era el assistant, así que el popped es el último "Estoy bien..."
        # Pero el código realmente saca el último mensaje del array: en este caso era el ASSISTANT. Luego lo vuelve a poner.
        # Entonces el prompt del usuario será el último mensaje (assistant) que fue sacado y vuelto a poner:
        user_content = openai_payload[1]['content']
        assert isinstance(user_content, list)
        assert len(user_content) == 1
        assert user_content[0]['text'] == "Por que existe algo en lugar de nada?"

        # Revisamos que la conversación haya sido restaurada
        restored_conversation = mock_blackboard.get('conversation')
        assert len(restored_conversation.messages) == 4
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
