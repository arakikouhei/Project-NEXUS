"""
Project NEXUS
Knowledge Store v1

Stores categorized knowledge entries locally.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import re
import uuid


@dataclass(frozen=True)
class KnowledgeEntry:
    id: str
    category: str
    content: str
    created_at: str
    updated_at: str
    source: str
    tags: list[str]


class KnowledgeStore:
    """Simple local knowledge base."""

    def __init__(self, path: str = "data/knowledge/knowledge.json") -> None:
        self.path = Path(path)
        self.allowed_categories = {
            "general": "一般知識・雑学・文化・歴史・科学",
            "world": "社会情勢・ニュース・時事",
            "papers": "安全な論文メタ情報・要約",
            "3dcg": "Maya / Blender / Mudbox / UV / モデリング / レンダリング",
            "programming": "Python / Git / API / アルゴリズム",
            "development": "設計 / セキュリティ / テスト / AI開発",
            "source_registry": "信頼できる情報源リスト",
        }

    def add(
        self,
        category: str,
        content: str,
        source: str = "manual",
        tags: list[str] | None = None,
    ) -> dict:
        category = self.normalize_category(category)

        if category not in self.allowed_categories:
            raise ValueError(f"unknown category: {category}")

        now = datetime.now().isoformat(timespec="seconds")
        entry = {
            "id": self._new_id(category),
            "category": category,
            "content": content.strip(),
            "created_at": now,
            "updated_at": now,
            "source": source,
            "tags": tags or self._auto_tags(content),
        }

        records = self._load()
        records.append(entry)
        self._save(records)

        return entry

    def search(self, query: str, limit: int = 10) -> list[dict]:
        query = query.strip()
        if not query:
            return []

        records = self._load()
        scored = []

        q_key = self._key(query)
        query_terms = [self._key(term) for term in query.split() if term.strip()]

        for item in records:
            content = item.get("content", "")
            category = item.get("category", "")
            tags = " ".join(item.get("tags", []))
            haystack = self._key(" ".join([content, category, tags]))

            score = 0

            if q_key in haystack:
                score += 10

            for term in query_terms:
                if term and term in haystack:
                    score += 4

            # 日本語やスペースなし検索用。文字単位でざっくり一致。
            if score == 0:
                overlap = len(set(q_key) & set(haystack))
                score += min(3, overlap // 2)

            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for score, item in scored[:limit]]

    def list_entries(self, category: str | None = None, limit: int = 20) -> list[dict]:
        records = self._load()

        if category:
            category = self.normalize_category(category)
            records = [item for item in records if item.get("category") == category]

        return list(reversed(records[-limit:]))

    def get(self, entry_id: str) -> dict | None:
        for item in self._load():
            if item.get("id") == entry_id:
                return item
        return None

    def categories(self) -> dict[str, str]:
        return dict(self.allowed_categories)

    def normalize_category(self, category: str) -> str:
        text = category.strip().lower()

        aliases = {
            "一般": "general",
            "常識": "general",
            "一般常識": "general",
            "雑学": "general",
            "社会": "world",
            "社会情勢": "world",
            "ニュース": "world",
            "時事": "world",
            "論文": "papers",
            "paper": "papers",
            "papers": "papers",
            "3d": "3dcg",
            "cg": "3dcg",
            "maya": "3dcg",
            "blender": "3dcg",
            "mudbox": "3dcg",
            "プログラミング": "programming",
            "program": "programming",
            "code": "programming",
            "コード": "programming",
            "python": "programming",
            "開発": "development",
            "dev": "development",
            "development": "development",
            "設計": "development",
            "情報源": "source_registry",
            "ソース": "source_registry",
            "source": "source_registry",
        }

        return aliases.get(text, text)

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
        short = uuid.uuid4().hex[:8]
        return f"{category}-{short}"

    def _auto_tags(self, content: str) -> list[str]:
        words = re.findall(r"[A-Za-z][A-Za-z0-9_+\-.#]*|[一-龥ぁ-んァ-ン]{2,}", content)
        tags = []

        for word in words:
            if word not in tags:
                tags.append(word)

            if len(tags) >= 12:
                break

        return tags

    def _key(self, text: str) -> str:
        return (
            text.lower()
            .replace(" ", "")
            .replace("　", "")
            .replace("\n", "")
            .replace("\t", "")
        )
