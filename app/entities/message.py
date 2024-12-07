import uuid
from typing import Any, Dict

from pydantic import BaseModel, model_validator

from app.entities.chat_role import ChatRole


class Message(BaseModel):
    id: str
    name: str
    content: str
    role: ChatRole = ChatRole.USER

    @model_validator(mode='before')
    @classmethod
    def __fill_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get('id'):
            return values

        values['id'] = str(uuid.uuid4())
        return values
