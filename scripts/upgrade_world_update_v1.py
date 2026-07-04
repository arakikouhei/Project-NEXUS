from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import json
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "world_update_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return

    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def write(path_text: str, content: str) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def patch_gitignore() -> None:
    path = ROOT / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.exists() else ""

    additions = [
        "data/knowledge/world_updates.json",
    ]

    changed = False
    for item in additions:
        if item not in text:
            text = text.rstrip() + "\n" + item + "\n"
            changed = True

    if changed:
        path.write_text(text, encoding="utf-8")


def seed_update_sources() -> None:
    path = ROOT / "data/knowledge/world_update_sources.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, list) and existing:
                return
        except Exception:
            pass

    now = datetime.now().isoformat(timespec="seconds")

    sources = [
        {
            "id": "update-world-google-news-jp",
            "category": "world",
            "name": "Google News JP / World",
            "url": "https://news.google.com/rss/search?q=%E4%B8%96%E7%95%8C%E6%83%85%E5%8B%A2&hl=ja&gl=JP&ceid=JP:ja",
            "note": "世界情勢のRSS検索。複数媒体の見出し確認用。",
            "trust_level": "medium",
            "ttl_days": 3,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        },
        {
            "id": "update-ai-google-news-jp",
            "category": "ai",
            "name": "Google News JP / AI",
            "url": "https://news.google.com/rss/search?q=AI%20%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD&hl=ja&gl=JP&ceid=JP:ja",
            "note": "AI関連ニュースのRSS検索。",
            "trust_level": "medium",
            "ttl_days": 7,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        },
        {
            "id": "update-3dcg-google-news-jp",
            "category": "3dcg",
            "name": "Google News JP / 3DCG",
            "url": "https://news.google.com/rss/search?q=3DCG%20Maya%20Blender&hl=ja&gl=JP&ceid=JP:ja",
            "note": "3DCG・Maya・Blender関連ニュースのRSS検索。",
            "trust_level": "medium",
            "ttl_days": 14,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        },
        {
            "id": "update-dev-google-news-jp",
            "category": "development",
            "name": "Google News JP / Software Development",
            "url": "https://news.google.com/rss/search?q=%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E9%96%8B%E7%99%BA%20Python%20GitHub&hl=ja&gl=JP&ceid=JP:ja",
            "note": "開発・Python・GitHub関連ニュースのRSS検索。",
            "trust_level": "medium",
            "ttl_days": 14,
            "created_at": now,
            "updated_at": now,
            "status": "active",
        },
    ]

    path.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_world_update_store() -> None:
    write(
        "nexus/memory/world_update_store.py",
        r'''
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
        ''',
    )


def write_world_update_tool() -> None:
    write(
        "nexus/tools/world_update.py",
        r'''
        """
        Project NEXUS
        World Update Tool v1

        Fetches RSS updates from registered update sources.
        """

        from __future__ import annotations

        from html import unescape
        import re
        import ssl
        import xml.etree.ElementTree as ET
        from urllib.request import Request, urlopen

        try:
            import certifi
        except Exception:
            certifi = None

        from nexus.memory.world_update_store import WorldUpdateStore
        from nexus.tools.base_tool import BaseTool


        class WorldUpdateTool(BaseTool):
            """Fetches and stores time-sensitive world/news updates."""

            name = "world_update"
            description = "社会情勢・AI・3DCG・開発系の更新情報を取得します"

            def __init__(self) -> None:
                self.store = WorldUpdateStore()
                self.max_items_per_source = 8

            def can_handle(self, user_input: str) -> bool:
                text = user_input.strip()

                return (
                    text == "更新ヘルプ"
                    or text == "知識更新状況"
                    or text == "更新ソース一覧"
                    or text == "更新ログ一覧"
                    or text.startswith("更新ログ一覧:")
                    or text.startswith("更新ログ一覧：")
                    or text.startswith("更新ソース追加:")
                    or text.startswith("更新ソース追加：")
                    or text in {
                        "世界情勢更新",
                        "社会情勢更新",
                        "AIニュース更新",
                        "3DCGニュース更新",
                        "開発ニュース更新",
                    }
                )

            def execute(self, user_input: str) -> str:
                text = user_input.strip()

                if text == "更新ヘルプ":
                    return self._help()

                if text == "知識更新状況":
                    return self._status()

                if text == "更新ソース一覧":
                    return self._source_list()

                if text == "更新ログ一覧":
                    return self._logs(None)

                if text.startswith(("更新ログ一覧:", "更新ログ一覧：")):
                    category = self._after_separator(text)
                    return self._logs(category)

                if text.startswith(("更新ソース追加:", "更新ソース追加：")):
                    body = self._after_separator(text)
                    return self._add_source(body)

                mapping = {
                    "世界情勢更新": "world",
                    "社会情勢更新": "world",
                    "AIニュース更新": "ai",
                    "3DCGニュース更新": "3dcg",
                    "開発ニュース更新": "development",
                }

                if text in mapping:
                    return self._update_category(mapping[text])

                return "対応していない更新操作です。"

            def _after_separator(self, text: str) -> str:
                for separator in [":", "："]:
                    if separator in text:
                        return text.split(separator, 1)[1].strip()
                return ""

            def _update_category(self, category: str) -> str:
                sources = self.store.sources(category=category)

                if not sources:
                    return f"## World Update\n\nカテゴリ '{category}' の更新ソースが登録されていません。"

                lines = [
                    "## World Update",
                    "",
                    f"Category: {category}",
                    "",
                ]

                total_new = 0
                total_skipped = 0
                total_errors = 0

                for source in sources:
                    lines.append(f"### Source: {source.get('name')}")
                    lines.append(f"- URL: {source.get('url')}")

                    try:
                        items = self._fetch_rss(source.get("url", ""))
                        new_count, skipped_count = self.store.add_updates(source, items)
                        total_new += new_count
                        total_skipped += skipped_count

                        lines.append(f"- Fetched Items: {len(items)}")
                        lines.append(f"- New: {new_count}")
                        lines.append(f"- Skipped Duplicate: {skipped_count}")

                        for item in items[:3]:
                            lines.append(f"  - {item.get('title')}")

                    except Exception as error:
                        total_errors += 1
                        lines.append(f"- Error: {error}")

                    lines.append("")

                lines.append("### Summary")
                lines.append(f"- Total New: {total_new}")
                lines.append(f"- Total Skipped: {total_skipped}")
                lines.append(f"- Errors: {total_errors}")
                lines.append("")
                lines.append("Notes:")
                lines.append("- これはRSS見出しベースの更新です。")
                lines.append("- ニュースは古くなるため、expires_at付きで保存します。")
                lines.append("- 重要な判断には複数ソース確認が必要です。")

                return "\n".join(lines).rstrip()

            def _fetch_rss(self, url: str) -> list[dict]:
                request = Request(
                    url,
                    headers={
                        "User-Agent": "Project-NEXUS-WorldUpdate/0.1",
                    },
                )

                with urlopen(request, timeout=12, context=self._ssl_context()) as response:
                    raw = response.read(1_200_000)

                root = ET.fromstring(raw)

                items = []

                for item in root.findall(".//item"):
                    title = self._text(item, "title")
                    link = self._text(item, "link")
                    published = self._text(item, "pubDate")
                    description = self._text(item, "description")

                    if not title or not link:
                        continue

                    items.append(
                        {
                            "title": self._clean(title),
                            "link": link.strip(),
                            "published": published.strip(),
                            "summary": self._clean(description),
                        }
                    )

                    if len(items) >= self.max_items_per_source:
                        break

                return items

            def _text(self, item, tag: str) -> str:
                found = item.find(tag)
                if found is None or found.text is None:
                    return ""
                return found.text

            def _clean(self, text: str) -> str:
                text = unescape(text or "")
                text = re.sub(r"(?is)<.*?>", " ", text)
                text = re.sub(r"\s+", " ", text)
                return text.strip()

            def _ssl_context(self) -> ssl.SSLContext:
                if certifi is not None:
                    return ssl.create_default_context(cafile=certifi.where())
                return ssl.create_default_context()

            def _source_list(self) -> str:
                sources = self.store.sources()

                if not sources:
                    return "## Update Sources\n\n更新ソースはまだ登録されていません。"

                lines = ["## Update Sources", ""]

                for item in sources:
                    lines.append(f"### {item.get('id')}")
                    lines.append(f"- Category: {item.get('category')}")
                    lines.append(f"- Name: {item.get('name')}")
                    lines.append(f"- URL: {item.get('url')}")
                    lines.append(f"- TTL Days: {item.get('ttl_days')}")
                    lines.append(f"- Note: {item.get('note')}")
                    lines.append("")

                return "\n".join(lines).rstrip()

            def _add_source(self, body: str) -> str:
                parts = [part.strip() for part in body.split("|")]

                if len(parts) < 3:
                    return (
                        "形式が違います。\n\n"
                        "例:\n"
                        "更新ソース追加: ai | AI News | https://example.com/rss | 7"
                    )

                category = parts[0]
                name = parts[1]
                url = parts[2]
                ttl_days = int(parts[3]) if len(parts) >= 4 and parts[3].isdigit() else 7
                note = parts[4] if len(parts) >= 5 else ""

                entry = self.store.add_source(
                    category=category,
                    name=name,
                    url=url,
                    note=note,
                    ttl_days=ttl_days,
                )

                return (
                    "## Update Source Added\n\n"
                    f"- ID: {entry.get('id')}\n"
                    f"- Category: {entry.get('category')}\n"
                    f"- Name: {entry.get('name')}\n"
                    f"- URL: {entry.get('url')}\n"
                    f"- TTL Days: {entry.get('ttl_days')}"
                )

            def _logs(self, category: str | None) -> str:
                category = category.strip() if category else None
                logs = self.store.recent(category=category, limit=20)

                title = "## Update Logs"
                if category:
                    title += f" / {category}"

                if not logs:
                    return title + "\n\nまだ更新ログはありません。"

                lines = [title, ""]

                for item in logs:
                    lines.append(f"### {item.get('title')}")
                    lines.append(f"- Category: {item.get('category')}")
                    lines.append(f"- Source: {item.get('source_name')}")
                    lines.append(f"- Published: {item.get('published')}")
                    lines.append(f"- Fetched: {item.get('fetched_at')}")
                    lines.append(f"- Expires: {item.get('expires_at')}")
                    lines.append(f"- URL: {item.get('link')}")
                    summary = item.get("summary", "")
                    if summary:
                        if len(summary) > 220:
                            summary = summary[:220].rstrip() + "..."
                        lines.append(f"- Summary: {summary}")
                    lines.append("")

                return "\n".join(lines).rstrip()

            def _status(self) -> str:
                status = self.store.status()

                lines = [
                    "## Knowledge Update Status",
                    "",
                    f"- Sources: {status.get('sources')}",
                    f"- Updates: {status.get('updates')}",
                    f"- Active Updates: {status.get('active')}",
                    f"- Expired Updates: {status.get('expired')}",
                    "",
                    "### By Category",
                ]

                by_category = status.get("by_category", {})

                if not by_category:
                    lines.append("- No updates yet.")
                else:
                    for category, count in by_category.items():
                        lines.append(f"- {category}: {count}")

                return "\n".join(lines)

            def _help(self) -> str:
                return (
                    "## World Update Help\n\n"
                    "使えるコマンド:\n"
                    "- 更新ソース一覧\n"
                    "- 世界情勢更新\n"
                    "- AIニュース更新\n"
                    "- 3DCGニュース更新\n"
                    "- 開発ニュース更新\n"
                    "- 更新ログ一覧\n"
                    "- 更新ログ一覧: ai\n"
                    "- 知識更新状況\n"
                    "- 更新ソース追加: ai | AI News | https://example.com/rss | 7\n\n"
                    "保存先:\n"
                    "- data/knowledge/world_updates.json\n"
                    "- data/knowledge/world_update_sources.json\n\n"
                    "注意:\n"
                    "- v1はRSS見出しベースです。\n"
                    "- 社会情勢は古くなるため期限付きで保存します。\n"
                    "- 重要情報は複数ソースで確認してください。"
                )
        ''',
    )


def patch_manager() -> None:
    path = ROOT / "nexus/tools/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.tools.world_update import WorldUpdateTool" not in text:
        text = text.replace(
            "from nexus.tools.source_registry import SourceRegistryTool\n",
            "from nexus.tools.source_registry import SourceRegistryTool\n"
            "from nexus.tools.world_update import WorldUpdateTool\n",
            1,
        )

    if "self.register(WorldUpdateTool())" not in text:
        text = text.replace(
            "        self.register(SourceRegistryTool())\n",
            "        self.register(SourceRegistryTool())\n"
            "        self.register(WorldUpdateTool())\n",
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_agent_bypass() -> None:
    path = ROOT / "nexus/agent/agent.py"
    text = path.read_text(encoding="utf-8")

    if "# WORLD_UPDATE_ROUTING_BYPASS_V1" in text:
        return

    target = '''        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)
'''

    insert = '''        # WORLD_UPDATE_ROUTING_BYPASS_V1
        update_prefixes = (
            "更新ヘルプ",
            "知識更新状況",
            "更新ソース一覧",
            "更新ログ一覧",
            "更新ログ一覧:",
            "更新ログ一覧：",
            "更新ソース追加:",
            "更新ソース追加：",
            "世界情勢更新",
            "社会情勢更新",
            "AIニュース更新",
            "3DCGニュース更新",
            "開発ニュース更新",
        )

        if stripped_input.startswith(update_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)
'''

    if target not in text:
        raise SystemExit("agent.py の挿入位置が見つかりません。")

    text = text.replace(target, insert, 1)
    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"知識更新状況"' not in text:
        text = text.replace(
            '                    "情報源検索: arXiv",\n',
            '                    "情報源検索: arXiv",\n'
            '                    "更新ヘルプ",\n'
            '                    "知識更新状況",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        path.write_text("あなたは Project NEXUS です。\n", encoding="utf-8")

    text = path.read_text(encoding="utf-8")
    marker = "# World Update v1"

    if marker in text:
        return

    addition = """

# World Update v1

NEXUSはRSSベースで社会情勢・AI・3DCG・開発系の更新情報を取得できます。

使える例:
- 更新ヘルプ
- 世界情勢更新
- AIニュース更新
- 3DCGニュース更新
- 開発ニュース更新
- 更新ログ一覧
- 知識更新状況

方針:
- v1はRSS見出しベースであり、完全な事実確認ではない
- 社会情勢は期限付き知識として扱う
- 重要情報は複数ソースで確認する
- 取得日時・情報源・URLを残す
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/WORLD_UPDATE_V1.md",
        """
        # World Update v1

        RSS-based update intake for time-sensitive information.

        ## Commands

        - 更新ヘルプ
        - 更新ソース一覧
        - 世界情勢更新
        - AIニュース更新
        - 3DCGニュース更新
        - 開発ニュース更新
        - 更新ログ一覧
        - 知識更新状況

        ## Storage

        - data/knowledge/world_update_sources.json
        - data/knowledge/world_updates.json

        `world_updates.json` is ignored by Git because it changes frequently.

        ## Limits

        v1 is RSS headline-based.
        It is not a complete fact-checking system.
        """,
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        ".gitignore",
        "nexus/memory/world_update_store.py",
        "nexus/tools/world_update.py",
        "nexus/tools/manager.py",
        "nexus/agent/agent.py",
        "nexus/tools/diagnostics.py",
        "prompts/system_prompt.txt",
        "data/knowledge/world_update_sources.json",
    ]:
        backup(target)

    patch_gitignore()
    seed_update_sources()
    write_world_update_store()
    write_world_update_tool()
    patch_manager()
    patch_agent_bypass()
    patch_diagnostics()
    patch_system_prompt()
    write_docs()

    print("World Update v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
