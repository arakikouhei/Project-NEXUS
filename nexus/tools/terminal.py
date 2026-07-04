"""
Project NEXUS
Safe Terminal Tool
"""

import subprocess
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class TerminalTool(BaseTool):
    """Executes safe terminal commands."""

    name = "terminal"
    description = "安全なターミナルコマンドを実行します"

    def __init__(self) -> None:
        self.working_directory = Path.cwd()

        self.allowed_exact_commands = {
            "pwd",
            "ls",
            "ls -la",
            "git status",
            "git log --oneline -5",
            "python3 --version",
            "pip3 --version",
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

        if command in self.allowed_exact_commands:
            return True

        parts = command.split()

        if not parts:
            return False

        first_word = parts[0]

        terminal_commands = {
            "pwd",
            "ls",
            "git",
            "python3",
            "pip3",
        }

        dangerous_commands = {
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

        return first_word in terminal_commands or first_word in dangerous_commands

    def execute(self, user_input: str) -> str:
        command = self._normalize_command(user_input)

        if not command:
            return "実行するコマンドがありません。"

        if self._is_blocked(command):
            return f"安全のため、このコマンドは実行できません: {command}"

        if command not in self.allowed_exact_commands:
            return f"許可されていないコマンドです: {command}"

        try:
            result = subprocess.run(
                command.split(),
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if output:
                return output

            if error:
                return error

            return "コマンドは実行されましたが、出力はありません。"

        except subprocess.TimeoutExpired:
            return "コマンドがタイムアウトしました。"

        except Exception as error:
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

    def _is_blocked(self, command: str) -> bool:
        parts = command.split()

        dangerous_commands = {
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

        dangerous_symbols = {
            ">",
            ">>",
            "|",
            "&&",
            ";",
        }

        if not parts:
            return False

        if parts[0] in dangerous_commands:
            return True

        for symbol in dangerous_symbols:
            if symbol in command:
                return True

        return False