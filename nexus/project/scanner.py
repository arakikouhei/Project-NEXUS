"""
Project NEXUS
Project Scanner
"""

from pathlib import Path


class ProjectScanner:
    """Scans the project directory."""

    def __init__(self, root: str = ".") -> None:
        self.root = Path(root)

    def scan(self) -> list[str]:
        """Return a list of all project files."""

        files = []

        ignore_dirs = {
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            ".idea",
            ".vscode",
        }

        ignore_suffixes = {
             ".pyc",
        }

        for path in self.root.rglob("*"):

            # フォルダを無視
            if any(part in ignore_dirs for part in path.parts):
                continue

            # ファイルだけ対象
            if not path.is_file():
                continue

            # 拡張子を無視
            if path.suffix in ignore_suffixes:
                continue

            files.append(str(path))

        return sorted(files)