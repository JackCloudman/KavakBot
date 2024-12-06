from app.services.faq_service_interface import FAQServiceInterface


class FAQService(FAQServiceInterface):
    def __init__(self):
        pass

    async def get_answer(self, question: str) -> str:
        pass
