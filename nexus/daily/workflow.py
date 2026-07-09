from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_MEMORY_PATH = PROJECT_ROOT / "data/project/project_memory.json"


def load_project_memory() -> dict[str, Any]:
    if not PROJECT_MEMORY_PATH.exists():
        return {
            "current_stage": "unknown",
            "recommended_next_stage": "unknown",
            "important_commands": [],
            "recommended_next_options": [],
        }

    return json.loads(PROJECT_MEMORY_PATH.read_text(encoding="utf-8"))


def build_next_actions(memory: dict[str, Any] | None = None) -> list[str]:
    data = memory or load_project_memory()
    options = data.get("recommended_next_options") or []

    if options:
        return [str(item) for item in options[:5]]

    return [
        "python3 scripts/check_system_stability.py",
        "python3 scripts/check_release_readiness.py",
        "python3 scripts/check_v3_0_readiness.py",
    ]


def build_today_report() -> str:
    data = load_project_memory()

    current_stage = data.get("current_stage", "unknown")
    next_stage = data.get("recommended_next_stage", "unknown")
    important_commands = data.get("important_commands", [])
    next_actions = build_next_actions(data)

    lines = [
        "===================================",
        "今日のNEXUS",
        "===================================",
        "",
        f"現在地: {current_stage}",
        f"次の段階: {next_stage}",
        "",
        "システム状態:",
        "- Project Memory: loaded" if PROJECT_MEMORY_PATH.exists() else "- Project Memory: missing",
        "- Dashboard: local launch supported",
        "- Safety: dangerous dashboard actions are not implemented",
        "",
        "重要コマンド:",
    ]

    if important_commands:
        for command in important_commands[:8]:
            lines.append(f"- {command}")
    else:
        lines.append("- NEXUS現在地")
        lines.append("- システム健康診断")
        lines.append("- NEXUSダッシュボード起動方法")

    lines.extend([
        "",
        "ダッシュボード:",
        "- 起動: python3 -m nexus.dashboard.server",
        "- URL: http://127.0.0.1:8765",
        "- 終了: Ctrl + C",
        "",
        "次にやること:",
    ])

    for item in next_actions:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "保存前チェック:",
        "- python3 scripts/test_major_commands.py",
        "- python3 scripts/check_system_stability.py",
        "- python3 scripts/check_release_readiness.py",
        "- python3 scripts/check_v3_0_readiness.py",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    print(build_today_report())
