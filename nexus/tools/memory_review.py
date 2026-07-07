"""
Project NEXUS
Memory Review Tool v1

Reviews memory-related data without deleting or rewriting anything.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta
import json
import hashlib

from nexus.tools.base_tool import BaseTool


class MemoryReviewTool(BaseTool):
    """Reviews memory for old, duplicate, and safety-check candidates."""

    name = "memory_review"
    description = "記憶データを削除なしでレビューします"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return text in {
            "記憶レビュー",
            "古い記憶候補",
            "重複記憶候補",
            "記憶安全確認",
        }

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "記憶レビュー":
            return self._memory_review()

        if text == "古い記憶候補":
            return self._old_memory_candidates()

        if text == "重複記憶候補":
            return self._duplicate_memory_candidates()

        if text == "記憶安全確認":
            return self._memory_safety_check()

        return "対応していない記憶レビュー操作です。"

    def _memory_review(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        work_notes = self._load_json("data/work_notes/work_notes.json", [])
        project_memory = self._load_json("data/project/project_memory.json", {})

        old_count = len(self._find_old_entries(knowledge, work_notes))
        duplicate_count = len(self._find_duplicates(knowledge, work_notes))
        safety_notes = self._safety_findings(knowledge, work_notes, project_memory)

        lines = [
            "## Memory Review",
            "",
            "削除や自動修正はしません。候補表示だけです。",
            "",
            "### Counts",
            "",
            f"- Knowledge Entries: {len(knowledge) if isinstance(knowledge, list) else 0}",
            f"- Work Notes: {len(work_notes) if isinstance(work_notes, list) else 0}",
            f"- Old Candidates: {old_count}",
            f"- Duplicate Candidates: {duplicate_count}",
            f"- Safety Findings: {len(safety_notes)}",
            "",
            "### Next Checks",
            "",
            "- 古い記憶候補",
            "- 重複記憶候補",
            "- 記憶安全確認",
        ]

        return "\n".join(lines)

    def _old_memory_candidates(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        work_notes = self._load_json("data/work_notes/work_notes.json", [])
        candidates = self._find_old_entries(knowledge, work_notes)

        lines = [
            "## Old Memory Candidates",
            "",
            "v1では削除しません。古そうな候補を表示するだけです。",
            "",
        ]

        if not candidates:
            lines.append("- 古い記憶候補は見つかりませんでした。")
            return "\n".join(lines)

        for item in candidates[:20]:
            lines.append(f"- {item['type']} | {item['id']} | {item['title']} | {item['date']} | reason={item['reason']}")

        return "\n".join(lines)

    def _duplicate_memory_candidates(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        work_notes = self._load_json("data/work_notes/work_notes.json", [])
        duplicates = self._find_duplicates(knowledge, work_notes)

        lines = [
            "## Duplicate Memory Candidates",
            "",
            "v1では削除しません。重複らしい候補を表示するだけです。",
            "",
        ]

        if not duplicates:
            lines.append("- 重複候補は見つかりませんでした。")
            return "\n".join(lines)

        for item in duplicates[:20]:
            ids = ", ".join(item["ids"])
            lines.append(f"- {item['kind']} | {ids} | reason={item['reason']}")

        return "\n".join(lines)

    def _memory_safety_check(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        work_notes = self._load_json("data/work_notes/work_notes.json", [])
        project_memory = self._load_json("data/project/project_memory.json", {})
        findings = self._safety_findings(knowledge, work_notes, project_memory)

        lines = [
            "## Memory Safety Check",
            "",
            "削除や自動修正はしません。注意点を表示するだけです。",
            "",
        ]

        if not findings:
            lines.append("- 重大な注意点は見つかりませんでした。")
            return "\n".join(lines)

        for finding in findings:
            lines.append(f"- {finding}")

        return "\n".join(lines)

    def _load_json(self, path_text: str, default):
        path = Path(path_text)

        if not path.exists():
            return default

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _find_old_entries(self, knowledge, work_notes) -> list[dict]:
        now = datetime.now()
        old_items = []

        if isinstance(knowledge, list):
            for entry in knowledge:
                if not isinstance(entry, dict):
                    continue

                date_text = entry.get("updated_at") or entry.get("created_at") or ""
                parsed = self._parse_date(date_text)

                if not parsed:
                    continue

                age_days = (now - parsed).days
                category = entry.get("category", "unknown")

                if age_days >= 180 and category in {"world", "updates", "news"}:
                    old_items.append({
                        "type": "knowledge",
                        "id": entry.get("id", "unknown"),
                        "title": entry.get("title", "untitled"),
                        "date": date_text,
                        "reason": f"time-sensitive category older than {age_days} days",
                    })

                if age_days >= 365:
                    old_items.append({
                        "type": "knowledge",
                        "id": entry.get("id", "unknown"),
                        "title": entry.get("title", "untitled"),
                        "date": date_text,
                        "reason": f"older than {age_days} days",
                    })

        if isinstance(work_notes, list):
            for note in work_notes:
                if not isinstance(note, dict):
                    continue

                date_text = note.get("updated_at") or note.get("created_at") or ""
                parsed = self._parse_date(date_text)

                if not parsed:
                    continue

                age_days = (now - parsed).days

                if age_days >= 365:
                    old_items.append({
                        "type": "work_note",
                        "id": note.get("id", "unknown"),
                        "title": note.get("summary", "untitled"),
                        "date": date_text,
                        "reason": f"older than {age_days} days",
                    })

        return old_items

    def _find_duplicates(self, knowledge, work_notes) -> list[dict]:
        duplicates = []

        digest_map = {}
        source_path_map = {}
        title_map = {}

        if isinstance(knowledge, list):
            for entry in knowledge:
                if not isinstance(entry, dict):
                    continue

                entry_id = entry.get("id", "unknown")
                digest = entry.get("digest")
                source_path = entry.get("source_path")
                title = str(entry.get("title", "")).strip().lower()

                if digest:
                    digest_map.setdefault(digest, []).append(entry_id)

                if source_path:
                    source_path_map.setdefault(source_path, []).append(entry_id)

                if title:
                    title_map.setdefault(title, []).append(entry_id)

        if isinstance(work_notes, list):
            for note in work_notes:
                if not isinstance(note, dict):
                    continue

                memo_id = note.get("id", "unknown")
                digest = note.get("digest")
                summary = str(note.get("summary", "")).strip().lower()

                if digest:
                    digest_map.setdefault(digest, []).append(memo_id)

                if summary:
                    title_map.setdefault(summary, []).append(memo_id)

        for digest, ids in digest_map.items():
            if len(ids) > 1:
                duplicates.append({
                    "kind": "digest",
                    "ids": ids,
                    "reason": "same digest",
                })

        for source_path, ids in source_path_map.items():
            if len(ids) > 1:
                duplicates.append({
                    "kind": "source_path",
                    "ids": ids,
                    "reason": f"same source_path: {source_path}",
                })

        for title, ids in title_map.items():
            if len(ids) > 1:
                duplicates.append({
                    "kind": "title/summary",
                    "ids": ids,
                    "reason": f"same title or summary: {title[:60]}",
                })

        return duplicates

    def _safety_findings(self, knowledge, work_notes, project_memory) -> list[str]:
        findings = []

        if not Path("data/project/project_memory.json").exists():
            findings.append("project_memory.json が見つかりません。")

        if not Path("data/knowledge/knowledge.json").exists():
            findings.append("knowledge.json が見つかりません。")

        if not Path("data/work_notes/work_notes.json").exists():
            findings.append("work_notes.json がまだありません。作業メモを使うと作成されます。")

        search_settings = self._load_json("data/knowledge/search_settings.json", {})
        if isinstance(search_settings, dict) and search_settings.get("include_archived") is True:
            findings.append("Archive Filterがアーカイブ含む状態です。通常は除外がおすすめです。")

        auto_recall = self._load_json("data/knowledge/auto_recall_settings.json", {})
        if isinstance(auto_recall, dict) and auto_recall.get("enabled") is True:
            findings.append("Knowledge Auto RecallがONです。通常はOFFが安全です。")

        if isinstance(knowledge, list):
            archived_count = sum(1 for item in knowledge if isinstance(item, dict) and item.get("archived"))
            if archived_count:
                findings.append(f"Archived knowledge entries: {archived_count}")

            missing_source = [
                item.get("id", "unknown")
                for item in knowledge
                if isinstance(item, dict)
                and not item.get("source")
                and item.get("category") in {"papers", "research", "world", "imported"}
            ]

            if missing_source:
                findings.append(f"source が弱い知識候補: {', '.join(missing_source[:8])}")

        if isinstance(project_memory, dict):
            stage = project_memory.get("current_stage", "")
            if "v0.6" not in stage and "v0.5" in stage:
                findings.append("Project Memoryの現在地がまだv0.5系です。v0.6作業中なら後で同期してください。")

        return findings

    def _parse_date(self, date_text: str):
        if not date_text:
            return None

        candidates = [
            date_text,
            date_text.replace("Z", ""),
            date_text.split("+")[0],
        ]

        for item in candidates:
            try:
                return datetime.fromisoformat(item)
            except Exception:
                continue

        return None
