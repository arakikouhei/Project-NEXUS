"""
Project NEXUS
Basic AI Engine

Temporary local response engine before connecting real LLM models.
"""

from nexus.ai.engines.base_engine import BaseAIEngine
from nexus.core.logger import logger


class BasicAIEngine(BaseAIEngine):
    """Simple rule-based AI engine."""

    def generate_response(self, user_input: str) -> str:
        """Generate a simple local response."""

        logger.info(f"BasicAIEngine received input: {user_input}")

        text = user_input.strip()

        if not text:
            return "入力が空です。何か話しかけてください。"

        if text in ["こんにちは", "こんちは", "hello", "Hello"]:
            return "こんにちは。私はNEXUSです。現在は基本応答モードで動作しています。"

        if text in ["おはよう", "おはようございます"]:
            return "おはようございます。今日もProject NEXUSを起動してくれてありがとう。"

        if text in ["何ができる？", "今何ができる？"]:
            return "現在は文字入力、ログ記録、設定読み込み、AI Manager、Basic AI Engineが動作しています。"

        return "現在は基本応答モードです。将来ここにローカルAIモデルを接続します。"