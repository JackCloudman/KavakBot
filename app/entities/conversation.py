import uuid
from typing import Any, Dict, List

from pydantic import BaseModel, model_validator

from app.entities.message import Message


class Conversation(BaseModel):
    id: str
    phone_number: str
    messages: List[Message]

    @model_validator(mode='before')
    @classmethod
    def __fill_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get('id'):
            return values

        values['id'] = str(uuid.uuid4())
        return values
