"""
Project NEXUS
Agent
"""

from nexus.agent.planner import SimplePlanner
from nexus.core.input_normalizer import InputNormalizer
from nexus.tools.manager import ToolManager
from nexus.personality.response_dynamics import ResponseDynamicsCore


class NexusAgent:
    """Controls high-level thinking."""

    def __init__(self) -> None:
        self.tools = ToolManager()
        self.planner = SimplePlanner()
        self.response_dynamics = ResponseDynamicsCore()
        self.normalizer = InputNormalizer()

    def process(self, user_input: str) -> tuple[bool, str | None]:
        # VISION_ROUTING_BYPASS_V2
        # 画像系コマンドは InputNormalizer より前に VisionTool へ渡す。
        stripped_input = user_input.strip()
        vision_prefixes = (
            "画像ヘルプ",
            "vision help",
            "画像安全確認:",
            "画像安全確認：",
            "画像分析:",
            "画像分析：",
            "画像意味分析:",
            "画像意味分析：",
        )

        if stripped_input.startswith(vision_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

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
