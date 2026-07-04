"""
Project NEXUS
Context Tool
"""

from nexus.context.builder import ContextBuilder
from nexus.tools.base_tool import BaseTool


class ContextTool(BaseTool):
    """Shows current NEXUS context."""

    name = "context"
    description = "現在のNEXUSの状況を表示します"

    def __init__(self) -> None:
        self.builder = ContextBuilder()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "nexus状況",
            "状況確認",
            "今の状態",
            "context",
            "コンテキスト",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        context = self.builder.build()

        lines = [
            "## NEXUS Context",
            "",
            f"Project: {context['project']}",
            f"Version: {context['version']}",
            f"Working Directory: {context['working_directory']}",
            f"Git Branch: {context['git_branch']}",
            f"Git Status: {context['git_status']}",
            "",
        ]

        logs = context.get("recent_terminal_logs", [])
        if logs:
            lines.append("Recent Terminal Logs:")
            for log in logs:
                lines.append(f"- {log}")
        else:
            lines.append("Recent Terminal Logs: none")

        return "\n".join(lines)
