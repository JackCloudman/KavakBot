from typing import Dict, List

import behavior_tree_cpp as bt
from openai import OpenAI

from app.robot.actions.action_interface import ActionInterface


class CallOpenAIAction(ActionInterface):
    def __init__(self, model_name: str, functions: List[Dict], openai_client: OpenAI):
        self._model_name: str = model_name
        self._openai_client: OpenAI = openai_client
        self._functions: List[Dict] = functions

    def execute(self, blackboard: bt.Blackboard) -> str:
        openai_payload = blackboard.get('openai_payload')
        try:
            response = self._openai_client.chat.completions.create(
                model=self._model_name,
                messages=openai_payload,
                functions=self._functions
            )

            blackboard.set('openai_response', response)
            return "SUCCESS"
        except Exception as e:
            print(e)
            blackboard.set('error', str(e))
            return "FAILURE"
