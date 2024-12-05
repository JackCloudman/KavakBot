import logging
from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    @abstractmethod
    def get_logger(self, logger_name: str) -> logging.Logger:
        raise NotImplementedError
