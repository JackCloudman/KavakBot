import uuid
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field, model_validator

from app.entities.message import Message


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    phone_number: str
    messages: List[Message]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="before")
    @classmethod
    def __fill_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get("id"):
            return values

        values["id"] = str(uuid.uuid4())
        return values

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        messages = [msg.to_str() for msg in self.messages]
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "messages": messages,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
