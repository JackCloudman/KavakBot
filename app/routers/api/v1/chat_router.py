from fastapi import APIRouter, Depends

from app.dependencies.flows import get_chatbot_flow

from app.external.request.chatbot_request import ChatBotRequest
from app.robot.flows.chatbot_flow_interface import ChatFlowInterface

router: APIRouter = APIRouter()


@router.post('/webhook/whatsappp')
async def webhook(
        payload: ChatBotRequest,
        chatbot_flow: ChatFlowInterface = Depends(get_chatbot_flow),
):
    return {"response": chatbot_flow.handle_message(
        phone_number=payload.phone_number,
        content=payload.message
    )

    }
