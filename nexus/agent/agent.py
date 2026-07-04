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

        # KNOWLEDGE_ROUTING_BYPASS_V1
        # 知識系コマンドは InputNormalizer により「ヘルプ」へ誤補正される可能性があるため、
        # 正規化前にKnowledgeToolへ渡す。
        knowledge_prefixes = (
            "知識ヘルプ",
            "知識カテゴリ",
            "知識一覧",
            "知識追加:",
            "知識追加：",
            "知識検索:",
            "知識検索：",
            "知識詳細:",
            "知識詳細：",
        )

        if stripped_input.startswith(knowledge_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # SOURCE_REGISTRY_ROUTING_BYPASS_V1
        # 情報源系コマンドはInputNormalizerより前に専用ツールへ渡す。
        source_prefixes = (
            "情報源ヘルプ",
            "情報源カテゴリ",
            "情報源一覧",
            "情報源追加:",
            "情報源追加：",
            "情報源検索:",
            "情報源検索：",
            "情報源詳細:",
            "情報源詳細：",
        )

        if stripped_input.startswith(source_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # WORLD_UPDATE_ROUTING_BYPASS_V1
        update_prefixes = (
            "更新ヘルプ",
            "知識更新状況",
            "更新ソース一覧",
            "更新ログ一覧",
            "更新ログ一覧:",
            "更新ログ一覧：",
            "更新ソース追加:",
            "更新ソース追加：",
            "世界情勢更新",
            "社会情勢更新",
            "AIニュース更新",
            "3DCGニュース更新",
            "開発ニュース更新",
        )

        if stripped_input.startswith(update_prefixes):
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
