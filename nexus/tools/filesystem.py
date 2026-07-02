"""
Project NEXUS
File System Tool
"""

from pathlib import Path

from nexus.tools.base_tool import BaseTool


class FileSystemTool(BaseTool):
    """Read files and list directories."""

    name = "filesystem"
    description = "ファイルやフォルダを操作します"

    def can_handle(self, user_input: str) -> bool:
        keywords = [
            "一覧",
            "フォルダ",
            "ディレクトリ",
            "開いて",
            "読んで",
        ]

        return any(word in user_input for word in keywords)

    def execute(self, user_input: str) -> str:
        root = Path(".")

        # フォルダ一覧
        if "一覧" in user_input or "フォルダ" in user_input:
            items = sorted(p.name for p in root.iterdir())
            return "\n".join(items)

        # READMEを読む
        if "README" in user_input:
            path = root / "README.md"

            if path.exists():
                return path.read_text(encoding="utf-8")[:2000]

            return "README.md が見つかりません。"

        return "操作を理解できませんでした。"