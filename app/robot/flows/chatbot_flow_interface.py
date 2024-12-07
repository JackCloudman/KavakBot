from abc import ABC, abstractmethod


class ChatFlowInterface(ABC):
    @abstractmethod
    def handle_message(self, phone_number: str, content: str) -> str:
        raise NotImplementedError
