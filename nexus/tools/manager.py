"""
Project NEXUS
Tool Manager
"""

from nexus.tools.base_tool import BaseTool
from nexus.tools.clock import ClockTool
from nexus.tools.terminal import TerminalTool
from nexus.tools.calculator import CalculatorTool
from nexus.tools.filesystem import FileSystemTool
from nexus.tools.project import ProjectTool
from nexus.tools.code import CodeTool


class ToolManager:
    """Manages all tools."""

    def __init__(self) -> None:
        self.tools: list[BaseTool] = []

        # TerminalToolはCalculatorToolより先に置く
        # 理由: "ls nexus/tools" の "/" や "git log -5" の "-5" を
        # CalculatorToolが誤って拾うのを防ぐため
        self.register(ClockTool())
        self.register(TerminalTool())
        self.register(CalculatorTool())
        self.register(FileSystemTool())
        self.register(ProjectTool())
        self.register(CodeTool())

    def register(self, tool: BaseTool) -> None:
        self.tools.append(tool)

    def execute(self, user_input: str) -> str | None:
        for tool in self.tools:
            if tool.can_handle(user_input):
                return tool.execute(user_input)

        return None