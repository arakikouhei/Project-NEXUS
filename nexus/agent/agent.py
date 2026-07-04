"""
Project NEXUS
Agent
"""

from nexus.agent.planner import SimplePlanner
from nexus.tools.manager import ToolManager


class NexusAgent:
    """Controls high-level thinking."""

    def __init__(self) -> None:
        self.tools = ToolManager()
        self.planner = SimplePlanner()

    def process(self, user_input: str) -> tuple[bool, str | None]:
        result = self.tools.execute(user_input)

        if result is not None:
            return True, result

        return False, None

    def plan(self, user_input: str) -> list[str]:
        return self.planner.plan(user_input)
