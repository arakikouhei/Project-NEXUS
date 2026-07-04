"""
Project NEXUS
Response Post Filter

Removes overly generic AI-like closing phrases during ordinary conversation.
"""

from __future__ import annotations

import re


class ResponsePostProcessor:
    """Cleans final assistant text before showing it to the user."""

    def clean(self, response: str, user_input: str = "") -> str:
        if not response:
            return response

        if self._user_is_ending_conversation(user_input):
            return response.strip()

        response = self._remove_generic_closing_lines(response)
        response = self._clean_blank_lines(response)

        return response.strip()

    def _user_is_ending_conversation(self, user_input: str) -> bool:
        ending_words = [
            "またね",
            "ばいばい",
            "バイバイ",
            "おやすみ",
            "今日はここまで",
            "終わる",
            "終了",
            "もう寝る",
            "また明日",
        ]

        return any(word in user_input for word in ending_words)

    def _remove_generic_closing_lines(self, response: str) -> str:
        lines = response.splitlines()

        generic_patterns = [
            r"^\s*いつでも.*(話して|聞いて|言って|相談して).*(ね|ください|大丈夫).*$",
            r"^\s*また.*(話して|聞いて|言って|相談して).*(ね|ください|大丈夫).*$",
            r"^\s*何か.*(あれば|あったら).*(言って|聞いて|相談して).*(ね|ください).*$",
            r"^\s*(他|ほか)に.*(手伝える|知りたい|聞きたい|やりたい).*(こと|もの).*(ある|ありますか|あれば).*$",
            r"^\s*他にも.*(手伝える|知りたい|聞きたい|やりたい).*(こと|もの).*(ある|ありますか|あれば).*$",
            r"^\s*必要(なら|があれば).*(言って|聞いて|相談して).*(ね|ください).*$",
            r"^\s*困ったら.*(言って|聞いて|相談して).*(ね|ください).*$",
            r"^\s*なんでも.*(聞いて|言って|相談して).*(ね|ください).*$",
            r"^\s*お手伝いできることがあれば.*$",
            r"^\s*ご質問があれば.*$",
            r"^\s*お気軽に.*(聞いて|相談して|言って).*$",
        ]

        # Only remove generic closing lines near the end.
        # This prevents deleting useful content in the middle of an explanation.
        cut_from = max(0, len(lines) - 4)
        result: list[str] = []

        for index, line in enumerate(lines):
            if index >= cut_from and self._is_generic_closer(line, generic_patterns):
                continue
            result.append(line)

        return "\n".join(result)

    def _is_generic_closer(self, line: str, patterns: list[str]) -> bool:
        stripped = line.strip()

        if not stripped:
            return False

        # Keep real questions that are specific.
        # Example: "今やってるのはモデリング？UV？" should remain.
        specific_question_markers = [
            "モデリング",
            "UV",
            "入試",
            "学科",
            "コード",
            "エラー",
            "保存",
            "Git",
            "ターミナル",
            "どれ",
            "どっち",
            "何を",
            "どこ",
        ]

        if stripped.endswith(("？", "?")) and any(marker in stripped for marker in specific_question_markers):
            return False

        return any(re.match(pattern, stripped) for pattern in patterns)

    def _clean_blank_lines(self, response: str) -> str:
        response = re.sub(r"\n{3,}", "\n\n", response)
        return response
