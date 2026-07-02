"""
Project NEXUS
Console Interface
"""

from nexus.core.logger import logger


class ConsoleInterface:
    """Text-based interface for Project NEXUS."""

    def __init__(self) -> None:
        self.running = False

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
        """Respond to user input."""
        logger.info(f"User input: {user_input}")

        print("NEXUS > 現在AIは未接続です。")
        print("NEXUS > でも、会話インターフェースは正常に動作しています。\n")

    def stop(self) -> None:
        """Stop console interface."""
        self.running = False
        logger.info("Console Interface stopped.")
        print("\nNEXUS Console Offline")