"""
Project NEXUS
App Control Tool
"""

from __future__ import annotations

import platform
import subprocess

from nexus.tools.base_tool import BaseTool


class AppControlTool(BaseTool):
    """Safely opens and quits allowed macOS apps."""

    name = "app_control"
    description = "許可されたMacアプリの起動・終了を行います"

    def __init__(self) -> None:
        self.allowed_apps = {
            "Chrome": "Google Chrome",
            "Google Chrome": "Google Chrome",
            "VS Code": "Visual Studio Code",
            "Visual Studio Code": "Visual Studio Code",
            "Finder": "Finder",
            "Maya": "Autodesk Maya",
            "Premiere": "Adobe Premiere Pro",
            "Premiere Pro": "Adobe Premiere Pro",
        }

    def can_handle(self, user_input: str) -> bool:
        return (
            user_input.endswith("を開いて")
            or user_input.endswith("を起動して")
            or user_input.endswith("を終了して")
            or user_input == "アプリ一覧"
        )

    def execute(self, user_input: str) -> str:
        if platform.system() != "Darwin":
            return "AppControlToolは現在macOS専用です。"

        if user_input == "アプリ一覧":
            names = sorted(self.allowed_apps.keys())
            return "## Allowed Apps\n\n" + "\n".join(f"- {name}" for name in names)

        if user_input.endswith("を開いて"):
            app_name = user_input.removesuffix("を開いて").strip()
            return self._open_app(app_name)

        if user_input.endswith("を起動して"):
            app_name = user_input.removesuffix("を起動して").strip()
            return self._open_app(app_name)

        if user_input.endswith("を終了して"):
            app_name = user_input.removesuffix("を終了して").strip()
            return self._quit_app(app_name)

        return "対応していないアプリ操作です。"

    def _resolve_app(self, app_name: str) -> str | None:
        return self.allowed_apps.get(app_name)

    def _open_app(self, app_name: str) -> str:
        resolved = self._resolve_app(app_name)

        if not resolved:
            return f"許可されていない、または未登録のアプリです: {app_name}"

        result = subprocess.run(
            ["open", "-a", resolved],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            return f"{resolved} を起動しました。"

        return f"{resolved} の起動に失敗しました。\n{result.stderr.strip()}"

    def _quit_app(self, app_name: str) -> str:
        resolved = self._resolve_app(app_name)

        if not resolved:
            return f"許可されていない、または未登録のアプリです: {app_name}"

        script = f'tell application "{resolved}" to quit'

        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            return f"{resolved} を終了しました。"

        return f"{resolved} の終了に失敗しました。\n{result.stderr.strip()}"
