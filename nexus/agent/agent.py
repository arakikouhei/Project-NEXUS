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
    def plan(self, user_input: str) -> list[str]:
        """Create a simple execution plan."""

        plan = []

        if "解析" in user_input and ".py" not in user_input:
            plan.append("project")
            plan.append("code")

        return plan