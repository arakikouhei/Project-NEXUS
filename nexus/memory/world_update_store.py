"""
Project NEXUS
World Update Store v1

Stores time-sensitive update logs.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import json
import uuid


class WorldUpdateStore:
    """Stores RSS/news update entries locally."""

    def __init__(
        self,
        updates_path: str = "data/knowledge/world_updates.json",
        sources_path: str = "data/knowledge/world_update_sources.json",
    ) -> None:
        self.updates_path = Path(updates_path)
        self.sources_path = Path(sources_path)

    def sources(self, category: str | None = None) -> list[dict]:
        records = self._load_json(self.sources_path)

        if category:
            records = [
                item for item in records
                if item.get("category") == category
                and item.get("status", "active") == "active"
            ]

        return records

    def add_source(
        self,
        category: str,
        name: str,
        url: str,
        note: str = "",
        ttl_days: int = 7,
    ) -> dict:
        records = self._load_json(self.sources_path)
        now = datetime.now().isoformat(timespec="seconds")

        for item in records:
            if item.get("url") == url:
                item["category"] = category
                item["name"] = name
                item["note"] = note
                item["ttl_days"] = ttl_days
                item["updated_at"] = now
                self._save_json(self.sources_path, records)
                return item

        entry = {
            "id": f"update-{category}-{uuid.uuid4().hex[:8]}",
            "category": category,
            "name": name,
            "url": url,
            "note": note,
            "trust_level": "medium",
            "ttl_days": ttl_days,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        }

        records.append(entry)
        self._save_json(self.sources_path, records)
        return entry

    def add_updates(self, source: dict, items: list[dict]) -> tuple[int, int]:
        records = self._load_json(self.updates_path)
        existing_links = {item.get("link") for item in records}
        now = datetime.now()
        new_count = 0
        skipped_count = 0

        ttl_days = int(source.get("ttl_days", 7) or 7)
        expires_at = (now + timedelta(days=ttl_days)).isoformat(timespec="seconds")

        for item in items:
            link = item.get("link", "")

            if not link or link in existing_links:
                skipped_count += 1
                continue

            entry = {
                "id": f"world-{uuid.uuid4().hex[:8]}",
                "category": source.get("category", "world"),
                "source_id": source.get("id", ""),
                "source_name": source.get("name", ""),
                "source_url": source.get("url", ""),
                "title": item.get("title", ""),
                "link": link,
                "published": item.get("published", ""),
                "summary": item.get("summary", ""),
                "fetched_at": now.isoformat(timespec="seconds"),
                "expires_at": expires_at,
                "trust_level": source.get("trust_level", "medium"),
            }

            records.append(entry)
            existing_links.add(link)
            new_count += 1

        records = records[-500:]
        self._save_json(self.updates_path, records)

        return new_count, skipped_count

    def recent(self, category: str | None = None, limit: int = 20) -> list[dict]:
        records = self._load_json(self.updates_path)

        if category:
            records = [item for item in records if item.get("category") == category]

        return list(reversed(records[-limit:]))

    def status(self) -> dict:
        records = self._load_json(self.updates_path)
        sources = self._load_json(self.sources_path)
        now = datetime.now()

        expired = 0
        active = 0

        for item in records:
            expires_at = item.get("expires_at", "")
            try:
                expires_dt = datetime.fromisoformat(expires_at)
            except Exception:
                expires_dt = now

            if expires_dt < now:
                expired += 1
            else:
                active += 1

        by_category: dict[str, int] = {}
        for item in records:
            category = item.get("category", "unknown")
            by_category[category] = by_category.get(category, 0) + 1

        return {
            "sources": len(sources),
            "updates": len(records),
            "active": active,
            "expired": expired,
            "by_category": by_category,
        }

    def _load_json(self, path: Path) -> list[dict]:
        if not path.exists():
            return []

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []

    def _save_json(self, path: Path, data: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
