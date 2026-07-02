"""
Project NEXUS
Console Interface
"""

from nexus.ai.manager import AIManager
from nexus.core.logger import logger


class ConsoleInterface:
    """Text-based interface for Project NEXUS."""

    def __init__(self) -> None:
        self.running = False
        self.ai_manager = AIManager()

    def start(self) -> None:
        """Start console interface."""
        self.running = True

        logger.info("Console Interface started.")

        print("\nNEXUS Console Online")
        print("Type 'exit' to shutdown.\n")

        while self.running:
            user_input = input("You > ")

            if user_input.lower() in ["exit", "quit"]:
                self.stop()
                break

            self.respond(user_input)

    def respond(self, user_input: str) -> None:
        """Send input to AI Manager."""

        logger.info(f"User input: {user_input}")

        response = self.ai_manager.generate_response(user_input)

        print(f"NEXUS > {response}\n")

    def stop(self) -> None:
        """Stop console interface."""

        self.running = False

        logger.info("Console Interface stopped.")

        print("\nNEXUS Console Offline")