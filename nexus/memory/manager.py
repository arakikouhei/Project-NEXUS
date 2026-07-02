"""
Project NEXUS
Memory Manager
"""

import json
from pathlib import Path

from nexus.core.logger import logger


class MemoryManager:
    """Handles memory storage and retrieval."""

    def __init__(self) -> None:
        self.status = "OFFLINE"

        self.memory_file = Path("data/memory.json")
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)

        self.memories = {}

        self.initialize()

    def initialize(self) -> None:
        """Initialize memory system."""

        self.status = "ONLINE"

        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.memories = json.load(f)

                logger.info("Memory loaded.")

            except Exception:
                self.memories = {}

        logger.info("Memory Manager initialized.")

    def save(self, key: str, value: str) -> None:
        """Save memory."""

        self.memories[key] = value

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=4)

        logger.info(f"Memory saved: {key} = {value}")

    def recall(self, key: str) -> str | None:
        """Recall memory."""

        return self.memories.get(key)

    def shutdown(self) -> None:
        """Shutdown memory."""

        self.status = "OFFLINE"

        logger.info("Memory Manager shutdown.")