"""
Project NEXUS
Voice Tool
"""

import platform
import subprocess

from nexus.tools.base_tool import BaseTool


class VoiceTool(BaseTool):
    """Speaks short text on macOS using say."""

    name = "voice"
    description = "短い文章をMacで読み上げます"

    def can_handle(self, user_input: str) -> bool:
        return (
            user_input.startswith("読み上げ:")
            or user_input.startswith("読み上げ：")
            or user_input.startswith("話して:")
            or user_input.startswith("話して：")
        )

    def execute(self, user_input: str) -> str:
        text = self._extract_text(user_input)

        if not text:
            return "読み上げる文章がありません。"

        if len(text) > 120:
            return "安全のため、読み上げは120文字以内にしてください。"

        if platform.system() != "Darwin":
            return "VoiceToolは現在macOSのsayコマンド専用です。"

        try:
            subprocess.run(
                ["say", text],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            return f"読み上げました: {text}"
        except subprocess.TimeoutExpired:
            return "読み上げがタイムアウトしました。"
        except Exception as error:
            return f"読み上げ中にエラーが発生しました: {error}"

    def _extract_text(self, user_input: str) -> str:
        for separator in [":", "："]:
            if separator in user_input:
                return user_input.split(separator, 1)[1].strip()
        return ""
