"""
Project NEXUS
Input Normalizer
"""

from __future__ import annotations

from dataclasses import dataclass
import difflib
import unicodedata


@dataclass(frozen=True)
class NormalizedInput:
    original: str
    text: str
    corrected: bool


class InputNormalizer:
    """Corrects small typos in user commands."""

    def __init__(self) -> None:
        self.known_commands = [
            "nexus状況",
            "状況確認",
            "今の状態",
            "ダッシュボード",
            "できること",
            "機能一覧",
            "ヘルプ",
            "システム情報",
            "ハードウェア状態",
            "球体準備",
            "球体状態",
            "移行内容確認",
            "移行パッケージ作成",
            "テスト実行",
            "git要約",
            "git状態",
            "変更確認",
            "差分確認",
            "最近のコミット",
            "コミット履歴",
            "ブランチ確認",
            "コミット準備",
            "作業ログ",
            "最近の作業",
            "pwd",
            "ls",
            "git status",
            "git log --oneline -5",
        ]

        self.prefix_commands = [
            "読み上げ",
            "話して",
            "作業記録",
            "コミットして",
        ]

        self.aliases = {
            "ダシュボード": "ダッシュボード",
            "ダッシュボド": "ダッシュボード",
            "ダッシュボート": "ダッシュボード",
            "nexusじょうきょう": "nexus状況",
            "ネクサス状況": "nexus状況",
            "今の状況": "今の状態",
            "できる事": "できること",
            "なにができる": "できること",
            "何が出来る": "できること",
            "システム状況": "システム情報",
            "システム確認": "システム情報",
            "ハードウエア状態": "ハードウェア状態",
            "ハードウェア状況": "ハードウェア状態",
            "球体状況": "球体状態",
            "球体確認": "球体準備",
            "移行内容確忍": "移行内容確認",
            "移行内容": "移行内容確認",
            "移行パッケジ作成": "移行パッケージ作成",
            "移行パッケージ": "移行パッケージ作成",
            "転送パッケージ作成": "移行パッケージ作成",
            "テスト": "テスト実行",
            "てすと実行": "テスト実行",
            "git用約": "git要約",
            "git要役": "git要約",
            "gitようやく": "git要約",
            "git状況": "git状態",
            "変更状況": "変更確認",
            "変更確忍": "変更確認",
            "差分状況": "差分確認",
            "最近コミット": "最近のコミット",
            "コミット最近": "最近のコミット",
            "ブランチ状況": "ブランチ確認",
            "こみっと準備": "コミット準備",
            "作業履歴": "作業ログ",
            "gitstauts": "git status",
            "gitstats": "git status",
            "gitstatus": "git status",
            "gitlog--online-5": "git log --oneline -5",
            "gitlog--oneline-5": "git log --oneline -5",
        }

    def normalize(self, user_input: str) -> NormalizedInput:
        original = user_input
        text = unicodedata.normalize("NFKC", user_input).strip()

        if not text:
            return NormalizedInput(original=original, text=text, corrected=False)

        # 「読み上げ: 本文」「作業記録: 本文」「コミットして: message」系は、
        # コマンド部分だけ補正して本文は変えない。
        for separator in [":", "："]:
            if separator in text:
                prefix, body = text.split(separator, 1)
                corrected_prefix = self._normalize_short(prefix)

                if corrected_prefix in self.prefix_commands:
                    normalized = f"{corrected_prefix}: {body.strip()}"
                    return NormalizedInput(
                        original=original,
                        text=normalized,
                        corrected=(normalized != original),
                    )

        normalized = self._normalize_short(text)

        return NormalizedInput(
            original=original,
            text=normalized,
            corrected=(normalized != original),
        )

    def _normalize_short(self, text: str) -> str:
        cleaned = " ".join(text.strip().split())
        key = self._key(cleaned)

        if key in self.aliases:
            return self.aliases[key]

        command_map = {
            self._key(command): command
            for command in self.known_commands + self.prefix_commands
        }

        if key in command_map:
            return command_map[key]

        # 長い文章を無理にコマンドへ変換しない
        if len(key) > 24:
            return cleaned

        matches = difflib.get_close_matches(
            key,
            list(command_map.keys()),
            n=1,
            cutoff=0.72,
        )

        if matches:
            return command_map[matches[0]]

        return cleaned

    def _key(self, text: str) -> str:
        return (
            unicodedata.normalize("NFKC", text)
            .replace(" ", "")
            .replace("　", "")
            .lower()
        )
