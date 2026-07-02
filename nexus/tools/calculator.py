"""
Project NEXUS
Calculator Tool
"""

from nexus.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """Simple calculator."""

    name = "calculator"
    description = "数式を計算します"

    def can_handle(self, user_input: str) -> bool:
        expression = user_input.replace(" ", "")
        return any(op in expression for op in ["+", "-", "*", "/", "(", ")"])

    def execute(self, user_input: str) -> str:
        try:
            result = eval(user_input, {"__builtins__": {}})
            return str(result)
        except Exception:
            return "計算できませんでした。"