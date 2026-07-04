from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / datetime.now().strftime("v09_%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return

    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        shutil.copy2(path, target)


def write_file(path_text: str, content: str) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def append_gitignore() -> None:
    path = ROOT / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    additions = [
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        "logs/*.log",
        "backups/",
    ]

    lines = existing.splitlines()
    changed = False

    for item in additions:
        if item not in lines:
            lines.append(item)
            changed = True

    if changed:
        path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in [
        "nexus/tools/manager.py",
        "nexus/tools/git.py",
        "nexus/agent/agent.py",
        "nexus/context/builder.py",
        ".gitignore",
    ]:
        backup(file_path)

    write_file(
        "nexus/context/builder.py",
        '''
        """
        Project NEXUS
        Context Builder
        """

        from pathlib import Path
        import subprocess


        class ContextBuilder:
            """Builds the current execution context."""

            def __init__(self) -> None:
                self.root = Path.cwd()

            def build(self) -> dict:
                return {
                    "project": "Project NEXUS",
                    "version": "v0.9.0-prototype",
                    "working_directory": str(self.root),
                    "git_branch": self._git_branch(),
                    "git_status": self._git_status(),
                    "recent_terminal_logs": self._recent_terminal_logs(),
                }

            def _git_branch(self) -> str:
                try:
                    result = subprocess.run(
                        ["git", "branch", "--show-current"],
                        cwd=self.root,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                    return result.stdout.strip() or "unknown"
                except Exception:
                    return "unknown"

            def _git_status(self) -> str:
                try:
                    result = subprocess.run(
                        ["git", "status", "--porcelain"],
                        cwd=self.root,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                    output = result.stdout.strip()
                    if not output:
                        return "clean"
                    return "dirty"
                except Exception:
                    return "unknown"

            def _recent_terminal_logs(self) -> list[str]:
                log_path = self.root / "logs" / "terminal.log"

                if not log_path.exists():
                    return []

                try:
                    lines = log_path.read_text(encoding="utf-8").splitlines()
                    return lines[-5:]
                except Exception:
                    return []
        ''',
    )

    write_file(
        "nexus/tools/context.py",
        '''
        """
        Project NEXUS
        Context Tool
        """

        from nexus.context.builder import ContextBuilder
        from nexus.tools.base_tool import BaseTool


        class ContextTool(BaseTool):
            """Shows current NEXUS context."""

            name = "context"
            description = "現在のNEXUSの状況を表示します"

            def __init__(self) -> None:
                self.builder = ContextBuilder()

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "nexus状況",
                    "状況確認",
                    "今の状態",
                    "context",
                    "コンテキスト",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                context = self.builder.build()

                lines = [
                    "## NEXUS Context",
                    "",
                    f"Project: {context['project']}",
                    f"Version: {context['version']}",
                    f"Working Directory: {context['working_directory']}",
                    f"Git Branch: {context['git_branch']}",
                    f"Git Status: {context['git_status']}",
                    "",
                ]

                logs = context.get("recent_terminal_logs", [])
                if logs:
                    lines.append("Recent Terminal Logs:")
                    for log in logs:
                        lines.append(f"- {log}")
                else:
                    lines.append("Recent Terminal Logs: none")

                return "\\n".join(lines)
        ''',
    )

    write_file(
        "nexus/tools/system.py",
        '''
        """
        Project NEXUS
        System Tool
        """

        import platform
        import shutil
        import sys
        from pathlib import Path

        from nexus.tools.base_tool import BaseTool


        class SystemTool(BaseTool):
            """Shows safe system information."""

            name = "system"
            description = "安全なシステム情報を表示します"

            def __init__(self) -> None:
                self.root = Path.cwd()

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "システム情報",
                    "system info",
                    "python情報",
                    "容量確認",
                    "環境確認",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                disk = shutil.disk_usage(self.root)

                return (
                    "## System Info\\n\\n"
                    f"OS: {platform.system()} {platform.release()}\\n"
                    f"Machine: {platform.machine()}\\n"
                    f"Python: {sys.version.split()[0]}\\n"
                    f"Project Root: {self.root}\\n"
                    f"Disk Free: {disk.free // (1024 ** 3)} GB\\n"
                )
        ''',
    )

    write_file(
        "nexus/tools/voice.py",
        '''
        """
        Project NEXUS
        Voice Tool
        """

        import platform
        import subprocess

        from nexus.tools.base_tool import BaseTool


        class VoiceTool(BaseTool):
            """Speaks short text on macOS using say."""

            name = "voice"
            description = "短い文章をMacで読み上げます"

            def can_handle(self, user_input: str) -> bool:
                return (
                    user_input.startswith("読み上げ:")
                    or user_input.startswith("読み上げ：")
                    or user_input.startswith("話して:")
                    or user_input.startswith("話して：")
                )

            def execute(self, user_input: str) -> str:
                text = self._extract_text(user_input)

                if not text:
                    return "読み上げる文章がありません。"

                if len(text) > 120:
                    return "安全のため、読み上げは120文字以内にしてください。"

                if platform.system() != "Darwin":
                    return "VoiceToolは現在macOSのsayコマンド専用です。"

                try:
                    subprocess.run(
                        ["say", text],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        check=False,
                    )
                    return f"読み上げました: {text}"
                except subprocess.TimeoutExpired:
                    return "読み上げがタイムアウトしました。"
                except Exception as error:
                    return f"読み上げ中にエラーが発生しました: {error}"

            def _extract_text(self, user_input: str) -> str:
                for separator in [":", "："]:
                    if separator in user_input:
                        return user_input.split(separator, 1)[1].strip()
                return ""
        ''',
    )

    write_file(
        "nexus/tools/git.py",
        '''
        """
        Project NEXUS
        Git Tool
        """

        import subprocess
        from pathlib import Path

        from nexus.tools.base_tool import BaseTool


        class GitTool(BaseTool):
            """Handles safe Git commands."""

            name = "git"
            description = "Gitの状態確認と安全なコミット操作を行います"

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
                    "コミット準備",
                    "コミットして",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                if "コミットして" in user_input:
                    message = self._extract_commit_message(user_input)
                    if not message:
                        return (
                            "コミットメッセージがありません。\\n\\n"
                            "例:\\n"
                            "コミットして: Add git workflow"
                        )
                    return self._commit_all(message)

                if "コミット準備" in user_input:
                    return self._prepare_commit()

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
                        return f"## {title}\\n\\n{self._limit_output(output)}"

                    if error:
                        return f"## {title}\\n\\n{self._limit_output(error)}"

                    return f"## {title}\\n\\n出力はありません。"

                except subprocess.TimeoutExpired:
                    return "Gitコマンドがタイムアウトしました。"

                except Exception as error:
                    return f"GitToolでエラーが発生しました: {error}"

            def _prepare_commit(self) -> str:
                summary = self._summarize_git_status()
                diff_summary = self._run_git_command(
                    ["git", "diff", "--stat"],
                    "Git Diff Summary",
                )

                return (
                    f"{summary}\\n\\n"
                    "---\\n\\n"
                    f"{diff_summary}\\n\\n"
                    "---\\n\\n"
                    "これは確認用です。まだコミットは実行していません。\\n"
                    "コミットする場合は次のように入力してください。\\n\\n"
                    "コミットして: Add feature description"
                )

            def _extract_commit_message(self, user_input: str) -> str:
                for separator in [":", "："]:
                    if separator in user_input:
                        return user_input.split(separator, 1)[1].strip()
                return ""

            def _commit_all(self, message: str) -> str:
                status_lines = self._get_porcelain_status()

                if status_lines is None:
                    return "Git状態の取得に失敗したため、コミットできませんでした。"

                if not status_lines:
                    return "コミットする変更はありません。"

                if "\\n" in message:
                    return "コミットメッセージに改行は使えません。"

                if len(message) > 120:
                    return "コミットメッセージが長すぎます。120文字以内にしてください。"

                try:
                    add_result = subprocess.run(
                        ["git", "add", "."],
                        cwd=self.working_directory,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )

                    if add_result.returncode != 0:
                        error = add_result.stderr.strip()
                        return f"git add に失敗しました。\\n\\n{error}"

                    commit_result = subprocess.run(
                        ["git", "commit", "-m", message],
                        cwd=self.working_directory,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        check=False,
                    )

                    output = commit_result.stdout.strip()
                    error = commit_result.stderr.strip()

                    if commit_result.returncode != 0:
                        return f"コミットに失敗しました。\\n\\n{error or output}"

                    return (
                        "## Commit Completed\\n\\n"
                        f"メッセージ: {message}\\n\\n"
                        f"{self._limit_output(output)}\\n\\n"
                        "GitHubへ送る場合は、NEXUSを終了してMacのターミナルで `git push` を実行してください。"
                    )

                except subprocess.TimeoutExpired:
                    return "Gitコミット処理がタイムアウトしました。"

                except Exception as error:
                    return f"コミット中にエラーが発生しました: {error}"

            def _summarize_git_status(self) -> str:
                branch = self._get_current_branch()
                status_lines = self._get_porcelain_status()

                if status_lines is None:
                    return "Git状態の取得に失敗しました。"

                if not status_lines:
                    return (
                        "## Git Summary\\n\\n"
                        f"現在のブランチ: {branch}\\n\\n"
                        "作業ツリーはきれいです。\\n"
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

                return "\\n".join(lines)

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

                return text[:max_length] + "\\n\\n...出力が長いため省略しました。"
        ''',
    )

    write_file(
        "nexus/agent/planner.py",
        '''
        """
        Project NEXUS
        Simple Planner
        """


        class SimplePlanner:
            """Creates simple plans for user requests."""

            def plan(self, user_input: str) -> list[str]:
                steps = []

                if "コミット" in user_input:
                    steps.append("Check Git status")
                    steps.append("Review changes")
                    steps.append("Commit safely")

                elif "解析" in user_input:
                    steps.append("Find target file")
                    steps.append("Analyze code")
                    steps.append("Summarize result")

                elif "状況" in user_input:
                    steps.append("Build current context")
                    steps.append("Summarize project state")

                else:
                    steps.append("Decide whether a tool can handle the request")
                    steps.append("Use AI response if no tool matches")

                return steps
        ''',
    )

    write_file(
        "nexus/agent/agent.py",
        '''
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
        ''',
    )

    write_file(
        "nexus/tools/manager.py",
        '''
        """
        Project NEXUS
        Tool Manager
        """

        from nexus.tools.base_tool import BaseTool
        from nexus.tools.clock import ClockTool
        from nexus.tools.git import GitTool
        from nexus.tools.terminal import TerminalTool
        from nexus.tools.context import ContextTool
        from nexus.tools.system import SystemTool
        from nexus.tools.voice import VoiceTool
        from nexus.tools.calculator import CalculatorTool
        from nexus.tools.filesystem import FileSystemTool
        from nexus.tools.project import ProjectTool
        from nexus.tools.code import CodeTool


        class ToolManager:
            """Manages all tools."""

            def __init__(self) -> None:
                self.tools: list[BaseTool] = []

                self.register(ClockTool())
                self.register(GitTool())
                self.register(TerminalTool())
                self.register(ContextTool())
                self.register(SystemTool())
                self.register(VoiceTool())
                self.register(CalculatorTool())
                self.register(FileSystemTool())
                self.register(ProjectTool())
                self.register(CodeTool())

            def register(self, tool: BaseTool) -> None:
                self.tools.append(tool)

            def execute(self, user_input: str) -> str | None:
                for tool in self.tools:
                    if tool.can_handle(user_input):
                        return tool.execute(user_input)

                return None
        ''',
    )

    append_gitignore()

    print("Upgrade files written.")
    print(f"Backup saved to: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
