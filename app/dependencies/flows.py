import os
from pathlib import Path
from typing import Dict

from fastapi import Depends

from app.dependencies.actions import get_actions
from app.entities.actions import ActionName
from app.robot.actions.action_interface import ActionInterface
from app.robot.flows.chatbot_flow import ChatBotFlow
from app.robot.flows.chatbot_flow_interface import ChatFlowInterface


def get_chatbot_flow(
        actions: Dict[ActionName, ActionInterface] = Depends(get_actions),
) -> ChatFlowInterface:
    config_path: str = os.getenv('CONFIG_PATH', 'configuration')
    root_dir: str = str(Path(__file__).resolve().parents[2])

    tree_absolute_path: str = os.path.join(root_dir, config_path)

    with open(f"{tree_absolute_path}/tree.xml") as file:
        tree_xml = file.read()

    return ChatBotFlow(
        tree_xml=tree_xml,
        actions=actions,
    )
