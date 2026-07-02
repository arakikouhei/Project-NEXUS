"""
Project NEXUS
Memory Manager
"""

from nexus.core.logger import logger


class MemoryManager:
    """Handles memory storage and retrieval."""

    def __init__(self) -> None:
        self.status = "OFFLINE"
        self.memories = {}

    def initialize(self) -> None:
        """Initialize memory system."""
        self.status = "ONLINE"

        logger.info("Memory Manager initialized.")
        print("[Memory] Manager Online")

    def save(self, key: str, value: str) -> None:
        """Save a memory."""
        self.memories[key] = value
        logger.info(f"Memory saved: {key} = {value}")

    def recall(self, key: str) -> str | None:
        """Recall a memory."""
        return self.memories.get(key)

    def shutdown(self) -> None:
        """Shutdown memory system."""
        self.status = "OFFLINE"
        logger.info("Memory Manager shutdown.")