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
