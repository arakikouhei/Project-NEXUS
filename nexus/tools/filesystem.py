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
        text = user_input.strip()

        # アプリ系はAppControlTool専用
        if text.startswith((
            "アプリ",
            "Chrome",
            "Google Chrome",
            "VS Code",
            "Visual Studio Code",
            "Finder",
            "Maya",
            "Premiere",
            "Premiere Pro",
        )):
            return False

        keywords = [
            "フォルダ一覧",
            "README",
            "main.py",
            "console.py",
        ]

        return any(word in text for word in keywords)
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
