"""
Project NEXUS
Safe Terminal Tool
"""

import shlex
import subprocess
from datetime import datetime
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class TerminalTool(BaseTool):
    """Executes safe terminal commands."""

    name = "terminal"
    description = "安全なターミナルコマンドを実行します"

    def __init__(self) -> None:
        self.working_directory = Path.cwd()
        self.log_file = self.working_directory / "logs" / "terminal.log"

        self.dangerous_commands = {
            "rm",
            "sudo",
            "shutdown",
            "reboot",
            "chmod",
            "chown",
            "kill",
            "killall",
            "mv",
            "cp",
        }

        self.dangerous_symbols = {
            ">",
            ">>",
            "|",
            "&&",
            ";",
        }

        self.terminal_commands = {
            "pwd",
            "ls",
            "git",
            "python3",
            "pip3",
        }

    def can_handle(self, user_input: str) -> bool:
        command = self._normalize_command(user_input)

        if (
            user_input.startswith("terminal ")
            or user_input.startswith("ターミナル ")
            or user_input.startswith("実行 ")
            or user_input.startswith("コマンド ")
        ):
            return True

        parts = self._split_command(command)

        if not parts:
            return False

        first_word = parts[0]

        return first_word in self.terminal_commands or first_word in self.dangerous_commands

    def execute(self, user_input: str) -> str:
        command = self._normalize_command(user_input)

        if not command:
            self._write_log("DENIED", command, "empty command")
            return "実行するコマンドがありません。"

        if self._is_blocked(command):
            self._write_log("BLOCKED", command, "dangerous command or symbol")
            return f"安全のため、このコマンドは実行できません: {command}"

        parts = self._split_command(command)

        if not parts:
            self._write_log("DENIED", command, "parse failed")
            return "コマンドを解析できませんでした。"

        is_valid, message = self._validate_command(parts)

        if not is_valid:
            self._write_log("DENIED", command, message)
            return message

        try:
            result = subprocess.run(
                parts,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            self._write_log(
                "ALLOWED",
                command,
                f"returncode={result.returncode}",
            )

            if output:
                return self._limit_output(output)

            if error:
                return self._limit_output(error)

            return "コマンドは実行されましたが、出力はありません。"

        except subprocess.TimeoutExpired:
            self._write_log("TIMEOUT", command, "timeout=10s")
            return "コマンドがタイムアウトしました。"

        except Exception as error:
            self._write_log("ERROR", command, str(error))
            return f"ターミナル実行中にエラーが発生しました: {error}"

    def _normalize_command(self, user_input: str) -> str:
        command = user_input.strip()

        prefixes = [
            "terminal ",
            "ターミナル ",
            "実行 ",
            "コマンド ",
        ]

        for prefix in prefixes:
            if command.startswith(prefix):
                command = command.replace(prefix, "", 1).strip()

        return command

    def _split_command(self, command: str) -> list[str]:
        try:
            return shlex.split(command)
        except ValueError:
            return []

    def _is_blocked(self, command: str) -> bool:
        parts = self._split_command(command)

        if not parts:
            return False

        for symbol in self.dangerous_symbols:
            if symbol in command:
                return True

        for part in parts:
            if part in self.dangerous_commands:
                return True

        return False

    def _validate_command(self, parts: list[str]) -> tuple[bool, str]:
        command = parts[0]

        if command == "pwd":
            if len(parts) == 1:
                return True, ""
            return False, "pwd に引数は使えません。"

        if command == "ls":
            return self._validate_ls(parts)

        if command == "git":
            return self._validate_git(parts)

        if command == "python3":
            if parts == ["python3", "--version"]:
                return True, ""
            return False, f"許可されていないコマンドです: {' '.join(parts)}"

        if command == "pip3":
            if parts == ["pip3", "--version"]:
                return True, ""
            return False, f"許可されていないコマンドです: {' '.join(parts)}"

        return False, f"許可されていないコマンドです: {' '.join(parts)}"

    def _validate_ls(self, parts: list[str]) -> tuple[bool, str]:
        if len(parts) == 1:
            return True, ""

        if len(parts) == 2:
            if parts[1] == "-la":
                return True, ""

            if self._is_safe_path(parts[1]):
                return True, ""

        if len(parts) == 3:
            if parts[1] == "-la" and self._is_safe_path(parts[2]):
                return True, ""

        return False, f"許可されていないlsコマンドです: {' '.join(parts)}"

    def _validate_git(self, parts: list[str]) -> tuple[bool, str]:
        allowed_git_commands = [
            ["git", "status"],
            ["git", "diff", "--stat"],
            ["git", "log", "--oneline", "-5"],
        ]

        if parts in allowed_git_commands:
            return True, ""

        return False, f"許可されていないgitコマンドです: {' '.join(parts)}"

    def _is_safe_path(self, path_text: str) -> bool:
        if not path_text:
            return False

        if path_text.startswith("-"):
            return False

        path = Path(path_text)

        if path.is_absolute():
            return False

        if "~" in path.parts:
            return False

        if ".." in path.parts:
            return False

        resolved_path = (self.working_directory / path).resolve()

        try:
            resolved_path.relative_to(self.working_directory.resolve())
        except ValueError:
            return False

        return True

    def _limit_output(self, text: str) -> str:
        max_length = 4000

        if len(text) <= max_length:
            return text

        return text[:max_length] + "\n\n...出力が長いため省略しました。"

    def _write_log(self, status: str, command: str, detail: str = "") -> None:
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if detail:
                line = f"[{now}] {status}: {command} | {detail}\n"
            else:
                line = f"[{now}] {status}: {command}\n"

            with self.log_file.open("a", encoding="utf-8") as file:
                file.write(line)

        except Exception:
            # ログ保存に失敗しても、ツール本体の実行は止めない
            pass