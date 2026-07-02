"""
Project NEXUS
Clock Tool
"""

from datetime import datetime

from nexus.tools.base_tool import BaseTool


class ClockTool(BaseTool):
    """Returns the current local time."""

    name = "clock"
    description = "現在時刻を取得します"

    def can_handle(self, user_input: str) -> bool:
        return "今何時" in user_input or "現在時刻" in user_input

    def execute(self, user_input: str = "") -> str:
        now = datetime.now()
        return now.strftime("現在時刻は %Y-%m-%d %H:%M:%S です。")