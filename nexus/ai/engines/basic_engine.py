"""
Project NEXUS
Basic AI Engine
"""

from nexus.ai.engines.base_engine import BaseAIEngine
from nexus.memory.manager import MemoryManager
from nexus.core.logger import logger


class BasicAIEngine(BaseAIEngine):
    """Simple rule-based AI engine."""

    KNOWLEDGE_PATTERNS = {
        "私の名前は": ("name", "名前"),
        "私の好きな色は": ("favorite_color", "好きな色"),
        "私の趣味は": ("hobby", "趣味"),
    }

    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory

    def generate_response(self, user_input: str) -> str:
        logger.info(f"BasicAIEngine received input: {user_input}")

        text = user_input.strip()

        for prefix, (key, label) in self.KNOWLEDGE_PATTERNS.items():
            if text.startswith(prefix) and text.endswith("です"):
                value = text.replace(prefix, "").replace("です", "").strip()
                self.memory.save(key, value)
                return f"{label}は{value}ですね。覚えました。"

        if text == "私の名前は？":
            name = self.memory.recall("name")
            if name:
                return f"あなたの名前は{name}さんです。"
            return "まだあなたのお名前は教えてもらっていません。"

        if text == "私について教えて":
            name = self.memory.recall("name")
            color = self.memory.recall("favorite_color")
            hobby = self.memory.recall("hobby")

            response = "あなたについて知っている情報です。\n\n"

            if name:
                response += f"名前：{name}\n"

            if color:
                response += f"好きな色：{color}\n"

            if hobby:
                response += f"趣味：{hobby}\n"

            if not name and not color and not hobby:
                response += "まだ情報を覚えていません。"

            return response

        if text in ["こんにちは", "こんちは", "hello", "Hello"]:
            return "こんにちは。私はNEXUSです。"

        if text in ["おはよう", "おはようございます"]:
            return "おはようございます！"

        return "現在は基本応答モードです。"