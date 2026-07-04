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
