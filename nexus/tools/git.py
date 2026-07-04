"""
Project NEXUS
Git Tool
"""

import subprocess
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class GitTool(BaseTool):
    """Handles safe Git read-only commands."""

    name = "git"
    description = "Gitの状態を安全に確認します"

    def __init__(self) -> None:
        self.working_directory = Path.cwd()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "git状態",
            "git status",
            "変更確認",
            "差分確認",
            "最近のコミット",
            "コミット履歴",
            "ブランチ確認",
            "今のブランチ",
        }

        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        if "git状態" in user_input or "git status" in user_input:
            return self._run_git_command(
                ["git", "status"],
                "Git Status",
            )

        if "変更確認" in user_input or "差分確認" in user_input:
            return self._run_git_command(
                ["git", "diff", "--stat"],
                "Git Diff Summary",
            )

        if "最近のコミット" in user_input or "コミット履歴" in user_input:
            return self._run_git_command(
                ["git", "log", "--oneline", "-5"],
                "Recent Commits",
            )

        if "ブランチ確認" in user_input or "今のブランチ" in user_input:
            return self._run_git_command(
                ["git", "branch", "--show-current"],
                "Current Branch",
            )

        return "対応していないGit操作です。"

    def _run_git_command(self, command: list[str], title: str) -> str:
        try:
            result = subprocess.run(
                command,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if output:
                return f"## {title}\n\n{output}"

            if error:
                return f"## {title}\n\n{error}"

            return f"## {title}\n\n出力はありません。"

        except subprocess.TimeoutExpired:
            return "Gitコマンドがタイムアウトしました。"

        except Exception as error:
            return f"GitToolでエラーが発生しました: {error}"