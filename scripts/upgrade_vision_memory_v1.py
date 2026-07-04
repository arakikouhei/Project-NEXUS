from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "vision_memory_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def write_vision_log_store() -> None:
    write(
        "nexus/memory/vision_log.py",
        r'''
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
        ''',
    )


def write_vision_memory_tool() -> None:
    write(
        "nexus/tools/vision_memory.py",
        r'''
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
        ''',
    )


def patch_vision_tool_logging() -> None:
    path = ROOT / "nexus/tools/vision.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.memory.vision_log import VisionLogStore" not in text:
        text = text.replace(
            "from nexus.tools.base_tool import BaseTool\n",
            "from nexus.tools.base_tool import BaseTool\n"
            "from nexus.memory.vision_log import VisionLogStore\n",
            1,
        )

    if "self.vision_log = VisionLogStore()" not in text:
        text = text.replace(
            "        self.max_size_mb = 25\n",
            "        self.max_size_mb = 25\n"
            "        self.vision_log = VisionLogStore()\n",
            1,
        )

    if "analysis_type=\"basic\"" not in text:
        text = text.replace(
            '        if text.startswith(("画像分析:", "画像分析：")):\n'
            '            path = self._extract_path(text)\n'
            '            return self._analyze(path)\n',
            '        if text.startswith(("画像分析:", "画像分析：")):\n'
            '            path = self._extract_path(text)\n'
            '            result = self._analyze(path)\n'
            '            self._record_analysis(path, "basic", result)\n'
            '            return result\n',
            1,
        )

    if "analysis_type=\"semantic\"" not in text:
        text = text.replace(
            '        if text.startswith(("画像意味分析:", "画像意味分析：")):\n'
            '            path = self._extract_path(text)\n'
            '            return self._semantic_analyze(path)\n',
            '        if text.startswith(("画像意味分析:", "画像意味分析：")):\n'
            '            path = self._extract_path(text)\n'
            '            result = self._semantic_analyze(path)\n'
            '            self._record_analysis(path, "semantic", result)\n'
            '            return result\n',
            1,
        )

    if "def _record_analysis(" not in text:
        marker = "    def _extract_path(self, text: str) -> str:\n"
        method = '''    def _record_analysis(self, path_text: str, analysis_type: str, result: str) -> None:
        if "分析できません" in result or "失敗しました" in result:
            return

        try:
            self.vision_log.record(
                image_path=path_text,
                analysis_type=analysis_type,
                result=result,
            )
        except Exception:
            # ログ保存失敗で画像分析自体を止めない
            pass

'''
        if marker not in text:
            raise SystemExit("vision.py: _extract_path が見つかりません。")

        text = text.replace(marker, method + marker, 1)

    path.write_text(text, encoding="utf-8")


def patch_manager() -> None:
    path = ROOT / "nexus/tools/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.tools.vision_memory import VisionMemoryTool" not in text:
        text = text.replace(
            "from nexus.tools.vision import VisionTool\n",
            "from nexus.tools.vision import VisionTool\n"
            "from nexus.tools.vision_memory import VisionMemoryTool\n",
            1,
        )

    if "self.register(VisionMemoryTool())" not in text:
        text = text.replace(
            "        self.register(VisionTool())\n",
            "        self.register(VisionTool())\n"
            "        self.register(VisionMemoryTool())\n",
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"画像分析ログ"' not in text:
        text = text.replace(
            '                    "画像意味テスト",\n',
            '                    "画像意味テスト",\n'
            '                    "画像分析ログ",\n'
            '                    "前回画像分析: tests/assets/sample_vision.png",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/VISION_MEMORY_V1.md",
        """
        # Vision Memory v1

        Vision Memory stores local image analysis history.

        ## Commands

        - 画像分析ログ
        - 最近分析した画像
        - 前回画像分析: /path/to/image.png
        - 画像ログヘルプ

        ## Saved Data

        Stored in:

        - data/vision_log.json

        ## Notes

        This stores analysis summaries and semantic scores.
        It does not store image binary data.
        """,
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/tools/vision.py",
        "nexus/tools/manager.py",
        "nexus/tools/diagnostics.py",
        "nexus/tools/vision_memory.py",
        "nexus/memory/vision_log.py",
    ]:
        backup(target)

    write_vision_log_store()
    write_vision_memory_tool()
    patch_vision_tool_logging()
    patch_manager()
    patch_diagnostics()
    write_docs()

    print("Vision Memory v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
