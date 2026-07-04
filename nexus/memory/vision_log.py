"""
Project NEXUS
Vision Log Store v1
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import re


class VisionLogStore:
    """Stores local vision analysis history."""

    def __init__(self, path: str = "data/vision_log.json") -> None:
        self.path = Path(path)

    def record(self, image_path: str, analysis_type: str, result: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        records = self._load()

        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "image_path": str(Path(image_path).expanduser()),
            "analysis_type": analysis_type,
            "summary": self._extract_summary(result),
            "scores": self._extract_scores(result),
        }

        records.append(entry)

        # 増えすぎ防止。直近200件だけ保持。
        records = records[-200:]

        self.path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def recent(self, limit: int = 10) -> list[dict]:
        records = self._load()
        return list(reversed(records[-limit:]))

    def find_by_path(self, image_path: str, limit: int = 5) -> list[dict]:
        target = str(Path(image_path).expanduser())
        records = self._load()

        matched = [
            item for item in records
            if item.get("image_path") == target
            or Path(item.get("image_path", "")).name == Path(target).name
        ]

        return list(reversed(matched[-limit:]))

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

    def _extract_summary(self, result: str) -> list[str]:
        lines = []

        capture = False
        for line in result.splitlines():
            stripped = line.strip()

            if stripped in {"### Reading", "### Visual Hints"}:
                capture = True
                continue

            if capture and stripped.startswith("### "):
                break

            if capture and stripped.startswith("- "):
                lines.append(stripped)

        return lines[:8]

    def _extract_scores(self, result: str) -> dict[str, int]:
        scores: dict[str, int] = {}

        for line in result.splitlines():
            match = re.match(r"-\s*(.+?):\s*(\d+)\s*/100", line.strip())

            if match:
                scores[match.group(1)] = int(match.group(2))

        return scores
