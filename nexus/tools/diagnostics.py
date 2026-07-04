"""
Project NEXUS
Tool Diagnostics v1

Diagnoses tool routing, tool order, and command collisions.
"""

from __future__ import annotations

from nexus.tools.base_tool import BaseTool


class ToolDiagnosticsTool(BaseTool):
    """Diagnoses which tools can handle an input."""

    name = "tool_diagnostics"
    description = "ツールの順序・衝突・横取りを診断します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "ツール順序"
            or text == "ツール一覧"
            or text == "ツール衝突チェック"
            or text.startswith("ツール診断:")
            or text.startswith("ツール診断：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text in {"ツール順序", "ツール一覧"}:
            return self._tool_order()

        if text == "ツール衝突チェック":
            return self._collision_check()

        if text.startswith(("ツール診断:", "ツール診断：")):
            query = self._extract_query(text)
            return self._diagnose_query(query)

        return "対応していないツール診断です。"

    def _manager(self):
        # 遅延import。ToolManagerの循環importを避ける。
        from nexus.tools.manager import ToolManager

        return ToolManager()

    def _extract_query(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _tool_order(self) -> str:
        manager = self._manager()

        lines = ["## Tool Order", ""]

        for index, tool in enumerate(manager.tools, start=1):
            lines.append(f"{index:02d}. {tool.__class__.__name__} / {getattr(tool, 'name', 'unknown')}")

        lines.append("")
        lines.append("Notes:")
        lines.append("- 上にあるツールほど先に判定されます。")
        lines.append("- CalculatorToolのような広いツールは、専用ツールより後ろが安全です。")

        return "\n".join(lines)

    def _diagnose_query(self, query: str) -> str:
        if not query:
            return "診断する入力がありません。例: ツール診断: 画像分析: tests/assets/sample_vision.png"

        manager = self._manager()
        hits = []

        for index, tool in enumerate(manager.tools, start=1):
            try:
                can = tool.can_handle(query)
            except Exception as error:
                hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown"), f"ERROR: {error}"))
                continue

            if can:
                hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown"), "MATCH"))

        lines = [
            "## Tool Diagnosis",
            "",
            f"Input: {query}",
            "",
        ]

        if not hits:
            lines.append("Result: どのツールも反応しませんでした。")
            return "\n".join(lines)

        lines.append("Matched tools:")
        for index, class_name, name, status in hits:
            lines.append(f"- {index:02d}. {class_name} / {name} [{status}]")

        first = hits[0]
        lines.append("")
        lines.append(f"Selected: {first[1]} / {first[2]}")

        if len(hits) >= 2:
            lines.append("")
            lines.append("Warning:")
            lines.append("- 複数ツールが同じ入力に反応しています。")
            lines.append("- 実際には一番上のツールだけが実行されます。")
            lines.append("- 意図しない横取りが起きる可能性があります。")

        return "\n".join(lines)

    def _collision_check(self) -> str:
        sample_inputs = [
            "画像ヘルプ",
            "画像安全確認: tests/assets/sample_vision.png",
            "画像分析: tests/assets/sample_vision.png",
            "計算: (2+5)*3",
            "単位変換: 40km/hをm/s",
            "安全検索: 東京造形",
            "調べて: 東京造形",
            "web要約: https://example.com",
            "url安全確認: https://example.com",
            "アプリ一覧",
            "git状態",
            "ls nexus/tools",
            "できること",
            "ダッシュボード",
            "テスト実行",
        ]

        manager = self._manager()

        lines = [
            "## Tool Collision Check",
            "",
        ]

        has_warning = False

        for query in sample_inputs:
            hits = []

            for index, tool in enumerate(manager.tools, start=1):
                try:
                    if tool.can_handle(query):
                        hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown")))
                except Exception as error:
                    hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown") + f" ERROR:{error}"))

            if len(hits) == 0:
                lines.append(f"MISS: {query}")
                has_warning = True
            elif len(hits) == 1:
                index, class_name, name = hits[0]
                lines.append(f"OK: {query} -> {index:02d}. {class_name}")
            else:
                has_warning = True
                first = hits[0]
                rest = ", ".join(f"{i:02d}.{c}" for i, c, n in hits[1:])
                lines.append(f"WARN: {query} -> selected {first[0]:02d}. {first[1]} / also {rest}")

        lines.append("")
        if has_warning:
            lines.append("Result: 注意が必要な項目があります。")
            lines.append("WARNは必ずしも失敗ではありませんが、横取りの原因になります。")
        else:
            lines.append("Result: 主要コマンドに大きな衝突は見つかりませんでした。")

        return "\n".join(lines)
