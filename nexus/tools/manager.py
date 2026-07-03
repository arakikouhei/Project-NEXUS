"""
Project NEXUS
Tool Manager
"""

from nexus.tools.base_tool import BaseTool
from nexus.tools.calculator import CalculatorTool
from nexus.tools.clock import ClockTool
from nexus.tools.filesystem import FileSystemTool
from nexus.tools.project import ProjectTool


class ToolManager:
    """Manages all tools."""

    def __init__(self) -> None:
        self.tools: list[BaseTool] = []

        self.register(ClockTool())
        self.register(CalculatorTool())
        self.register(FileSystemTool())
        self.register(ProjectTool())

    def register(self, tool: BaseTool) -> None:
        self.tools.append(tool)

    def execute(self, user_input: str) -> str | None:
        for tool in self.tools:
            if tool.can_handle(user_input):
                return tool.execute(user_input)

        return None