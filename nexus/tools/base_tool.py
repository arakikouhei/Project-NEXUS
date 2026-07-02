"""
Project NEXUS
Base Tool
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Base class for all tools."""

    name: str = ""
    description: str = ""

    @abstractmethod
    def can_handle(self, user_input: str) -> bool:
        """Return True if this tool can handle the request."""
        pass

    @abstractmethod
    def execute(self, user_input: str) -> str:
        """Execute the tool."""
        pass