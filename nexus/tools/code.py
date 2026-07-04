"""
Project NEXUS
Code Tool
"""

from pathlib import Path

from nexus.code.reader import CodeReader
from nexus.tools.base_tool import BaseTool


class CodeTool(BaseTool):
    """Analyze Python source files."""

    name = "code"
    description = "Pythonコードを解析します"

    def __init__(self) -> None:
        self.reader = CodeReader()

    def can_handle(self, user_input: str) -> bool:
        keywords = [
            "解析",
            "分析",
        ]

        return (
            any(word in user_input for word in keywords)
            and ".py" in user_input
        )

    def execute(self, user_input: str) -> str:
        for word in ["解析して", "解析", "分析して", "分析"]:
            user_input = user_input.replace(word, "")

        filename = user_input.strip()

        path = Path(filename)

        if not path.exists():
            return f"{filename} が見つかりません。"

        return self.reader.analyze_file(path)
