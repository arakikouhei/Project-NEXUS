"""
Project NEXUS
Advanced Math Tool
"""

from __future__ import annotations

import ast
import math
import operator
import re

from nexus.tools.base_tool import BaseTool


class AdvancedMathTool(BaseTool):
    """Handles safer advanced calculations and high-school math basics."""

    name = "advanced_math"
    description = "高校数学レベルの計算を補助します"

    def __init__(self) -> None:
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        self.functions = {
            "sqrt": math.sqrt,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "ln": math.log,
            "abs": abs,
            "round": round,
            "floor": math.floor,
            "ceil": math.ceil,
        }

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "計算:",
            "計算：",
            "方程式:",
            "方程式：",
            "因数分解:",
            "因数分解：",
            "展開:",
            "展開：",
            "微分:",
            "微分：",
            "積分:",
            "積分：",
            "平方完成:",
            "平方完成：",
            "単位変換:",
            "単位変換：",
            "高校数学",
        }

        if any(keyword in user_input for keyword in keywords):
            return True

        simple_math_pattern = r"^[0-9\.\+\-\*/\(\)\s\^%]+$"
        return bool(re.match(simple_math_pattern, user_input.strip()))

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith(("計算:", "計算：")):
            expression = self._extract_after_colon(text)
            return self._calculate(expression)

        if text.startswith(("単位変換:", "単位変換：")):
            expression = self._extract_after_colon(text)
            return self._convert_units(expression)

        if text.startswith(("方程式:", "方程式：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("solve", expression)

        if text.startswith(("因数分解:", "因数分解：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("factor", expression)

        if text.startswith(("展開:", "展開：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("expand", expression)

        if text.startswith(("微分:", "微分：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("diff", expression)

        if text.startswith(("積分:", "積分：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("integrate", expression)

        if text.startswith(("平方完成:", "平方完成：")):
            expression = self._extract_after_colon(text)
            return self._sympy_task("complete_square", expression)

        if "高校数学" in text:
            return self._help()

        return self._calculate(text)

    def _extract_after_colon(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return text.strip()

    def _calculate(self, expression: str) -> str:
        if not expression:
            return "計算する式がありません。"

        expression = expression.replace("^", "**")

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._eval_node(tree.body)
            return f"## Calculation Result\n\n{expression} = {result}"
        except Exception as error:
            return f"計算できませんでした: {error}"

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("数値以外は使えません。")

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)
            if operator_type not in self.operators:
                raise ValueError("許可されていない演算子です。")
            return self.operators[operator_type](
                self._eval_node(node.left),
                self._eval_node(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)
            if operator_type not in self.operators:
                raise ValueError("許可されていない単項演算子です。")
            return self.operators[operator_type](self._eval_node(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("許可されていない関数です。")

            function_name = node.func.id

            if function_name not in self.functions:
                raise ValueError(f"使えない関数です: {function_name}")

            args = [self._eval_node(arg) for arg in node.args]
            return self.functions[function_name](*args)

        raise ValueError("この式は安全上計算できません。")

    def _sympy_task(self, task: str, expression: str) -> str:
        try:
            import sympy as sp
        except Exception:
            return (
                "Sympyが未インストールです。\n\n"
                "Macターミナルで `pip3 install sympy` を実行すると、"
                "方程式・因数分解・微分積分が使えるようになります。"
            )

        if not expression:
            return "式がありません。"

        try:
            x = sp.symbols("x")
            expr_text = expression.replace("^", "**")

            if task == "solve":
                if "=" in expr_text:
                    left, right = expr_text.split("=", 1)
                    equation = sp.Eq(sp.sympify(left), sp.sympify(right))
                    result = sp.solve(equation, x)
                else:
                    result = sp.solve(sp.sympify(expr_text), x)
                return f"## Equation Result\n\n解: {result}"

            expr = sp.sympify(expr_text)

            if task == "factor":
                return f"## Factor Result\n\n{sp.factor(expr)}"

            if task == "expand":
                return f"## Expand Result\n\n{sp.expand(expr)}"

            if task == "diff":
                return f"## Derivative Result\n\n{sp.diff(expr, x)}"

            if task == "integrate":
                return f"## Integral Result\n\n{sp.integrate(expr, x)} + C"

            if task == "complete_square":
                a = sp.Poly(expr, x)
                if a.degree() != 2:
                    return "平方完成は今のところ二次式のみ対応です。"
                result = sp.complete_square(expr, x)
                return f"## Complete Square\n\n{result}"

            return "対応していない数学処理です。"

        except Exception as error:
            return f"数学処理に失敗しました: {error}"

    def _convert_units(self, expression: str) -> str:
        text = expression.replace(" ", "")

        kmh_match = re.match(r"([0-9.]+)km/h?をm/s|([0-9.]+)km毎時を秒速", text)
        if kmh_match:
            value_text = kmh_match.group(1) or kmh_match.group(2)
            value = float(value_text)
            result = value * 1000 / 3600
            return f"## Unit Conversion\n\n{value} km/h = {result:.4f} m/s"

        ms_match = re.match(r"([0-9.]+)m/sをkm/h|([0-9.]+)秒速を時速", text)
        if ms_match:
            value_text = ms_match.group(1) or ms_match.group(2)
            value = float(value_text)
            result = value * 3600 / 1000
            return f"## Unit Conversion\n\n{value} m/s = {result:.4f} km/h"

        return (
            "対応している単位変換例:\n"
            "- 単位変換: 40km/hをm/s\n"
            "- 単位変換: 10m/sをkm/h"
        )

    def _help(self) -> str:
        return (
            "## Advanced Math Help\n\n"
            "使える例:\n"
            "- 計算: (2+5)*3\n"
            "- 計算: sqrt(144)\n"
            "- 計算: sin(30)\n"
            "- 方程式: x^2 - 5*x + 6 = 0\n"
            "- 因数分解: x^2 - 5*x + 6\n"
            "- 展開: (x+2)*(x+3)\n"
            "- 微分: x^3 + 2*x\n"
            "- 積分: x^2\n"
            "- 単位変換: 40km/hをm/s\n"
        )
