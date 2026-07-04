"""
Project NEXUS
Safe Research Tool v1

Safe first-step research using Wikipedia API.
This is not a full web search engine.
"""

from __future__ import annotations

import json
import ssl
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

try:
    import certifi
except Exception:
    certifi = None

from nexus.personality.entity_resolver import EntityResolver
from nexus.tools.base_tool import BaseTool


class SafeResearchTool(BaseTool):
    """Safely researches terms using Wikipedia as a first source."""

    name = "safe_research"
    description = "知らない用語や略称を安全に調べます"

    def __init__(self) -> None:
        self.entity_resolver = EntityResolver()

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("調べて:")
            or text.startswith("調べて：")
            or text.startswith("用語確認:")
            or text.startswith("用語確認：")
            or text.startswith("wiki検索:")
            or text.startswith("wiki検索：")
            or text.endswith("について調べて")
        )

    def execute(self, user_input: str) -> str:
        query = self._extract_query(user_input)

        if not query:
            return "調べる言葉がありません。"

        normalized_query = self._normalize_entity(query)

        try:
            result = self._wikipedia_summary(normalized_query)
        except Exception as error:
            return (
                "調査に失敗しました。\n\n"
                f"原因: {error}\n\n"
                "ネット接続、SSL証明書、またはWikipedia側の応答が原因の可能性があります。"
            )

        if result:
            alias_note = ""
            if normalized_query != query:
                alias_note = f"解釈: 「{query}」→「{normalized_query}」\n\n"

            return alias_note + result

        if normalized_query != query:
            return (
                f"「{query}」は「{normalized_query}」として調べましたが、"
                "Wikipediaでは十分な情報を見つけられませんでした。"
            )

        return f"「{query}」について、Wikipediaでは十分な情報を見つけられませんでした。"

    def _extract_query(self, user_input: str) -> str:
        text = user_input.strip()

        for prefix in ["調べて:", "調べて：", "用語確認:", "用語確認：", "wiki検索:", "wiki検索："]:
            if text.startswith(prefix):
                return text[len(prefix):].strip()

        if text.endswith("について調べて"):
            return text.removesuffix("について調べて").strip()

        return text

    def _normalize_entity(self, query: str) -> str:
        matches = self.entity_resolver.find_matches(query)

        if matches:
            return matches[0].canonical

        return query

    def _wikipedia_summary(self, query: str) -> str | None:
        title = self._search_title(query)

        if not title:
            return None

        extract, page_url = self._fetch_extract(title)

        if not extract:
            return None

        if len(extract) > 900:
            extract = extract[:900].rstrip() + "..."

        return (
            "## Safe Research Result\n\n"
            f"検索語: {query}\n"
            f"見つかった項目: {title}\n\n"
            f"{extract}\n\n"
            "注意: Wikipediaベースの初期調査です。"
            "入試・学費・出願日程などの最新情報は公式サイト確認が必要です。\n"
            f"URL: {page_url}"
        )

    def _search_title(self, query: str) -> str | None:
        params = urlencode(
            {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": 1,
                "format": "json",
            }
        )

        url = f"https://ja.wikipedia.org/w/api.php?{params}"
        data = self._get_json(url)

        results = data.get("query", {}).get("search", [])

        if not results:
            return None

        return results[0].get("title")

    def _fetch_extract(self, title: str) -> tuple[str | None, str]:
        params = urlencode(
            {
                "action": "query",
                "prop": "extracts|info",
                "exintro": "1",
                "explaintext": "1",
                "redirects": "1",
                "inprop": "url",
                "titles": title,
                "format": "json",
            }
        )

        url = f"https://ja.wikipedia.org/w/api.php?{params}"
        data = self._get_json(url)

        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            extract = page.get("extract")
            fullurl = page.get("fullurl") or f"https://ja.wikipedia.org/wiki/{quote(title)}"

            if extract:
                return extract, fullurl

        return None, f"https://ja.wikipedia.org/wiki/{quote(title)}"

    def _get_json(self, url: str) -> dict:
        request = Request(
            url,
            headers={
                "User-Agent": "Project-NEXUS-SafeResearch/0.1",
            },
        )

        context = self._ssl_context()

        with urlopen(request, timeout=10, context=context) as response:
            raw = response.read(800_000)

        return json.loads(raw.decode("utf-8", errors="ignore"))

    def _ssl_context(self) -> ssl.SSLContext:
        if certifi is not None:
            return ssl.create_default_context(cafile=certifi.where())

        return ssl.create_default_context()
