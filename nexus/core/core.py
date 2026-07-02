"""
Project NEXUS
Core System
"""

from config.settings import settings
from nexus.ai.manager import AIManager
from nexus.core.logger import logger


class NexusCore:
    """Main controller for Project NEXUS."""

    def __init__(self) -> None:
        self.project_name = settings.PROJECT_NAME
        self.version = settings.VERSION
        self.status = "OFFLINE"
        self.ai_manager = AIManager()

    def boot(self) -> None:
        """Start the NEXUS Core."""
        self.status = "ONLINE"

        logger.info(f"{self.project_name} v{self.version} booted.")

        print("===================================")
        print(f"{self.project_name}")
        print("NEXUS Core")
        print(f"Version: {self.version}")
        print(f"Status: {self.status}")
        print("===================================")

        self.ai_manager.initialize()