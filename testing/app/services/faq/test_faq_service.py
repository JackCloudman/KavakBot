from unittest.mock import MagicMock

import pytest

from app.services.faq.faq_service import FAQService


class TestFAQService:

    @pytest.fixture
    def openai_client(self):
        return MagicMock()

    @pytest.fixture
    def faq_service(self, openai_client):
        return FAQService("instructions", "assistant_id", openai_client)

    def test_get_answer_completed(self, faq_service, openai_client):
        question = "Que es Kavak?"
        thread = MagicMock()
        thread.id = "thread_id"
        openai_client.beta.threads.create.return_value = thread

        run = MagicMock()
        run.status = "completed"
        openai_client.beta.threads.runs.create_and_poll.return_value = run

        message_text = MagicMock()
        message_text.value = "Kavak es una empresa de compra y venta de autos usados."
        message_text.annotations = []

        message_content = MagicMock()
        message_content.text = message_text

        message = MagicMock()
        message.content = [message_content]
        messages_page = [message]

        openai_client.beta.threads.messages.list.return_value = messages_page

        answer = faq_service.get_answer(question)

        assert answer == "Kavak es una empresa de compra y venta de autos usados."

    def test_get_answer_not_completed(self, faq_service, openai_client):
        question = "What is the capital of France?"
        thread = MagicMock()
        thread.id = "thread_id"
        openai_client.beta.threads.create.return_value = thread

        run = MagicMock()
        run.status = "in_progress"
        openai_client.beta.threads.runs.create_and_poll.return_value = run

        answer = faq_service.get_answer(question)

        assert answer == "I'm sorry, I don't have an answer for you right now."
