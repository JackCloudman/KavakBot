import behavior_tree_cpp as bt

from app.robot.actions.action_interface import ActionInterface


class UseResponseAction(ActionInterface):
    def execute(self, blackboard: bt.Blackboard) -> str:
        try:
            response = blackboard.get('openai_response')
            final_response = response.choices[0].message.content
            blackboard.set('final_response', final_response)
            return "SUCCESS"
        except Exception as e:
            print(f"Error getting response: {e}")
            return "FAILURE"
