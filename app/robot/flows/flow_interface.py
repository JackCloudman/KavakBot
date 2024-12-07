from abc import ABC, abstractmethod


class FlowInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError
