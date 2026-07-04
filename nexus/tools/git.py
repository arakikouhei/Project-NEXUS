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
            "git要約",
            "変更まとめ",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        if "git要約" in user_input or "変更まとめ" in user_input:
            return self._summarize_git_status()

        if "git状態" in user_input or "git status" in user_input:
            return self._run_git_command(["git", "status"], "Git Status")

        if "変更確認" in user_input or "差分確認" in user_input:
            return self._run_git_command(["git", "diff", "--stat"], "Git Diff Summary")

        if "最近のコミット" in user_input or "コミット履歴" in user_input:
            return self._run_git_command(["git", "log", "--oneline", "-5"], "Recent Commits")

        if "ブランチ確認" in user_input or "今のブランチ" in user_input:
            return self._run_git_command(["git", "branch", "--show-current"], "Current Branch")

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
                return f"## {title}\n\n{self._limit_output(output)}"

            if error:
                return f"## {title}\n\n{self._limit_output(error)}"

            return f"## {title}\n\n出力はありません。"

        except subprocess.TimeoutExpired:
            return "Gitコマンドがタイムアウトしました。"

        except Exception as error:
            return f"GitToolでエラーが発生しました: {error}"

    def _summarize_git_status(self) -> str:
        branch = self._get_current_branch()
        status_lines = self._get_porcelain_status()

        if status_lines is None:
            return "Git状態の取得に失敗しました。"

        if not status_lines:
            return (
                "## Git Summary\n\n"
                f"現在のブランチ: {branch}\n\n"
                "作業ツリーはきれいです。\n"
                "コミットする変更はありません。"
            )

        modified_files = []
        new_files = []
        deleted_files = []
        staged_files = []
        other_files = []

        for line in status_lines:
            status = line[:2]
            file_path = line[2:].strip()

            index_status = status[0]
            working_status = status[1]

            if status == "??":
                new_files.append(file_path)
                continue

            if index_status != " ":
                staged_files.append(file_path)

            if working_status == "M" or index_status == "M":
                modified_files.append(file_path)
            elif working_status == "D" or index_status == "D":
                deleted_files.append(file_path)
            else:
                other_files.append(file_path)

        lines = [
            "## Git Summary",
            "",
            f"現在のブランチ: {branch}",
            "",
        ]

        self._add_file_section(lines, "変更されたファイル", modified_files)
        self._add_file_section(lines, "新規ファイル", new_files)
        self._add_file_section(lines, "削除されたファイル", deleted_files)
        self._add_file_section(lines, "ステージ済みファイル", staged_files)
        self._add_file_section(lines, "その他の変更", other_files)

        lines.append("まだコミットされていない変更があります。")

        return "\n".join(lines)

    def _add_file_section(self, lines: list[str], title: str, files: list[str]) -> None:
        if not files:
            return

        lines.append(f"{title}:")
        for file_path in sorted(set(files)):
            lines.append(f"- {file_path}")
        lines.append("")

    def _get_current_branch(self) -> str:
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return result.stdout.strip() or "不明"

        except Exception:
            return "不明"

    def _get_porcelain_status(self) -> list[str] | None:
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            if result.returncode != 0:
                return None

            output = result.stdout.strip()

            if not output:
                return []

            return output.splitlines()

        except Exception:
            return None

    def _limit_output(self, text: str) -> str:
        max_length = 4000

        if len(text) <= max_length:
            return text

        return text[:max_length] + "\n\n...出力が長いため省略しました。"
