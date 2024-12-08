from datetime import datetime
from typing import Dict, List

import behavior_tree_cpp as bt

from app.entities.chat_role import ChatRole
from app.entities.conversation import Conversation
from app.entities.message import Message
from app.robot.actions.action_interface import ActionInterface


class PreparePromptAction(ActionInterface):
    def __init__(self, system_prompt: str) -> None:
        self._system_prompt: str = system_prompt

    def execute(self, blackboard: bt.Blackboard) -> str:
        conversation: Conversation = blackboard.get('conversation')

        history_chat: str = ""
        last_message: Message = conversation.messages.pop()
        current_date: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        for m in conversation.messages:
            history_chat += f"{m.role}: {m.content}\n"

        prompt: str = f"{self._system_prompt}\n{history_chat}" if history_chat else self._system_prompt
        prompt += f"\nCurrent date: {current_date}"
        openai_payload: List[Dict] = [
            {
                "role": ChatRole.SYSTEM,
                "content": prompt,

            },
            {
                "role": ChatRole.USER,
                "content": [
                    {
                        "text": f"{last_message.content}",
                        "type": "text"
                    }
                ]
            }
        ]

        blackboard.set('openai_payload', openai_payload)

        # Rollback last message
        conversation.messages.append(last_message)
        blackboard.set('conversation', conversation)

        return "SUCCESS"
