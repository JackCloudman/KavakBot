import logging
import sys

from examples.KavakBot.app.components.logger.logger_interface import \
    LoggerInterface


class Logger(LoggerInterface):
    def __init__(self, log_format: str, log_level: str, stream=None, propagate: bool = False):
        self._log_formatter = logging.Formatter(log_format)
        self._log_level = self._get_level(log_level)
        self._stream = stream or sys.stdout
        self._propagate = propagate

    def _get_level(self, log_level: str) -> int:
        level = log_level.upper()
        numeric_level = getattr(logging, level, None)
        if isinstance(numeric_level, int):
            return numeric_level
        else:
            return logging.WARNING

    def _get_console_handler(self) -> logging.StreamHandler:
        console_handler = logging.StreamHandler(self._stream)
        console_handler.setFormatter(self._log_formatter)
        return console_handler

    def get_logger(self, logger_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        logger.propagate = self._propagate
        logger.setLevel(self._log_level)

        if not logger.handlers:
            logger.addHandler(self._get_console_handler())

        return logger
