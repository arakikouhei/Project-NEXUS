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
            "見せて",
        ]

        return any(word in user_input for word in keywords)

    def execute(self, user_input: str) -> str:
        root = Path(".")

        if "一覧" in user_input or "フォルダ一覧" in user_input:
            items = sorted(p.name for p in root.iterdir())
            return "\n".join(items)

        if "README" in user_input:
            return self._read_file(root / "README.md")

        if "main.py" in user_input:
            return self._read_file(root / "main.py")

        if "console.py" in user_input:
            return self._read_file(root / "console.py")

        return "操作を理解できませんでした。"

    def _read_file(self, path: Path) -> str:
        if not path.exists():
            return f"{path.name} が見つかりません。"

        if not path.is_file():
            return f"{path.name} はファイルではありません。"

        return path.read_text(encoding="utf-8")[:3000]