from enum import Enum
from typing import Callable


class ToolName(str, Enum):
    SEARCH_CAR = "search_car"
    FINANCIAL_CALCULATOR = "financial_calculator"


class Tool:
    def __init__(self, name: ToolName, tool: Callable):
        self.name = name
        self.tool = tool

    def __call__(self, *args, **kwargs):
        return self.tool(*args, **kwargs)
