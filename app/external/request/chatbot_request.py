from pydantic import BaseModel


class ChatBotRequest(BaseModel):
    message: str
    phone_number: str
