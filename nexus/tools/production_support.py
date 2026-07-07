import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class ProductionSupportTool:
    """Creative production support notes for Project NEXUS."""

    DATA_DIR = Path("data/production")
    NOTES_PATH = DATA_DIR / "production_notes.json"

    COMMANDS = {
        "制作メモヘルプ",
        "制作メモ一覧",
        "3DCG作業確認",
        "Maya作業メモ",
    }

    PREFIXES = (
        "制作メモ追加:",
        "制作メモ検索:",
        "制作メモ詳細:",
    )

    def can_handle(self, text: str) -> bool:
        text = text.strip()
        return text in self.COMMANDS or any(text.startswith(prefix) for prefix in self.PREFIXES)

    def execute(self, text: str) -> str:
        return self.handle(text)

    def handle(self, text: str) -> str:
        text = text.strip()

        if text == "制作メモヘルプ":
            return self._help()

        if text.startswith("制作メモ追加:"):
            content = text.split(":", 1)[1].strip()
            return self._add_note(content)

        if text == "制作メモ一覧":
            return self._list_notes()

        if text.startswith("制作メモ検索:"):
            query = text.split(":", 1)[1].strip()
            return self._search_notes(query)

        if text.startswith("制作メモ詳細:"):
            note_id = text.split(":", 1)[1].strip()
            return self._note_detail(note_id)

        if text == "3DCG作業確認":
            return self._three_d_check()

        if text == "Maya作業メモ":
            return self._maya_notes()

        return "Production Support: unsupported command."

    def _help(self) -> str:
        return """## Production Support

Creative production support commands.

### Commands

- 制作メモヘルプ
- 制作メモ追加: text
- 制作メモ一覧
- 制作メモ検索: query
- 制作メモ詳細: memo-id
- 3DCG作業確認
- Maya作業メモ

### Purpose

- Keep creative production notes
- Track 3DCG / Maya work
- Prepare for future production dashboard panels

Safety: notes are stored separately in `data/production/production_notes.json`.
"""

    def _add_note(self, content: str) -> str:
        if not content:
            return self._error("No memo text provided.")

        data = self._load_data()

        note_id = "prod-" + uuid.uuid4().hex[:8]
        tags = self._infer_tags(content)

        note = {
            "id": note_id,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "content": content,
            "tags": tags,
        }

        data.setdefault("notes", []).append(note)
        self._save_data(data)

        return "\n".join(
            [
                "## Production Support",
                "",
                "Production memo added.",
                "",
                f"- ID: `{note_id}`",
                f"- Tags: {', '.join(tags) if tags else 'none'}",
                "",
                "Use `制作メモ一覧` or `制作メモ詳細: memo-id` to review it.",
            ]
        )

    def _list_notes(self) -> str:
        notes = self._load_data().get("notes", [])

        lines = [
            "## Production Support",
            "",
            "Production memo list.",
            "",
        ]

        if not notes:
            lines.append("No production memos yet.")
            return "\n".join(lines)

        for note in notes[-20:][::-1]:
            content = note.get("content", "")
            short = content[:90] + ("..." if len(content) > 90 else "")
            tags = ", ".join(note.get("tags", [])) or "none"
            lines += [
                f"### {note.get('id', 'unknown')}",
                f"- Created: {note.get('created_at', 'unknown')}",
                f"- Tags: {tags}",
                f"- Memo: {short}",
                "",
            ]

        return "\n".join(lines).rstrip()

    def _search_notes(self, query: str) -> str:
        if not query:
            return self._error("No search query provided.")

        notes = self._load_data().get("notes", [])
        query_lower = query.lower()

        matches = []
        for note in notes:
            haystack = " ".join(
                [
                    note.get("id", ""),
                    note.get("content", ""),
                    " ".join(note.get("tags", [])),
                ]
            ).lower()
            if query_lower in haystack:
                matches.append(note)

        lines = [
            "## Production Support",
            "",
            f"Search query: `{query}`",
            "",
        ]

        if not matches:
            lines.append("No matching production memos found.")
            return "\n".join(lines)

        for note in matches[-20:][::-1]:
            content = note.get("content", "")
            short = content[:110] + ("..." if len(content) > 110 else "")
            lines += [
                f"### {note.get('id', 'unknown')}",
                f"- Created: {note.get('created_at', 'unknown')}",
                f"- Memo: {short}",
                "",
            ]

        return "\n".join(lines).rstrip()

    def _note_detail(self, note_id: str) -> str:
        if not note_id:
            return self._error("No memo ID provided.")

        notes = self._load_data().get("notes", [])

        for note in notes:
            if note.get("id") == note_id:
                tags = ", ".join(note.get("tags", [])) or "none"
                return "\n".join(
                    [
                        "## Production Support",
                        "",
                        f"Memo detail: `{note_id}`",
                        "",
                        f"- Created: {note.get('created_at', 'unknown')}",
                        f"- Tags: {tags}",
                        "",
                        "### Content",
                        note.get("content", ""),
                    ]
                )

        return self._error(f"Production memo not found: `{note_id}`")

    def _three_d_check(self) -> str:
        notes = self._load_data().get("notes", [])
        related = self._filter_by_tags(notes, {"3dcg", "maya", "mudbox", "blender", "modeling", "uv"})

        lines = [
            "## Production Support",
            "",
            "3DCG work check.",
            "",
            "### Checklist",
            "- モデルの目的を確認する",
            "- スケールを確認する",
            "- トポロジーを確認する",
            "- 法線の向きを確認する",
            "- UVの切れ目と歪みを確認する",
            "- 必要ならバックアップしてから編集する",
            "",
            "### Related Production Memos",
        ]

        if not related:
            lines.append("No related production memos found yet.")
            return "\n".join(lines)

        for note in related[-10:][::-1]:
            content = note.get("content", "")
            short = content[:100] + ("..." if len(content) > 100 else "")
            lines.append(f"- `{note.get('id', 'unknown')}`: {short}")

        return "\n".join(lines)

    def _maya_notes(self) -> str:
        notes = self._load_data().get("notes", [])
        related = self._filter_by_tags(notes, {"maya"})

        lines = [
            "## Production Support",
            "",
            "Maya work memos.",
            "",
        ]

        if not related:
            lines += [
                "No Maya production memos yet.",
                "",
                "Tip: add one with `制作メモ追加: Mayaで...`",
            ]
            return "\n".join(lines)

        for note in related[-20:][::-1]:
            content = note.get("content", "")
            short = content[:120] + ("..." if len(content) > 120 else "")
            lines += [
                f"### {note.get('id', 'unknown')}",
                f"- Created: {note.get('created_at', 'unknown')}",
                f"- Memo: {short}",
                "",
            ]

        return "\n".join(lines).rstrip()

    def _infer_tags(self, content: str) -> List[str]:
        text = content.lower()
        tags = ["production"]

        keyword_tags = {
            "maya": "maya",
            "マヤ": "maya",
            "mudbox": "mudbox",
            "マッドボックス": "mudbox",
            "blender": "blender",
            "uv": "uv",
            "3dcg": "3dcg",
            "3d": "3dcg",
            "モデリング": "modeling",
            "モデル": "modeling",
            "イラスト": "illustration",
            "絵": "illustration",
            "アニメ": "animation",
            "映像": "video",
            "premiere": "premiere",
            "clip": "clipstudio",
        }

        for keyword, tag in keyword_tags.items():
            if keyword in text and tag not in tags:
                tags.append(tag)

        return tags

    def _filter_by_tags(self, notes: List[Dict[str, Any]], tags: set) -> List[Dict[str, Any]]:
        results = []
        for note in notes:
            note_tags = set(note.get("tags", []))
            if note_tags.intersection(tags):
                results.append(note)
        return results

    def _load_data(self) -> Dict[str, Any]:
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not self.NOTES_PATH.exists():
            return {"version": 1, "notes": []}

        try:
            return json.loads(self.NOTES_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"version": 1, "notes": []}

    def _save_data(self, data: Dict[str, Any]) -> None:
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.NOTES_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _error(self, message: str) -> str:
        return "\n".join(
            [
                "## Production Support",
                "",
                "Request failed.",
                "",
                f"Reason: {message}",
            ]
        )
