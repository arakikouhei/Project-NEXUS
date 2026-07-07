"""
Project NEXUS
Personal Work Notes Tool v1

Stores, lists, searches, and shows personal work notes.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import hashlib

from nexus.tools.base_tool import BaseTool


class WorkNotesTool(BaseTool):
    """Manages personal work notes."""

    name = "work_notes"
    description = "作業メモを追加・一覧・検索・詳細表示します"

    NOTES_PATH = Path("data/work_notes/work_notes.json")

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("作業メモ追加:")
            or text.startswith("作業メモ検索:")
            or text.startswith("作業メモ詳細:")
            or text in {
                "作業メモ一覧",
                "作業メモヘルプ",
            }
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "作業メモヘルプ":
            return self._help()

        if text.startswith("作業メモ追加:"):
            content = text.split(":", 1)[1].strip()
            return self._add_note(content)

        if text == "作業メモ一覧":
            return self._list_notes()

        if text.startswith("作業メモ検索:"):
            query = text.split(":", 1)[1].strip()
            return self._search_notes(query)

        if text.startswith("作業メモ詳細:"):
            memo_id = text.split(":", 1)[1].strip()
            return self._note_detail(memo_id)

        return "対応していない作業メモ操作です。"

    def _help(self) -> str:
        return """## Work Notes Help

使えるコマンド:

- 作業メモ追加: text
- 作業メモ一覧
- 作業メモ検索: query
- 作業メモ詳細: memo-id

方針:
- 作業メモは data/work_notes/work_notes.json に保存します。
- 削除はしません。
- NEXUSの知識本体とは分けて保存します。
"""

    def _add_note(self, content: str) -> str:
        if not content:
            return "作業メモ内容が空です。例: 作業メモ追加: 今日の作業内容"

        notes = self._load_notes()

        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        memo_id = f"work-{digest[:8]}"

        for note in notes:
            if isinstance(note, dict) and note.get("digest") == digest:
                return f"""## Work Note Already Exists

同じ内容の作業メモが既にあります。

- ID: {note.get("id", "unknown")}
- Created At: {note.get("created_at", "unknown")}
"""

        note = {
            "id": memo_id,
            "content": content,
            "summary": self._summary(content),
            "tags": self._guess_tags(content),
            "digest": digest,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "archived": False,
        }

        notes.append(note)
        self._save_notes(notes)

        return f"""## Work Note Added

- ID: {memo_id}
- Summary: {note["summary"]}
- Tags: {", ".join(note["tags"])}
- Characters: {len(content)}

確認:
- 作業メモ一覧
- 作業メモ詳細: {memo_id}
"""

    def _list_notes(self) -> str:
        notes = self._load_notes()

        lines = [
            "## Work Notes",
            "",
        ]

        if not notes:
            lines.append("- 作業メモはまだありません。")
            return "\n".join(lines)

        for note in reversed(notes[-20:]):
            if not isinstance(note, dict):
                continue

            lines.append(f"- {note.get('id', 'unknown')} | {note.get('summary', '')} | {note.get('created_at', 'unknown')}")

        return "\n".join(lines)

    def _search_notes(self, query: str) -> str:
        if not query:
            return "検索語が空です。例: 作業メモ検索: Maya"

        notes = self._load_notes()
        terms = [x.lower() for x in query.replace("　", " ").split() if x.strip()]

        matches = []

        for note in notes:
            if not isinstance(note, dict):
                continue

            text = " ".join([
                note.get("id", ""),
                note.get("summary", ""),
                note.get("content", ""),
                " ".join(note.get("tags", [])) if isinstance(note.get("tags", []), list) else "",
            ]).lower()

            score = 0
            for term in terms:
                if term in text:
                    score += 10
                if term in note.get("summary", "").lower():
                    score += 5

            if score > 0:
                matches.append((score, note))

        matches.sort(key=lambda x: (-x[0], x[1].get("created_at", "")), reverse=False)

        lines = [
            "## Work Note Search",
            "",
            f"Query: {query}",
            "",
        ]

        if not matches:
            lines.append("- 一致する作業メモはありません。")
            return "\n".join(lines)

        for score, note in matches[:10]:
            lines.append(f"- {note.get('id', 'unknown')} | {note.get('summary', '')} | score={score}")

        return "\n".join(lines)

    def _note_detail(self, memo_id: str) -> str:
        if not memo_id:
            return "メモIDが空です。例: 作業メモ詳細: work-xxxxxxxx"

        notes = self._load_notes()

        for note in notes:
            if isinstance(note, dict) and note.get("id") == memo_id:
                tags = note.get("tags", [])
                tag_text = ", ".join(tags) if isinstance(tags, list) else ""

                return f"""## Work Note Detail

- ID: {note.get('id', 'unknown')}
- Created At: {note.get('created_at', 'unknown')}
- Updated At: {note.get('updated_at', 'unknown')}
- Tags: {tag_text}
- Archived: {note.get('archived', False)}

### Content

{note.get('content', '')}
"""

        return f"""## Work Note Not Found

- ID: {memo_id}

確認:
- 作業メモ一覧
"""

    def _load_notes(self) -> list:
        if not self.NOTES_PATH.exists():
            return []

        try:
            data = json.loads(self.NOTES_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save_notes(self, notes: list) -> None:
        self.NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.NOTES_PATH.write_text(
            json.dumps(notes, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _summary(self, content: str) -> str:
        one_line = " ".join(content.strip().split())
        return one_line[:80] if one_line else "untitled"

    def _guess_tags(self, content: str) -> list[str]:
        tags = ["work_note"]

        lowered = content.lower()

        if "nexus" in lowered:
            tags.append("nexus")

        if "maya" in lowered or "uv" in lowered or "3dcg" in lowered:
            tags.append("3dcg")

        if "論文" in content or "paper" in lowered or "research" in lowered:
            tags.append("research")

        if "ui" in lowered or "画面" in content:
            tags.append("ui")

        if "音声" in content or "voice" in lowered:
            tags.append("voice")

        if "カメラ" in content or "camera" in lowered:
            tags.append("camera")

        return list(dict.fromkeys(tags))
