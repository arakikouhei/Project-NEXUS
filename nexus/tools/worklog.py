"""
Project NEXUS
Work Log Tool
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class WorkLogTool(BaseTool):
    """Records and shows work logs."""

    name = "worklog"
    description = "作業ログを記録・表示します"

    def __init__(self) -> None:
        self.root = Path.cwd()
        self.path = self.root / "data" / "worklog.json"

    def can_handle(self, user_input: str) -> bool:
        return (
            user_input.startswith("作業記録:")
            or user_input.startswith("作業記録：")
            or user_input in {"作業ログ", "最近の作業", "作業履歴"}
        )

    def execute(self, user_input: str) -> str:
        if user_input.startswith("作業記録:") or user_input.startswith("作業記録："):
            text = self._extract_text(user_input)

            if not text:
                return "記録する内容がありません。"

            if len(text) > 300:
                return "作業記録は300文字以内にしてください。"

            return self._add_entry(text)

        return self._show_entries()

    def _extract_text(self, user_input: str) -> str:
        for separator in [":", "："]:
            if separator in user_input:
                return user_input.split(separator, 1)[1].strip()
        return ""

    def _load(self) -> dict:
        if not self.path.exists():
            return {"entries": []}

        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {"entries": []}

    def _save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _add_entry(self, text: str) -> str:
        data = self._load()

        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
        }

        data.setdefault("entries", []).append(entry)
        self._save(data)

        return f"作業記録に追加しました: {text}"

    def _show_entries(self) -> str:
        data = self._load()
        entries = data.get("entries", [])

        lines = ["## Work Log", ""]

        if not entries:
            lines.append("作業ログはまだありません。")
            return "\n".join(lines)

        for entry in entries[-10:]:
            lines.append(f"- {entry.get('time', 'unknown')} | {entry.get('text', '')}")

        return "\n".join(lines)
