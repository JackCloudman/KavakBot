from openai import OpenAI

from app.services.faq.faq_service_interface import FAQServiceInterface


class FAQService(FAQServiceInterface):
    def __init__(self,
                 openai_client: OpenAI) -> None:
        self._openai_client: OpenAI = openai_client

    async def get_answer(self, question: str) -> str:
        pass
