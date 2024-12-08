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
    tree_xml: str = """
<?xml version="1.0" encoding="UTF-8"?>
<root BTCPP_format="3"
      main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <Sequence>
      <FetchConversationHistory/>
      <PreparePrompt/>
      <Fallback>
          <Repeat num_cycles="5">
            <Sequence>
              <CallOpenAI/>
              <ResponseHasFunctionCall/>
              <ExecuteFunction/>
            </Sequence>
          </Repeat>
        <UseResponse/>
      </Fallback>
    </Sequence>
  </BehaviorTree>

  <!-- Description of Node Models (used by Groot) -->
  <TreeNodesModel>
    <Action ID="CallOpenAI"
            editable="true"/>
    <Action ID="ExecuteFunction"
            editable="true"/>
    <Action ID="FetchConversationHistory"
            editable="true"/>
    <Action ID="PreparePrompt"
            editable="true"/>
    <Condition ID="ResponseHasFunctionCall"
               editable="true"/>
    <Action ID="UseResponse"
            editable="true"/>
  </TreeNodesModel>

</root>
    """  # TODO: Add the correct tree_xml content

    return ChatBotFlow(
        tree_xml=tree_xml,
        actions=actions,
    )
