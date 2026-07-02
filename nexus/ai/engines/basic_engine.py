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
        logger.info(f"BasicAIEngine received input: {user_input}")

        text = user_input.strip()

        if text.startswith("私の名前は") and text.endswith("です"):
            name = text.replace("私の名前は", "").replace("です", "").strip()
            self.memory.save("name", name)
            return f"わかりました。あなたの名前は{name}さんですね。覚えました。"

        if text.startswith("私の好きな色は") and text.endswith("です"):
            color = text.replace("私の好きな色は", "").replace("です", "").strip()
            self.memory.save("favorite_color", color)
            return f"好きな色は{color}ですね。覚えました。"

        if text.startswith("私の趣味は") and text.endswith("です"):
            hobby = text.replace("私の趣味は", "").replace("です", "").strip()
            self.memory.save("hobby", hobby)
            return f"趣味は{hobby}ですね。覚えました。"

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