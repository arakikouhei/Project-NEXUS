"""
Project NEXUS
Source Registry Store v1

Stores trusted or semi-trusted information sources.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import uuid


class SourceRegistryStore:
    """Local registry for information sources."""

    def __init__(self, path: str = "data/knowledge/source_registry.json") -> None:
        self.path = Path(path)
        self.allowed_categories = {
            "general": "一般知識・辞典・百科事典",
            "world": "社会情勢・ニュース・時事",
            "papers": "論文・研究・学術情報",
            "3dcg": "3DCG・DCCツール・CG制作",
            "programming": "プログラミング・公式ドキュメント",
            "development": "開発・設計・セキュリティ",
            "official": "企業・大学・団体などの公式サイト",
        }

    def add(
        self,
        category: str,
        name: str,
        url: str,
        note: str = "",
        trust_level: str = "medium",
    ) -> dict:
        category = self.normalize_category(category)
        trust_level = self.normalize_trust_level(trust_level)

        if category not in self.allowed_categories:
            raise ValueError(f"unknown category: {category}")

        if not self._looks_like_url(url):
            raise ValueError("URLの形式が正しくありません。http:// または https:// で始めてください。")

        records = self._load()
        now = datetime.now().isoformat(timespec="seconds")

        # 同じURLは重複登録しない
        for item in records:
            if item.get("url") == url:
                item["updated_at"] = now
                item["category"] = category
                item["name"] = name.strip()
                item["note"] = note.strip()
                item["trust_level"] = trust_level
                self._save(records)
                return item

        entry = {
            "id": self._new_id(category),
            "category": category,
            "name": name.strip(),
            "url": url.strip(),
            "note": note.strip(),
            "trust_level": trust_level,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        }

        records.append(entry)
        self._save(records)
        return entry

    def search(self, query: str, limit: int = 10) -> list[dict]:
        query = query.strip()
        if not query:
            return []

        records = self._load()
        q_key = self._key(query)
        results = []

        for item in records:
            haystack = self._key(
                " ".join(
                    [
                        item.get("category", ""),
                        item.get("name", ""),
                        item.get("url", ""),
                        item.get("note", ""),
                        item.get("trust_level", ""),
                    ]
                )
            )

            score = 0

            if q_key in haystack:
                score += 10

            for term in query.split():
                if self._key(term) in haystack:
                    score += 4

            if score > 0:
                results.append((score, item))

        results.sort(key=lambda pair: pair[0], reverse=True)
        return [item for score, item in results[:limit]]

    def list_sources(self, category: str | None = None, limit: int = 50) -> list[dict]:
        records = self._load()

        if category:
            normalized = self.normalize_category(category)
            records = [item for item in records if item.get("category") == normalized]

        return list(reversed(records[-limit:]))

    def get(self, source_id: str) -> dict | None:
        for item in self._load():
            if item.get("id") == source_id:
                return item
        return None

    def categories(self) -> dict[str, str]:
        return dict(self.allowed_categories)

    def normalize_category(self, category: str) -> str:
        text = category.strip().lower()

        aliases = {
            "一般": "general",
            "常識": "general",
            "辞典": "general",
            "社会": "world",
            "社会情勢": "world",
            "ニュース": "world",
            "時事": "world",
            "論文": "papers",
            "paper": "papers",
            "papers": "papers",
            "研究": "papers",
            "学術": "papers",
            "3d": "3dcg",
            "cg": "3dcg",
            "3dcg": "3dcg",
            "maya": "3dcg",
            "blender": "3dcg",
            "プログラミング": "programming",
            "programming": "programming",
            "python": "programming",
            "コード": "programming",
            "開発": "development",
            "dev": "development",
            "development": "development",
            "設計": "development",
            "セキュリティ": "development",
            "公式": "official",
            "official": "official",
        }

        return aliases.get(text, text)

    def normalize_trust_level(self, trust_level: str) -> str:
        text = trust_level.strip().lower()

        aliases = {
            "高": "high",
            "高い": "high",
            "公式": "high",
            "中": "medium",
            "普通": "medium",
            "低": "low",
            "低い": "low",
        }

        text = aliases.get(text, text)

        if text not in {"high", "medium", "low"}:
            return "medium"

        return text

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []

    def _save(self, records: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _new_id(self, category: str) -> str:
        return f"source-{category}-{uuid.uuid4().hex[:8]}"

    def _looks_like_url(self, url: str) -> bool:
        lowered = url.strip().lower()
        return lowered.startswith("https://") or lowered.startswith("http://")

    def _key(self, text: str) -> str:
        return (
            text.lower()
            .replace(" ", "")
            .replace("　", "")
            .replace("\n", "")
            .replace("\t", "")
        )
