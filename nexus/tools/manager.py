"""
Project NEXUS
Tool Manager
"""

from nexus.tools.calculator import CalculatorTool
from nexus.tools.clock import ClockTool
from nexus.tools.filesystem import FileSystemTool


class ToolManager:
    """Manages all tools."""

    def __init__(self) -> None:
        self.tools = [
            ClockTool(),
            CalculatorTool(),
            FileSystemTool(),
        ]

    def execute(self, user_input: str) -> str | None:
        """Execute a matching tool."""

        for tool in self.tools:
            if tool.can_handle(user_input):
                return tool.execute(user_input)

        return None