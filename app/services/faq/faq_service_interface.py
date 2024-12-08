from abc import ABC, abstractmethod


class FAQServiceInterface(ABC):
    @abstractmethod
    def get_answer(self, question: str) -> str:
        raise NotImplementedError
