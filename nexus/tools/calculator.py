"""
Project NEXUS
Calculator Tool

Strict v1:
- Does not capture image commands
- Does not capture URLs
- Does not capture terminal commands
- Handles only explicit calculation-like inputs
"""

from __future__ import annotations

import ast
import operator
import re

from nexus.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    """Performs safe basic calculations."""

    name = "calculator"
    description = "安全な基本計算を行います"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        if not text:
            return False

        # 明示コマンドだけは受ける
        if text.startswith(("計算:", "計算：", "calc:", "calc：")):
            return True

        # 他ツール用の入力は絶対に拾わない
        blocked_prefixes = (
            "画像",
            "安全検索:",
            "安全検索：",
            "公式確認:",
            "公式確認：",
            "公式検索:",
            "公式検索：",
            "調べて:",
            "調べて：",
            "用語確認:",
            "用語確認：",
            "web要約:",
            "web要約：",
            "url安全確認:",
            "url安全確認：",
            "アプリ",
            "ツール",
            "git",
            "コミット",
            "読み上げ",
            "作業記録",
        )

        if text.startswith(blocked_prefixes):
            return False

        # URLやファイルパスっぽいものは拾わない
        lowered = text.lower()
        if "http://" in lowered or "https://" in lowered:
            return False

        if "/" in text or "\\" in text:
            return False

        # ターミナル系を拾わない
        terminal_like = (
            "ls",
            "pwd",
            "cd ",
            "python",
            "pip",
            "mkdir",
            "cat ",
            "cp ",
            "mv ",
            "rm ",
        )

        if lowered == "ls" or lowered.startswith(terminal_like):
            return False

        # 日本語文章っぽいものは拾わない
        if re.search(r"[ぁ-んァ-ン一-龥]", text):
            return False

        # 数字と演算子だけに近い短い式なら拾う
        if not re.search(r"\d", text):
            return False

        allowed = set("0123456789+-*/().% **")
        return all(ch in allowed for ch in text)

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        expression = text

        for prefix in ["計算:", "計算：", "calc:", "calc："]:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()
                break

        try:
            result = self._safe_eval(expression)
            return (
                "## Calculation Result\n\n"
                f"{expression} = {result}"
            )
        except Exception:
            return "計算できませんでした。"

    def _safe_eval(self, expression: str):
        expression = expression.replace("％", "%")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")

        node = ast.parse(expression, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node):
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        unary_operators = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)

            if op_type not in operators:
                raise ValueError("Unsupported operator")

            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            return operators[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)

            if op_type not in unary_operators:
                raise ValueError("Unsupported unary operator")

            return unary_operators[op_type](self._eval_node(node.operand))

        raise ValueError("Unsupported expression")
