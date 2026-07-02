"""
Project NEXUS
Basic AI Engine
"""

from nexus.ai.engines.base_engine import BaseAIEngine
from nexus.memory.manager import MemoryManager
from nexus.core.logger import logger


class BasicAIEngine(BaseAIEngine):
    """Simple rule-based AI engine."""

    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def generate_response(self, user_input: str) -> str:
        """Generate a simple local response."""

        logger.info(f"BasicAIEngine received input: {user_input}")

        text = user_input.strip()

        if text.startswith("私の名前は") and text.endswith("です"):
            name = text.replace("私の名前は", "").replace("です", "").strip()
            self.memory.save("name", name)
            return f"わかりました。あなたの名前は{name}さんですね。覚えました。"

        if text == "私の名前は？":
            name = self.memory.recall("name")

            if name:
                return f"あなたの名前は{name}さんです。"

            return "まだあなたのお名前は教えてもらっていません。"

        if text in ["こんにちは", "こんちは", "hello", "Hello"]:
            return "こんにちは。私はNEXUSです。"

        if text in ["おはよう", "おはようございます"]:
            return "おはようございます！"

        return "現在は基本応答モードです。"