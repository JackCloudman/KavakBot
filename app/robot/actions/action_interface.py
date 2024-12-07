from abc import ABC, abstractmethod

import behavior_tree_cpp as bt


class ActionInterface(ABC):
    @abstractmethod
    def execute(self, blackboard: bt.Blackboard) -> str:
        raise NotImplementedError
