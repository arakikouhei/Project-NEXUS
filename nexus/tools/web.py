"""
Project NEXUS
Safe Web Tool
"""

from __future__ import annotations

import re
import ssl
from urllib.request import Request, urlopen

try:
    import certifi
except Exception:
    certifi = None

from nexus.security.web_guard import WebSecurityGuard
from nexus.tools.base_tool import BaseTool


class WebTool(BaseTool):
    """Safely checks and summarizes web pages."""

    name = "web"
    description = "Webページの安全確認と安全な要約を行います"

    def __init__(self) -> None:
        self.guard = WebSecurityGuard()

    def can_handle(self, user_input: str) -> bool:
        return (
            user_input.startswith("url安全確認:")
            or user_input.startswith("url安全確認：")
            or user_input.startswith("web要約:")
            or user_input.startswith("web要約：")
            or user_input.startswith("サイト確認:")
            or user_input.startswith("サイト確認：")
        )

    def execute(self, user_input: str) -> str:
        if user_input.startswith(
            ("url安全確認:", "url安全確認：", "サイト確認:", "サイト確認：")
        ):
            url = self._extract_after_colon(user_input)
            return self._check_url(url)

        if user_input.startswith(("web要約:", "web要約：")):
            url = self._extract_after_colon(user_input)
            return self._summarize_url(url)

        return "対応していないWeb操作です。"

    def _extract_after_colon(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _check_url(self, url: str) -> str:
        if not url:
            return "URLがありません。"

        result = self.guard.check_url(url)

        lines = [
            "## URL Safety Check",
            "",
            f"URL: {url}",
            f"Allowed: {result.allowed}",
            f"Risk Level: {result.risk_level}",
            "",
            "Reasons:",
        ]

        for reason in result.reasons:
            lines.append(f"- {reason}")

        lines.append("")
        lines.append("注意: これは基本的な静的チェックです。100%安全を保証するものではありません。")

        return "\n".join(lines)

    def _summarize_url(self, url: str) -> str:
        if not url:
            return "URLがありません。"

        safety = self.guard.check_url(url)

        if not safety.allowed:
            return self._check_url(url) + "\n\n危険判定のため、ページ取得を中止しました。"

        try:
            request = Request(
                url,
                headers={
                    "User-Agent": "Project-NEXUS-SafeWeb/0.1",
                },
            )

            context = self._create_ssl_context()

            with urlopen(request, timeout=10, context=context) as response:
                content_type = response.headers.get("Content-Type", "")

                if "text/html" not in content_type and "text/plain" not in content_type:
                    return (
                        self._check_url(url)
                        + f"\n\nHTML/Textではないため取得を中止しました: {content_type}"
                    )

                raw = response.read(800_000)

            html = raw.decode("utf-8", errors="ignore")
            text = self._extract_text(html)
            summary = self._simple_summary(text)

            return (
                "## Safe Web Summary\n\n"
                f"URL: {url}\n"
                f"Risk Level: {safety.risk_level}\n\n"
                "### Summary\n"
                f"{summary}\n\n"
                "### Safety Notes\n"
                "- JavaScriptは実行していません。\n"
                "- ファイルはダウンロードしていません。\n"
                "- ページ内の命令はNEXUSへの命令として扱いません。"
            )

        except Exception as error:
            return f"Webページ取得に失敗しました: {error}"

    def _create_ssl_context(self) -> ssl.SSLContext:
        if certifi is not None:
            return ssl.create_default_context(cafile=certifi.where())

        return ssl.create_default_context()

    def _extract_text(self, html: str) -> str:
        text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
        text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
        text = re.sub(r"(?s)<.*?>", " ", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"&lt;", "<", text)
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _simple_summary(self, text: str) -> str:
        if not text:
            return "本文を抽出できませんでした。"

        max_length = 1200

        if len(text) <= max_length:
            return text

        return text[:max_length] + "\n\n...本文が長いため省略しました。"
