from unittest.mock import MagicMock

import pytest

from app.entities.tool import ToolName
from app.services.tools.tool_service import ToolService


class TestToolService:

    @pytest.fixture
    def tools(self):
        return {
            ToolName.SEARCH_CAR: MagicMock(),
        }

    @pytest.fixture
    def tool_service(self, tools):
        return ToolService(tools)

    def test_get_tool_existing(self, tool_service):
        tool = tool_service.get_tool(ToolName.SEARCH_CAR)
        assert tool is not None

    def test_get_tool_non_existing(self, tool_service):
        tool = tool_service.get_tool(ToolName.FINANCIAL_CALCULATOR)
        assert tool is None
