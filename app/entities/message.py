from pydantic import BaseModel

from app.entities.chat_role import ChatRole


class Message(BaseModel):
    id: str
    name: str
    content: str
    role: ChatRole
