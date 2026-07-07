"""
Project NEXUS
Core System
"""

from config.settings import settings
from console import ConsoleInterface
from nexus.ai.manager import AIManager
from nexus.core.logger import logger


class NexusCore:
    """Main controller for Project NEXUS."""

    def __init__(self) -> None:
        self.project_name = settings.PROJECT_NAME
        self.version = settings.VERSION
        self.roadmap_stage = settings.ROADMAP_STAGE
        self.status = "OFFLINE"

        # ここで1つだけ生成する
        self.ai_manager = AIManager()
        self.console = ConsoleInterface(self.ai_manager)

    def boot(self) -> None:
        """Start the NEXUS Core."""

        self.status = "ONLINE"

        logger.info(f"{self.project_name} v{self.version} booted.")

        print("===================================")
        print(self.project_name)
        print("NEXUS Core")
        print(f"Version: {self.version}")
        print(f"Roadmap Stage: {self.roadmap_stage}")
        print(f"Status: {self.status}")
        print("===================================")

        self.ai_manager.initialize()
        self.console.start()