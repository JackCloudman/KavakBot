from typing import Callable, Dict

import behavior_tree_cpp as bt

from app.entities.actions import ActionName
from app.entities.message import Message
from app.robot.actions.action_interface import ActionInterface
from app.robot.flows.chatbot_flow_interface import ChatFlowInterface


class ChatBotFlow(ChatFlowInterface):
    def __init__(self,
                 tree_xml: str,
                 actions: Dict[ActionName, ActionInterface],
                 ) -> None:
        self._tree_xml: str = tree_xml
        self._factory = bt.BehaviorTreeFactory()
        self._blackboard = bt.Blackboard.create()

        for action_name, action in actions.items():
            self._factory.register_simple_action(action_name, action.execute)

    def handle_message(self, phone_number: str, content: str) -> str:

        self._blackboard.set('phone_number', phone_number)
        self._blackboard.set('message', Message(
            name=phone_number, content=content))

        # Create tree
        tree: bt.Tree = self._factory.create_tree_from_text(
            self._tree_xml, self._blackboard)

        logger = bt.StdCoutLogger(tree)

        # Ejecutar el árbol de comportamiento
        status = tree.tick_root()
        return self._blackboard.get('final_response')
