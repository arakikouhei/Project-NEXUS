"""
Project NEXUS
Project Memory Tool v1

Shows the current development state of Project NEXUS.
"""

from __future__ import annotations

from pathlib import Path
import json
import subprocess

from nexus.tools.base_tool import BaseTool


class ProjectMemoryTool(BaseTool):
    """Shows Project NEXUS development memory."""

    name = "project_memory"
    description = "NEXUS自身の開発状況・現在地・マイルストーンを表示します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return text in {
            "NEXUS記憶",
            "NEXUS開発状況",
            "NEXUS現在地",
            "NEXUSマイルストーン",
        }

    def execute(self, user_input: str) -> str:
        text = user_input.strip()
        data = self._load_memory()

        if text == "NEXUS記憶":
            return self._memory_overview(data)

        if text == "NEXUS開発状況":
            return self._development_status(data)

        if text == "NEXUS現在地":
            return self._current_position(data)

        if text == "NEXUSマイルストーン":
            return self._milestones(data)

        return "対応していないProject Memory操作です。"

    def _load_memory(self) -> dict:
        path = Path("data/project/project_memory.json")

        if not path.exists():
            return {}

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _git_latest_commit(self) -> str:
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-1"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip() or "unknown"
        except Exception:
            pass

        return "unknown"

    def _git_clean(self) -> str:
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return "True" if not result.stdout.strip() else "False"
        except Exception:
            pass

        return "unknown"

    def _memory_overview(self, data: dict) -> str:
        project_name = data.get("project_name", "Project NEXUS")
        stage = data.get("current_stage", "unknown")
        status = data.get("status", "unknown")

        return f"""## NEXUS Project Memory

- Project: {project_name}
- Current Stage: {stage}
- Status: {status}
- Latest Commit: {self._git_latest_commit()}
- Git Clean: {self._git_clean()}

使える確認:
- NEXUS開発状況
- NEXUS現在地
- NEXUSマイルストーン
"""

    def _development_status(self, data: dict) -> str:
        state = data.get("latest_confirmed_state", {})
        commands = data.get("important_commands", [])

        lines = [
            "## NEXUS Development Status",
            "",
            f"- Stage: {data.get('current_stage', 'unknown')}",
            f"- Status: {data.get('status', 'unknown')}",
            f"- Latest Commit: {self._git_latest_commit()}",
            f"- Git Clean Now: {self._git_clean()}",
            "",
            "### Last Confirmed State",
            "",
            f"- Git Clean: {state.get('git_clean', 'unknown')}",
            f"- Python Compile Errors: {state.get('python_compile_errors', 'unknown')}",
            f"- Features Detected: {state.get('features_detected', 'unknown')}",
            f"- Auto Recall Enabled: {state.get('auto_recall_enabled', 'unknown')}",
            f"- Archive Include Archived: {state.get('archive_filter_include_archived', 'unknown')}",
            "",
            "### Important Commands",
            "",
        ]

        for command in commands:
            lines.append(f"- {command}")

        return "\n".join(lines)

    def _current_position(self, data: dict) -> str:
        options = data.get("recommended_next_options", [])
        safety = data.get("safety_policy", [])

        lines = [
            "## NEXUS Current Position",
            "",
            f"- Current Stage: {data.get('current_stage', 'unknown')}",
            f"- Recommended Next Stage: {data.get('recommended_next_stage', 'unknown')}",
            "",
            "### Next Options",
            "",
        ]

        for option in options:
            lines.append(f"- {option}")

        lines.extend([
            "",
            "### Safety Policy",
            "",
        ])

        for item in safety:
            lines.append(f"- {item}")

        return "\n".join(lines)

    def _milestones(self, data: dict) -> str:
        milestones = data.get("major_milestones", [])

        lines = [
            "## NEXUS Milestones",
            "",
        ]

        if not milestones:
            lines.append("- No milestones found.")
            return "\n".join(lines)

        for item in milestones:
            name = item.get("name", "unknown")
            status = item.get("status", "unknown")
            summary = item.get("summary", "")
            lines.append(f"### {name}")
            lines.append(f"- Status: {status}")
            lines.append(f"- Summary: {summary}")
            lines.append("")

        return "\n".join(lines).rstrip()
