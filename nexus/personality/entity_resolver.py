"""
Project NEXUS
Entity Resolver

This layer helps NEXUS treat abbreviations and compound terms as entities,
instead of splitting them into unrelated words.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re


@dataclass
class EntityMatch:
    alias: str
    canonical: str
    category: str
    confidence: str
    note: str


class EntityResolver:
    """Resolves aliases and likely proper nouns."""

    def __init__(self, alias_path: str = "data/entity_aliases.json") -> None:
        self.alias_path = Path(alias_path)
        self.aliases = self._load_aliases()

    def _load_aliases(self) -> dict[str, dict[str, str]]:
        if not self.alias_path.exists():
            return {}

        try:
            data = json.loads(self.alias_path.read_text(encoding="utf-8"))
            return data.get("aliases", {})
        except Exception:
            return {}

    def analyze(self, text: str) -> str:
        matches = self.find_matches(text)
        proper_candidate = self.find_possible_proper_noun(text)

        lines = []

        if matches:
            lines.append("Detected entity aliases:")
            for match in matches:
                lines.append(
                    f"- '{match.alias}' likely means '{match.canonical}' "
                    f"(category: {match.category}, confidence: {match.confidence}). "
                    f"Note: {match.note}"
                )

            lines.append(
                "Entity rule: Treat detected aliases as whole entities. "
                "Do not split them into separate common words."
            )

        elif proper_candidate:
            lines.append(
                f"Possible proper noun or abbreviation detected: '{proper_candidate}'. "
                "Treat it as a single phrase first. Do not split it into unrelated words. "
                "If meaning is unclear, ask a light clarification or say that a search would help."
            )

        else:
            lines.append(
                "No special entity alias detected. Still avoid over-splitting unfamiliar compound terms."
            )

        lines.append(
            "If a user asks about an institution, school, software, title, product, or abbreviation, "
            "first consider that the whole phrase may be the name of something."
        )

        return "\n".join(lines)

    def find_matches(self, text: str) -> list[EntityMatch]:
        results: list[EntityMatch] = []

        # Longest aliases first, so 東京造形大学-like aliases win over smaller fragments.
        for alias in sorted(self.aliases.keys(), key=len, reverse=True):
            if alias and alias in text:
                data = self.aliases[alias]
                results.append(
                    EntityMatch(
                        alias=alias,
                        canonical=data.get("canonical", alias),
                        category=data.get("category", "unknown"),
                        confidence=data.get("confidence", "medium"),
                        note=data.get("note", ""),
                    )
                )

        # Deduplicate canonical names.
        seen = set()
        deduped = []
        for item in results:
            key = (item.alias, item.canonical)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)

        return deduped[:5]

    def find_possible_proper_noun(self, text: str) -> str | None:
        patterns = [
            r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})について",
            r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})って(?:いうの)?(?:を)?",
            r"最近(?:は)?([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})(?:っていうの)?を",
            r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})知ってる",
        ]

        stopwords = {
            "これ",
            "それ",
            "あれ",
            "どう",
            "なに",
            "何",
            "少し",
            "最近",
            "ゲームの話もいいけど最近は",
        }

        for pattern in patterns:
            match = re.search(pattern, text)
            if not match:
                continue

            candidate = match.group(1).strip(" 、。！？?")

            if candidate in stopwords:
                continue

            if len(candidate) >= 2:
                return candidate

        return None
