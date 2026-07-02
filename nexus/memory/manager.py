"""
Project NEXUS
Memory Manager

Responsible for long-term memory management.
"""

from nexus.core.logger import logger


class MemoryManager:
    """Handles memory storage and retrieval."""

    def __init__(self) -> None:
        self.status = "OFFLINE"
        self.memory_count = 0

    def initialize(self) -> None:
        """Initialize memory system."""

        self.status = "ONLINE"

        logger.info("Memory Manager initialized.")

        print("[Memory] Manager Online")

    def save_memory(self, text: str) -> None:
        """Save memory."""

        self.memory_count += 1

        logger.info(f"Memory Saved: {text}")

    def shutdown(self) -> None:
        """Shutdown memory system."""

        self.status = "OFFLINE"

        logger.info("Memory Manager shutdown.")