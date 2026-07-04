"""
Project NEXUS
Project Memory Tool v1

Shows the current development state of Project NEXUS.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
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

# PROJECT_MEMORY_V2_UPDATE_PATCH

def _project_memory_v2_backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / "project_memory_auto" / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / path.name
    backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def _project_memory_v2_save_memory(data: dict) -> Path:
    path = Path("data/project/project_memory.json")
    path.parent.mkdir(parents=True, exist_ok=True)

    _project_memory_v2_backup_file(path)

    data["updated_at"] = datetime.now().isoformat(timespec="seconds")

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return path


def _project_memory_v2_append_methods():
    original_can_handle = ProjectMemoryTool.can_handle
    original_execute = ProjectMemoryTool.execute

    def can_handle_v2(self, user_input: str) -> bool:
        text = user_input.strip()

        if (
            text.startswith("NEXUS現在地更新:")
            or text.startswith("NEXUS次段階更新:")
            or text.startswith("NEXUSマイルストーン追加:")
            or text == "NEXUS記憶保存状況"
        ):
            return True

        return original_can_handle(self, user_input)

    def execute_v2(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith("NEXUS現在地更新:"):
            value = text.split(":", 1)[1].strip()
            return self._update_current_stage_v2(value)

        if text.startswith("NEXUS次段階更新:"):
            value = text.split(":", 1)[1].strip()
            return self._update_next_stage_v2(value)

        if text.startswith("NEXUSマイルストーン追加:"):
            value = text.split(":", 1)[1].strip()
            return self._add_milestone_v2(value)

        if text == "NEXUS記憶保存状況":
            return self._memory_save_status_v2()

        return original_execute(self, user_input)

    def _update_current_stage_v2(self, value: str) -> str:
        if not value:
            return "更新内容が空です。例: NEXUS現在地更新: v0.4 active"

        data = self._load_memory()
        before = data.get("current_stage", "unknown")
        data["current_stage"] = value

        path = _project_memory_v2_save_memory(data)

        return f"""## Project Memory Updated

- Field: current_stage
- Before: {before}
- After: {value}
- Saved: {path}

確認:
- NEXUS現在地
- NEXUS開発状況
"""

    def _update_next_stage_v2(self, value: str) -> str:
        if not value:
            return "更新内容が空です。例: NEXUS次段階更新: Safe Refactor v1"

        data = self._load_memory()
        before = data.get("recommended_next_stage", "unknown")
        data["recommended_next_stage"] = value

        path = _project_memory_v2_save_memory(data)

        return f"""## Project Memory Updated

- Field: recommended_next_stage
- Before: {before}
- After: {value}
- Saved: {path}

確認:
- NEXUS現在地
"""

    def _add_milestone_v2(self, value: str) -> str:
        if not value:
            return "追加内容が空です。例: NEXUSマイルストーン追加: Knowledge Import v1 | Local notes can be imported."

        if "|" in value:
            name, summary = [part.strip() for part in value.split("|", 1)]
        else:
            name = value.strip()
            summary = ""

        if not name:
            return "マイルストーン名が空です。"

        data = self._load_memory()
        milestones = data.get("major_milestones", [])

        if not isinstance(milestones, list):
            milestones = []

        for item in milestones:
            if isinstance(item, dict) and item.get("name") == name:
                return f"""## Milestone Already Exists

同名のマイルストーンが既にあります。

- Name: {name}

確認:
- NEXUSマイルストーン
"""

        milestone = {
            "name": name,
            "status": "completed",
            "summary": summary or "Added from Project Memory v2.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        milestones.append(milestone)
        data["major_milestones"] = milestones

        path = _project_memory_v2_save_memory(data)

        return f"""## Milestone Added

- Name: {name}
- Status: completed
- Summary: {milestone["summary"]}
- Saved: {path}

確認:
- NEXUSマイルストーン
"""

    def _memory_save_status_v2(self) -> str:
        path = Path("data/project/project_memory.json")
        backups = sorted(
            Path("backups/project_memory_auto").glob("*/*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        ) if Path("backups/project_memory_auto").exists() else []

        data = self._load_memory()

        lines = [
            "## Project Memory Save Status",
            "",
            f"- Memory File Exists: {path.exists()}",
            f"- Memory File: {path}",
            f"- Current Stage: {data.get('current_stage', 'unknown')}",
            f"- Recommended Next Stage: {data.get('recommended_next_stage', 'unknown')}",
            f"- Updated At: {data.get('updated_at', 'unknown')}",
            f"- Auto Backups: {len(backups)}",
            "",
            "### Latest Backups",
            "",
        ]

        if backups:
            for backup in backups[:5]:
                lines.append(f"- {backup}")
        else:
            lines.append("- なし")

        return "\n".join(lines)

    ProjectMemoryTool.can_handle = can_handle_v2
    ProjectMemoryTool.execute = execute_v2
    ProjectMemoryTool._update_current_stage_v2 = _update_current_stage_v2
    ProjectMemoryTool._update_next_stage_v2 = _update_next_stage_v2
    ProjectMemoryTool._add_milestone_v2 = _add_milestone_v2
    ProjectMemoryTool._memory_save_status_v2 = _memory_save_status_v2


if not hasattr(ProjectMemoryTool, "_project_memory_v2_patched"):
    ProjectMemoryTool._project_memory_v2_patched = True
    _project_memory_v2_append_methods()
