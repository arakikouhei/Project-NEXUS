"""
Project NEXUS
System Tool
"""

import platform
import shutil
import sys
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class SystemTool(BaseTool):
    """Shows safe system information."""

    name = "system"
    description = "安全なシステム情報を表示します"

    def __init__(self) -> None:
        self.root = Path.cwd()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "システム情報",
            "system info",
            "python情報",
            "容量確認",
            "環境確認",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        disk = shutil.disk_usage(self.root)

        return (
            "## System Info\n\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Machine: {platform.machine()}\n"
            f"Python: {sys.version.split()[0]}\n"
            f"Project Root: {self.root}\n"
            f"Disk Free: {disk.free // (1024 ** 3)} GB\n"
        )
