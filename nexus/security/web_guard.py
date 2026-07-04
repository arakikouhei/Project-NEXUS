"""
Project NEXUS
Web Security Guard
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
import ipaddress


@dataclass
class URLSafetyResult:
    url: str
    allowed: bool
    risk_level: str
    reasons: list[str]


class WebSecurityGuard:
    """Checks URLs before web access."""

    def __init__(self) -> None:
        self.blocked_suffixes = {
            ".exe",
            ".dmg",
            ".pkg",
            ".command",
            ".sh",
            ".bat",
            ".ps1",
            ".scr",
            ".jar",
            ".app",
        }

        self.warning_suffixes = {
            ".zip",
            ".rar",
            ".7z",
            ".tar",
            ".gz",
        }

        self.shorteners = {
            "bit.ly",
            "tinyurl.com",
            "t.co",
            "goo.gl",
            "ow.ly",
            "is.gd",
            "buff.ly",
        }

    def check_url(self, url: str) -> URLSafetyResult:
        reasons = []

        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            reasons.append("http/https以外のURLです。")
            return URLSafetyResult(url, False, "blocked", reasons)

        if parsed.scheme == "http":
            reasons.append("httpsではなくhttpです。通信が暗号化されません。")

        host = parsed.hostname or ""

        if not host:
            reasons.append("ホスト名がありません。")
            return URLSafetyResult(url, False, "blocked", reasons)

        if self._is_ip_address(host):
            reasons.append("IPアドレス直打ちURLです。")

        if host.lower() in self.shorteners:
            reasons.append("短縮URLです。リンク先が不透明です。")

        lowered_path = parsed.path.lower()

        for suffix in self.blocked_suffixes:
            if lowered_path.endswith(suffix):
                reasons.append(f"危険な可能性のあるファイル形式です: {suffix}")
                return URLSafetyResult(url, False, "blocked", reasons)

        for suffix in self.warning_suffixes:
            if lowered_path.endswith(suffix):
                reasons.append(f"圧縮ファイルです。自動取得は避けます: {suffix}")

        if reasons:
            return URLSafetyResult(url, True, "warning", reasons)

        return URLSafetyResult(url, True, "low", ["基本チェックでは大きな問題は見つかりませんでした。"])

    def _is_ip_address(self, host: str) -> bool:
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False
