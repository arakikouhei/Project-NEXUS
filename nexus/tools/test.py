"""
Project NEXUS
Test Tool
"""

import subprocess
from pathlib import Path

from nexus.tools.base_tool import BaseTool


class TestTool(BaseTool):
    """Runs NEXUS integration tests."""

    name = "test"
    description = "NEXUSの統合テストを実行します"

    def __init__(self) -> None:
        self.root = Path.cwd()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "テスト実行",
            "統合テスト",
            "nexusテスト",
            "NEXUSテスト",
            "self test",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        script_path = self.root / "scripts" / "integration_check.py"

        if not script_path.exists():
            return "scripts/integration_check.py が見つかりません。"

        try:
            result = subprocess.run(
                ["python3", str(script_path)],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode == 0 and output:
                return "## NEXUS Test Result\n\n" + self._limit_output(output)

            if error:
                return "## NEXUS Test Error\n\n" + self._limit_output(error)

            return "テストは実行されましたが、出力がありません。"

        except subprocess.TimeoutExpired:
            return "統合テストがタイムアウトしました。"

        except Exception as error:
            return f"テスト実行中にエラーが発生しました: {error}"

    def _limit_output(self, text: str) -> str:
        max_length = 6000

        if len(text) <= max_length:
            return text

        return text[:max_length] + "\n\n...出力が長いため省略しました。"
