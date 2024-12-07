from enum import Enum


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
    SYSTEM = "system"
