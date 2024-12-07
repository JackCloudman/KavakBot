from typing import List

from pydantic import BaseModel

from app.entities.message import Message


class Conversation(BaseModel):
    id: str
    phone_number: str
    messages: List[Message]

