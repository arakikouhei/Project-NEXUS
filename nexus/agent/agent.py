"""
Project NEXUS
Agent
"""

from nexus.agent.planner import SimplePlanner
from nexus.core.input_normalizer import InputNormalizer
from nexus.tools.manager import ToolManager


class NexusAgent:
    """Controls high-level thinking."""

    def __init__(self) -> None:
        self.tools = ToolManager()
        self.planner = SimplePlanner()
        self.normalizer = InputNormalizer()

    def process(self, user_input: str) -> tuple[bool, str | None]:
        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)

        if result is not None:
            if normalized.corrected:
                return (
                    True,
                    f"入力補正: {normalized.original} → {normalized.text}\n\n{result}",
                )

            return True, result

        return False, None

    def plan(self, user_input: str) -> list[str]:
        normalized = self.normalizer.normalize(user_input)
        return self.planner.plan(normalized.text)
