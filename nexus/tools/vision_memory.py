"""
Project NEXUS
Vision Memory Tool v1
"""

from __future__ import annotations

from pathlib import Path

from nexus.memory.vision_log import VisionLogStore
from nexus.tools.base_tool import BaseTool


class VisionMemoryTool(BaseTool):
    """Shows previous vision analysis logs."""

    name = "vision_memory"
    description = "画像分析ログを確認します"

    def __init__(self) -> None:
        self.store = VisionLogStore()

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "画像分析ログ"
            or text == "最近分析した画像"
            or text == "画像ログヘルプ"
            or text.startswith("前回画像分析:")
            or text.startswith("前回画像分析：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "画像ログヘルプ":
            return self._help()

        if text in {"画像分析ログ", "最近分析した画像"}:
            return self._recent()

        if text.startswith(("前回画像分析:", "前回画像分析：")):
            path_text = self._extract_path(text)
            return self._previous(path_text)

        return "対応していない画像ログ操作です。"

    def _extract_path(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip().strip('"').strip("'")
        return ""

    def _recent(self) -> str:
        records = self.store.recent(limit=10)

        if not records:
            return (
                "## Vision Log\n\n"
                "まだ画像分析ログはありません。\n\n"
                "例:\n"
                "- 画像分析: tests/assets/sample_vision.png\n"
                "- 画像意味分析: tests/assets/sample_vision.png"
            )

        lines = ["## Recent Vision Logs", ""]

        for index, item in enumerate(records, start=1):
            path = item.get("image_path", "")
            name = Path(path).name if path else "unknown"
            timestamp = item.get("timestamp", "unknown")
            analysis_type = item.get("analysis_type", "unknown")
            scores = item.get("scores", {})

            top_score = self._top_score(scores)

            lines.append(f"### {index}. {name}")
            lines.append(f"- Time: {timestamp}")
            lines.append(f"- Type: {analysis_type}")
            lines.append(f"- Path: {path}")

            if top_score:
                lines.append(f"- Top: {top_score}")

            summary = item.get("summary", [])
            for s in summary[:2]:
                lines.append(s)

            lines.append("")

        return "\n".join(lines).rstrip()

    def _previous(self, path_text: str) -> str:
        if not path_text:
            return "画像パスがありません。例: 前回画像分析: tests/assets/sample_vision.png"

        records = self.store.find_by_path(path_text, limit=5)

        if not records:
            return (
                "## Previous Vision Analysis\n\n"
                f"対象: {path_text}\n\n"
                "この画像の過去ログは見つかりませんでした。"
            )

        lines = [
            "## Previous Vision Analysis",
            "",
            f"対象: {path_text}",
            "",
        ]

        for index, item in enumerate(records, start=1):
            lines.append(f"### {index}. {item.get('timestamp', 'unknown')}")
            lines.append(f"- Type: {item.get('analysis_type', 'unknown')}")
            lines.append(f"- Path: {item.get('image_path', '')}")

            scores = item.get("scores", {})
            if scores:
                lines.append("- Scores:")
                for label, score in scores.items():
                    lines.append(f"  - {label}: {score}/100")

            summary = item.get("summary", [])
            if summary:
                lines.append("- Summary:")
                for s in summary[:4]:
                    lines.append(f"  {s}")

            lines.append("")

        return "\n".join(lines).rstrip()

    def _top_score(self, scores: dict) -> str | None:
        if not scores:
            return None

        label, score = max(scores.items(), key=lambda item: item[1])
        return f"{label} {score}/100"

    def _help(self) -> str:
        return (
            "## Vision Log Help\n\n"
            "使えるコマンド:\n"
            "- 画像分析ログ\n"
            "- 最近分析した画像\n"
            "- 前回画像分析: /path/to/image.png\n\n"
            "ログされるもの:\n"
            "- 分析日時\n"
            "- 画像パス\n"
            "- 分析タイプ\n"
            "- 意味スコア\n"
            "- 読み取り要約\n\n"
            "ログ保存先:\n"
            "- data/vision_log.json"
        )
