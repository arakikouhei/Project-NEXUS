"""
Project NEXUS
Qwen AI Engine
"""

import requests

from nexus.ai.engines.base_engine import BaseAIEngine
from nexus.memory.manager import MemoryManager


class QwenEngine(BaseAIEngine):
    """Engine for Ollama + Qwen."""

    def __init__(self, memory: MemoryManager | None = None) -> None:
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen3:latest"
        self.memory = memory

    def generate_response(self, user_input: str) -> str:
        prompt = self._build_prompt(user_input)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()

            data = response.json()
            return data["response"].strip()

        except Exception as e:
            return f"Qwen Error: {e}"

    def _build_prompt(self, user_input: str) -> str:
        memory_text = ""

        if self.memory:
            name = self.memory.recall("name")
            color = self.memory.recall("favorite_color")
            hobby = self.memory.recall("hobby")

            memory_lines = []

            if name:
                memory_lines.append(f"- 名前: {name}")
            if color:
                memory_lines.append(f"- 好きな色: {color}")
            if hobby:
                memory_lines.append(f"- 趣味: {hobby}")

            if memory_lines:
                memory_text = "\n".join(memory_lines)

        return f"""
あなたはProject NEXUSという、ユーザー専用のAIアシスタントです。
日本語で、自然で親しみやすく答えてください。

ユーザーについて知っている情報:
{memory_text if memory_text else "まだ情報はありません。"}

ユーザーの発言:
{user_input}
"""