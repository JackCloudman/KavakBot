from openai import BaseModel


class ChatBotResponse(BaseModel):
    response: str
