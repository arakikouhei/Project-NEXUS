"""
Project NEXUS
AI Manager
"""

from nexus.ai.engines.basic_engine import BasicAIEngine
from nexus.core.logger import logger


class AIManager:
    """Controls all AI interactions."""

    def __init__(self) -> None:
        self.model_name = "BasicLocalResponder"
        self.status = "OFFLINE"
        self.engine = BasicAIEngine()

    def initialize(self) -> None:
        self.status = "ONLINE"
        logger.info("AI Manager initialized.")
        print("[AI] Manager Online")

    def generate_response(self, user_input: str) -> str:
        logger.info("Generating AI response...")
        return self.engine.generate_response(user_input)

    def shutdown(self) -> None:
        self.status = "OFFLINE"
        logger.info("AI Manager shutdown.")