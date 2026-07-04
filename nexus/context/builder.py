"""
Project NEXUS
Context Builder
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


class ContextBuilder:
    """Builds the current execution context."""

    def __init__(self) -> None:
        self.root = Path.cwd()
        self.worklog_path = self.root / "data" / "worklog.json"

    def build(self) -> dict:
        return {
            "project": "Project NEXUS",
            "version": "v0.95.0-pre-sphere",
            "stage": "Pre-Sphere Core",
            "working_directory": str(self.root),
            "git_branch": self._git_branch(),
            "git_status": self._git_status(),
            "available_tools": self._available_tools(),
            "recent_worklog": self._recent_worklog(),
            "recent_terminal_logs": self._recent_terminal_logs(),
            "sphere_ready": False,
            "hardware_mode": "mock",
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

            if result.stdout.strip():
                return "dirty"

            return "clean"

        except Exception:
            return "unknown"

    def _available_tools(self) -> list[str]:
        return [
            "ClockTool",
            "GitTool",
            "TerminalTool",
            "ContextTool",
            "SystemTool",
            "VoiceTool",
            "TestTool",
            "DashboardTool",
            "WorkLogTool",
            "HardwareTool",
            "CapabilityTool",
            "CalculatorTool",
            "FileSystemTool",
            "ProjectTool",
            "CodeTool",
        ]

    def _recent_worklog(self) -> list[str]:
        if not self.worklog_path.exists():
            return []

        try:
            data = json.loads(self.worklog_path.read_text(encoding="utf-8"))
            entries = data.get("entries", [])
            recent = entries[-5:]
            return [
                f"{entry.get('time', 'unknown')} - {entry.get('text', '')}"
                for entry in recent
            ]
        except Exception:
            return []

    def _recent_terminal_logs(self) -> list[str]:
        log_path = self.root / "logs" / "terminal.log"

        if not log_path.exists():
            return []

        try:
            lines = log_path.read_text(encoding="utf-8").splitlines()
            return lines[-5:]
        except Exception:
            return []
