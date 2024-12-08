
from pydantic import BaseModel

from app.entities.chat_role import ChatRole


class Message(BaseModel):
    content: str
    role: ChatRole = ChatRole.USER

    def to_str(self) -> str:
        return f"{self.role}: {self.content}"

    @staticmethod
    def from_str(message: str) -> 'Message':
        role, content = message.split(": ", 1)
        return Message(role=ChatRole(role.strip()), content=content.strip())
