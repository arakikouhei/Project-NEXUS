"""
Project NEXUS
Console Interface
"""

from nexus.ai.manager import AIManager
from nexus.core.logger import logger


class ConsoleInterface:
    """Text-based interface for Project NEXUS."""

    def __init__(self, ai_manager: AIManager) -> None:
        self.running = False
        self.ai_manager = ai_manager

    def start(self) -> None:
        self.running = True
        logger.info("Console Interface started.")

        print("\nNEXUS Console Online")
        print("Type 'exit' to shutdown.\n")

        while self.running:
            try:
                user_input = input("You > ").strip()

                if not user_input:
                    continue

                if user_input.lower() in {"exit", "quit", "q"} or user_input in {"終了", "終わり"}:
                    self.stop()
                    break

                self.respond(user_input)

            except KeyboardInterrupt:
                self.stop()
                break

    def respond(self, user_input: str) -> None:
        logger.info(f"User input: {user_input}")

        response = self.ai_manager.generate_response(user_input)

        print(f"NEXUS > {response}\n")

    def stop(self) -> None:
        self.running = False
        logger.info("Console Interface stopped.")
        print("\nNEXUS Console Offline")