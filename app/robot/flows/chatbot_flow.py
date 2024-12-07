from typing import Callable, Dict

import behavior_tree_cpp as bt

from app.entities.actions import ActionName
from app.entities.message import Message


class ChatBotFlow:
    def __init__(self,
                 tree_xml: str,
                 actions: Dict[ActionName, Callable],
                 ) -> None:
        self._factory = bt.BehaviorTreeFactory()
        self._blackboard = bt.Blackboard.create()

        for action_name, action in actions.items():
            self._factory.register_simple_action(action_name, action)

        self._tree_xml: str = tree_xml

    def handle_message(self, phone_number: str, content: str) -> str:
        self._blackboard.set('phone_number', phone_number)
        self._blackboard.set('message', Message(
            name=phone_number, content=content))

        # Create tree
        tree = self._factory.create_tree_from_xml(
            self._tree_xml, self._blackboard)

        # Tick tree
        tree.tick_root()

        final_response: str = self._blackboard.get(
            'final_response') or "Error processing message"

        return final_response
