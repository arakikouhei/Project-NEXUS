"""
Project NEXUS
Code Summary
"""


class CodeSummary:
    """Creates text summaries from analysis results."""

    def create(self, analysis: dict) -> str:
        lines = []

        lines.append("コード解析結果です。")
        lines.append("")

        lines.append(f"クラス数: {analysis['class_count']}")
        lines.append(f"関数数: {analysis['function_count']}")
        lines.append(f"import数: {analysis['import_count']}")
        lines.append("")

        if analysis["classes"]:
            lines.append("クラス:")
            for name in analysis["classes"]:
                lines.append(f"- {name}")
            lines.append("")

        if analysis["functions"]:
            lines.append("関数:")
            for name in analysis["functions"]:
                lines.append(f"- {name}")

        return "\n".join(lines)