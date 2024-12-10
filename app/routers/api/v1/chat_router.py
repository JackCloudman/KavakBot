from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.flows import get_chatbot_flow
from app.external.request.chatbot_request import ChatBotRequest
from app.external.response.chatbot_response import ChatBotResponse
from app.robot.flows.chatbot_flow_interface import ChatFlowInterface

router: APIRouter = APIRouter()


@router.post('/webhook/whatsappp', status_code=status.HTTP_200_OK, response_model=ChatBotResponse)
async def webhook(
        payload: ChatBotRequest,
        chatbot_flow: ChatFlowInterface = Depends(get_chatbot_flow),
):

    response: str = chatbot_flow.handle_message(
        phone_number=payload.phone_number,
        content=payload.message
    )

    return ChatBotResponse(response=response)
