import behavior_tree_cpp as bt

from app.robot.actions.action_interface import ActionInterface


class HasToolCall(ActionInterface):
    def execute(self, blackboard: bt.Blackboard) -> str:
        response = blackboard.get('openai_response')
        if response and response.choices[0].message.function_call:
            return "SUCCESS"
        else:
            return "FAILURE"
