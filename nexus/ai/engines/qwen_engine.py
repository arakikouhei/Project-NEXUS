"""
Project NEXUS
Qwen AI Engine
"""

import requests

from nexus.ai.engines.base_engine import BaseAIEngine


class QwenEngine(BaseAIEngine):
    """Engine for Ollama + Qwen."""

    def __init__(self) -> None:
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen3:latest"

    def generate_response(self, user_input: str) -> str:
        payload = {
            "model": self.model,
            "prompt": user_input,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            return data["response"].strip()

        except Exception as e:
            return f"Qwen Error: {e}"