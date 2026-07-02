"""
Project NEXUS
Base AI Engine

Defines the interface that all AI engines must follow.
"""

from abc import ABC, abstractmethod


class BaseAIEngine(ABC):
    """Abstract base class for all AI engines."""

    @abstractmethod
    def generate_response(self, user_input: str) -> str:
        """Generate a response from user input."""
        raise NotImplementedError