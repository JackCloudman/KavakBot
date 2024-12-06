from pydantic import BaseModel

from app.entities.roles import ChatRole


class Message(BaseModel):
    id: str
    name: str
    content: str
    role: ChatRole
