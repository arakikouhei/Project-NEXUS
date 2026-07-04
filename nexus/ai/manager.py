"""
Project NEXUS
AI Manager
"""

from config.settings import settings
from nexus.ai.engines.basic_engine import BasicAIEngine
from nexus.ai.engines.qwen_engine import QwenEngine
from nexus.core.logger import logger
from nexus.memory.conversation import ConversationMemory
from nexus.memory.manager import MemoryManager
from nexus.tools.manager import ToolManager
from nexus.agent.agent import NexusAgent
from nexus.personality.response_dynamics import ResponseDynamicsCore
from nexus.personality.response_filter import ResponsePostProcessor

class AIManager:
    """Controls all AI interactions."""

    def __init__(self) -> None:
        self.status = "OFFLINE"
        self.memory = MemoryManager()
        self.conversation = ConversationMemory()
        self.agent = NexusAgent()
        self.response_dynamics = ResponseDynamicsCore()
        self.response_post_processor = ResponsePostProcessor()

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

        handled, result = self.agent.process(user_input)

        if handled:
            return result

        self.conversation.add("user", user_input)

        ai_input = self.response_dynamics.wrap_user_input(user_input)
        response = self.engine.generate_response(ai_input)
        response = self.response_post_processor.clean(response, user_input)

        self.conversation.add("assistant", response)

        return response

    def shutdown(self) -> None:
        self.status = "OFFLINE"
        logger.info("AI Manager shutdown.")