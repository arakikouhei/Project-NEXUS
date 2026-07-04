"""
Project NEXUS
Capability Tool
"""

from nexus.tools.base_tool import BaseTool


class CapabilityTool(BaseTool):
    """Shows what NEXUS can do."""

    name = "capability"
    description = "NEXUSのできることを表示します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        # 画像系ヘルプはVisionTool専用
        if text.startswith(("画像", "vision")):
            return False

        keywords = [
            "できること",
            "機能一覧",
            "ヘルプ",
            "使い方",
            "何ができる",
        ]

        return text in keywords
    def execute(self, user_input: str) -> str:
        return (
            "## NEXUS Capabilities\n\n"
            "現在のNEXUSは Pre-Sphere Core 段階です。\n\n"
            "### 状態確認\n"
            "- nexus状況\n"
            "- ダッシュボード\n"
            "- システム情報\n"
            "- ハードウェア状態\n"
            "- 球体準備\n\n"
            "### Git\n"
            "- git要約\n"
            "- git状態\n"
            "- 変更確認\n"
            "- 最近のコミット\n"
            "- コミット準備\n"
            "- コミットして: メッセージ\n\n"
            "### Terminal\n"
            "- pwd\n"
            "- ls\n"
            "- ls nexus/tools\n"
            "- git log --oneline -5\n\n"
            "### Self Test\n"
            "- テスト実行\n\n"
            "### Work Log\n"
            "- 作業記録: 内容\n"
            "- 作業ログ\n\n"
            "### Voice\n"
            "- 読み上げ: テキスト\n\n"
            "### Project / Code\n"
            "- AIManagerはどこ？\n"
            "- nexus/tools/git.pyを解析して\n"
        )
