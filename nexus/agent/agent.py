"""
Project NEXUS
Agent
"""

from nexus.tools.manager import ToolManager


class NexusAgent:
    """Controls high-level thinking."""

    def __init__(self) -> None:
        self.tools = ToolManager()

    def process(self, user_input: str) -> tuple[bool, str | None]:
        """
        Returns:
            (True, result)  -> Tool handled it
            (False, None)   -> Send to AI
        """

        result = self.tools.execute(user_input)

        if result is not None:
            return True, result

        return False, None