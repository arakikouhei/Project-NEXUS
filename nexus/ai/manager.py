"""
Project NEXUS
AI Manager
"""

from config.settings import settings
from nexus.ai.engines.basic_engine import BasicAIEngine
from nexus.ai.engines.qwen_engine import QwenEngine
from nexus.core.logger import logger
from nexus.memory.manager import MemoryManager


class AIManager:
    """Controls all AI interactions."""

    def __init__(self) -> None:
        self.status = "OFFLINE"
        self.memory = MemoryManager()

        # 設定ファイルから使用するAIを選択
        if settings.AI_ENGINE == "basic":
            self.model_name = "BasicLocalResponder"
            self.engine = BasicAIEngine(self.memory)

        elif settings.AI_ENGINE == "qwen":
            self.model_name = "Qwen"
            self.engine = QwenEngine(self.memory)

        else:
            raise ValueError(f"Unknown AI engine: {settings.AI_ENGINE}")

    def initialize(self) -> None:
        self.status = "ONLINE"

        logger.info(f"AI Manager initialized. Engine: {self.model_name}")
        print(f"[AI] {self.model_name} Online")

    def generate_response(self, user_input: str) -> str:
        logger.info("Generating AI response...")
        return self.engine.generate_response(user_input)

    def shutdown(self) -> None:
        self.status = "OFFLINE"
        logger.info("AI Manager shutdown.")