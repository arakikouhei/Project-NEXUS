"""
Project NEXUS
Dashboard Tool
"""

from nexus.context.builder import ContextBuilder
from nexus.tools.base_tool import BaseTool


class DashboardTool(BaseTool):
    """Shows a NEXUS dashboard."""

    name = "dashboard"
    description = "NEXUSのダッシュボードを表示します"

    def __init__(self) -> None:
        self.builder = ContextBuilder()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "ダッシュボード",
            "nexusダッシュボード",
            "ホーム",
            "ホーム画面",
            "現在のまとめ",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        context = self.builder.build()

        lines = [
            "## NEXUS Dashboard",
            "",
            f"Stage: {context['stage']}",
            f"Version: {context['version']}",
            f"Git: {context['git_branch']} / {context['git_status']}",
            f"Hardware Mode: {context['hardware_mode']}",
            f"Sphere Ready: {context['sphere_ready']}",
            "",
            "Available Core Commands:",
            "- nexus状況",
            "- システム情報",
            "- git要約",
            "- コミット準備",
            "- テスト実行",
            "- ハードウェア状態",
            "- 作業ログ",
            "- できること",
            "",
        ]

        worklog = context.get("recent_worklog", [])
        if worklog:
            lines.append("Recent Work Log:")
            for item in worklog:
                lines.append(f"- {item}")
        else:
            lines.append("Recent Work Log: none")

        return "\n".join(lines)
