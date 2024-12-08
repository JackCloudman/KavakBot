from typing import List

from openai import OpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Message

from app.services.faq.faq_service_interface import FAQServiceInterface
from app.utils.remove_annotations import remove_file_annotations


class FAQService(FAQServiceInterface):
    def __init__(self,
                 instructions: str,
                 assistant_id: str,
                 openai_client: OpenAI) -> None:
        self._instructions: str = instructions
        self._assistant_id: str = assistant_id
        self._openai_client: OpenAI = openai_client

    def get_answer(self, question: str) -> str:
        thread: Thread = self._openai_client.beta.threads.create()

        thread_message = self._openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
        )

        run = self._openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self._assistant_id,
            instructions=self._instructions,
        )

        if run.status == "completed":
            messages_page = self._openai_client.beta.threads.messages.list(
                thread_id=thread.id,
            )
            messages: List[Message] = list(messages_page)
            text = messages[0].content[0].text
            return remove_file_annotations(text.value, text.annotations)

        return "I'm sorry, I don't have an answer for you right now."
