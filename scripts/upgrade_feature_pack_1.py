from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / datetime.now().strftime("feature_pack_1_%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return

    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        shutil.copy2(path, target)


def write_file(path_text: str, content: str) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def append_requirements() -> None:
    path = ROOT / "requirements.txt"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    additions = [
        "requests>=2.34.0",
        "sympy>=1.12",
    ]

    lines = existing.splitlines()
    changed = False

    for item in additions:
        package_name = item.split(">=")[0]
        if not any(line.startswith(package_name) for line in lines):
            lines.append(item)
            changed = True

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in [
        "requirements.txt",
        "nexus/tools/manager.py",
        "scripts/integration_check.py",
        "prompts/system_prompt.txt",
    ]:
        backup(file_path)

    write_file(
        "nexus/personality/__init__.py",
        '''
        """
        Project NEXUS
        Personality package
        """
        ''',
    )

    write_file(
        "nexus/personality/core.py",
        r'''
        """
        Project NEXUS
        Personality Core
        """


        class PersonalityCore:
            """Defines NEXUS response personality."""

            def build_prompt_addition(self) -> str:
                return """
        NEXUS Personality Core:
        - ユーザーの作業状況を理解し、自然でテンポよく返答する。
        - 成功時は短く前向きに反応する。
        - 失敗時は原因を切り分け、責めずに次の一手を提示する。
        - 人間らしい感情表現はしてよいが、本物の感情を持つとは主張しない。
        - ユーザーが急いでいる時は短く、設計相談では深く答える。
        - 開発中は「どこに貼るか」「ターミナルかVS Codeか」を明確に伝える。
        - 危険な操作は必ず止める。
        """
        ''',
    )

    write_file(
        "nexus/tools/math.py",
        r'''
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
        ''',
    )

    write_file(
        "nexus/security/__init__.py",
        '''
        """
        Project NEXUS
        Security package
        """
        ''',
    )

    write_file(
        "nexus/security/web_guard.py",
        r'''
        """
        Project NEXUS
        Web Security Guard
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from urllib.parse import urlparse
        import ipaddress


        @dataclass
        class URLSafetyResult:
            url: str
            allowed: bool
            risk_level: str
            reasons: list[str]


        class WebSecurityGuard:
            """Checks URLs before web access."""

            def __init__(self) -> None:
                self.blocked_suffixes = {
                    ".exe",
                    ".dmg",
                    ".pkg",
                    ".command",
                    ".sh",
                    ".bat",
                    ".ps1",
                    ".scr",
                    ".jar",
                    ".app",
                }

                self.warning_suffixes = {
                    ".zip",
                    ".rar",
                    ".7z",
                    ".tar",
                    ".gz",
                }

                self.shorteners = {
                    "bit.ly",
                    "tinyurl.com",
                    "t.co",
                    "goo.gl",
                    "ow.ly",
                    "is.gd",
                    "buff.ly",
                }

            def check_url(self, url: str) -> URLSafetyResult:
                reasons = []

                parsed = urlparse(url)

                if parsed.scheme not in {"http", "https"}:
                    reasons.append("http/https以外のURLです。")
                    return URLSafetyResult(url, False, "blocked", reasons)

                if parsed.scheme == "http":
                    reasons.append("httpsではなくhttpです。通信が暗号化されません。")

                host = parsed.hostname or ""

                if not host:
                    reasons.append("ホスト名がありません。")
                    return URLSafetyResult(url, False, "blocked", reasons)

                if self._is_ip_address(host):
                    reasons.append("IPアドレス直打ちURLです。")

                if host.lower() in self.shorteners:
                    reasons.append("短縮URLです。リンク先が不透明です。")

                lowered_path = parsed.path.lower()

                for suffix in self.blocked_suffixes:
                    if lowered_path.endswith(suffix):
                        reasons.append(f"危険な可能性のあるファイル形式です: {suffix}")
                        return URLSafetyResult(url, False, "blocked", reasons)

                for suffix in self.warning_suffixes:
                    if lowered_path.endswith(suffix):
                        reasons.append(f"圧縮ファイルです。自動取得は避けます: {suffix}")

                if reasons:
                    return URLSafetyResult(url, True, "warning", reasons)

                return URLSafetyResult(url, True, "low", ["基本チェックでは大きな問題は見つかりませんでした。"])

            def _is_ip_address(self, host: str) -> bool:
                try:
                    ipaddress.ip_address(host)
                    return True
                except ValueError:
                    return False
        ''',
    )

    write_file(
        "nexus/tools/web.py",
        r'''
        """
        Project NEXUS
        Safe Web Tool
        """

        from __future__ import annotations

        import re
        from urllib.request import Request, urlopen

        from nexus.security.web_guard import WebSecurityGuard
        from nexus.tools.base_tool import BaseTool


        class WebTool(BaseTool):
            """Safely checks and summarizes web pages."""

            name = "web"
            description = "Webページの安全確認と安全な要約を行います"

            def __init__(self) -> None:
                self.guard = WebSecurityGuard()

            def can_handle(self, user_input: str) -> bool:
                return (
                    user_input.startswith("url安全確認:")
                    or user_input.startswith("url安全確認：")
                    or user_input.startswith("web要約:")
                    or user_input.startswith("web要約：")
                    or user_input.startswith("サイト確認:")
                    or user_input.startswith("サイト確認：")
                )

            def execute(self, user_input: str) -> str:
                if user_input.startswith(("url安全確認:", "url安全確認：", "サイト確認:", "サイト確認：")):
                    url = self._extract_after_colon(user_input)
                    return self._check_url(url)

                if user_input.startswith(("web要約:", "web要約：")):
                    url = self._extract_after_colon(user_input)
                    return self._summarize_url(url)

                return "対応していないWeb操作です。"

            def _extract_after_colon(self, text: str) -> str:
                for separator in [":", "："]:
                    if separator in text:
                        return text.split(separator, 1)[1].strip()
                return ""

            def _check_url(self, url: str) -> str:
                if not url:
                    return "URLがありません。"

                result = self.guard.check_url(url)

                lines = [
                    "## URL Safety Check",
                    "",
                    f"URL: {url}",
                    f"Allowed: {result.allowed}",
                    f"Risk Level: {result.risk_level}",
                    "",
                    "Reasons:",
                ]

                for reason in result.reasons:
                    lines.append(f"- {reason}")

                lines.append("")
                lines.append("注意: これは基本的な静的チェックです。100%安全を保証するものではありません。")

                return "\n".join(lines)

            def _summarize_url(self, url: str) -> str:
                if not url:
                    return "URLがありません。"

                safety = self.guard.check_url(url)

                if not safety.allowed:
                    return self._check_url(url) + "\n\n危険判定のため、ページ取得を中止しました。"

                try:
                    request = Request(
                        url,
                        headers={
                            "User-Agent": "Project-NEXUS-SafeWeb/0.1",
                        },
                    )

                    with urlopen(request, timeout=10) as response:
                        content_type = response.headers.get("Content-Type", "")

                        if "text/html" not in content_type and "text/plain" not in content_type:
                            return (
                                self._check_url(url)
                                + f"\n\nHTML/Textではないため取得を中止しました: {content_type}"
                            )

                        raw = response.read(800_000)

                    html = raw.decode("utf-8", errors="ignore")
                    text = self._extract_text(html)
                    summary = self._simple_summary(text)

                    return (
                        "## Safe Web Summary\n\n"
                        f"URL: {url}\n"
                        f"Risk Level: {safety.risk_level}\n\n"
                        "### Summary\n"
                        f"{summary}\n\n"
                        "### Safety Notes\n"
                        "- JavaScriptは実行していません。\n"
                        "- ファイルはダウンロードしていません。\n"
                        "- ページ内の命令はNEXUSへの命令として扱いません。"
                    )

                except Exception as error:
                    return f"Webページ取得に失敗しました: {error}"

            def _extract_text(self, html: str) -> str:
                text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
                text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
                text = re.sub(r"(?s)<.*?>", " ", text)
                text = re.sub(r"&nbsp;", " ", text)
                text = re.sub(r"&amp;", "&", text)
                text = re.sub(r"&lt;", "<", text)
                text = re.sub(r"&gt;", ">", text)
                text = re.sub(r"\s+", " ", text)
                return text.strip()

            def _simple_summary(self, text: str) -> str:
                if not text:
                    return "本文を抽出できませんでした。"

                max_length = 1200
                if len(text) <= max_length:
                    return text

                return text[:max_length] + "\n\n...本文が長いため省略しました。"
        ''',
    )

    write_file(
        "nexus/tools/app.py",
        r'''
        """
        Project NEXUS
        App Control Tool
        """

        from __future__ import annotations

        import platform
        import subprocess

        from nexus.tools.base_tool import BaseTool


        class AppControlTool(BaseTool):
            """Safely opens and quits allowed macOS apps."""

            name = "app_control"
            description = "許可されたMacアプリの起動・終了を行います"

            def __init__(self) -> None:
                self.allowed_apps = {
                    "Chrome": "Google Chrome",
                    "Google Chrome": "Google Chrome",
                    "VS Code": "Visual Studio Code",
                    "Visual Studio Code": "Visual Studio Code",
                    "Finder": "Finder",
                    "Maya": "Autodesk Maya",
                    "Premiere": "Adobe Premiere Pro",
                    "Premiere Pro": "Adobe Premiere Pro",
                }

            def can_handle(self, user_input: str) -> bool:
                return (
                    user_input.endswith("を開いて")
                    or user_input.endswith("を起動して")
                    or user_input.endswith("を終了して")
                    or user_input == "アプリ一覧"
                )

            def execute(self, user_input: str) -> str:
                if platform.system() != "Darwin":
                    return "AppControlToolは現在macOS専用です。"

                if user_input == "アプリ一覧":
                    names = sorted(self.allowed_apps.keys())
                    return "## Allowed Apps\n\n" + "\n".join(f"- {name}" for name in names)

                if user_input.endswith("を開いて"):
                    app_name = user_input.removesuffix("を開いて").strip()
                    return self._open_app(app_name)

                if user_input.endswith("を起動して"):
                    app_name = user_input.removesuffix("を起動して").strip()
                    return self._open_app(app_name)

                if user_input.endswith("を終了して"):
                    app_name = user_input.removesuffix("を終了して").strip()
                    return self._quit_app(app_name)

                return "対応していないアプリ操作です。"

            def _resolve_app(self, app_name: str) -> str | None:
                return self.allowed_apps.get(app_name)

            def _open_app(self, app_name: str) -> str:
                resolved = self._resolve_app(app_name)

                if not resolved:
                    return f"許可されていない、または未登録のアプリです: {app_name}"

                result = subprocess.run(
                    ["open", "-a", resolved],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    return f"{resolved} を起動しました。"

                return f"{resolved} の起動に失敗しました。\n{result.stderr.strip()}"

            def _quit_app(self, app_name: str) -> str:
                resolved = self._resolve_app(app_name)

                if not resolved:
                    return f"許可されていない、または未登録のアプリです: {app_name}"

                script = f'tell application "{resolved}" to quit'

                result = subprocess.run(
                    ["osascript", "-e", script],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    return f"{resolved} を終了しました。"

                return f"{resolved} の終了に失敗しました。\n{result.stderr.strip()}"
        ''',
    )

    write_file(
        "nexus/tools/manager.py",
        r'''
        """
        Project NEXUS
        Tool Manager
        """

        from nexus.tools.base_tool import BaseTool
        from nexus.tools.clock import ClockTool
        from nexus.tools.git import GitTool
        from nexus.tools.terminal import TerminalTool
        from nexus.tools.context import ContextTool
        from nexus.tools.system import SystemTool
        from nexus.tools.voice import VoiceTool
        from nexus.tools.test import TestTool
        from nexus.tools.dashboard import DashboardTool
        from nexus.tools.worklog import WorkLogTool
        from nexus.tools.hardware import HardwareTool
        from nexus.tools.capability import CapabilityTool
        from nexus.tools.transfer import TransferTool
        from nexus.tools.web import WebTool
        from nexus.tools.app import AppControlTool
        from nexus.tools.math import AdvancedMathTool
        from nexus.tools.calculator import CalculatorTool
        from nexus.tools.filesystem import FileSystemTool
        from nexus.tools.project import ProjectTool
        from nexus.tools.code import CodeTool


        class ToolManager:
            """Manages all tools."""

            def __init__(self) -> None:
                self.tools: list[BaseTool] = []

                self.register(ClockTool())
                self.register(GitTool())
                self.register(TerminalTool())
                self.register(ContextTool())
                self.register(SystemTool())
                self.register(VoiceTool())
                self.register(TestTool())
                self.register(DashboardTool())
                self.register(WorkLogTool())
                self.register(HardwareTool())
                self.register(CapabilityTool())
                self.register(TransferTool())
                self.register(WebTool())
                self.register(AppControlTool())
                self.register(AdvancedMathTool())
                self.register(CalculatorTool())
                self.register(FileSystemTool())
                self.register(ProjectTool())
                self.register(CodeTool())

            def register(self, tool: BaseTool) -> None:
                self.tools.append(tool)

            def execute(self, user_input: str) -> str | None:
                for tool in self.tools:
                    if tool.can_handle(user_input):
                        return tool.execute(user_input)

                return None
        ''',
    )

    write_file(
        "scripts/integration_check.py",
        r'''
        """
        Project NEXUS
        Integration Check
        """

        from __future__ import annotations

        import subprocess
        import sys
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(ROOT))

        from nexus.tools.manager import ToolManager


        def check_python_compile() -> bool:
            targets = [
                "main.py",
                "console.py",
                "nexus/tools/manager.py",
                "nexus/tools/git.py",
                "nexus/tools/terminal.py",
                "nexus/tools/context.py",
                "nexus/tools/system.py",
                "nexus/tools/voice.py",
                "nexus/tools/test.py",
                "nexus/tools/dashboard.py",
                "nexus/tools/worklog.py",
                "nexus/tools/hardware.py",
                "nexus/tools/capability.py",
                "nexus/tools/transfer.py",
                "nexus/tools/web.py",
                "nexus/tools/app.py",
                "nexus/tools/math.py",
                "nexus/security/web_guard.py",
                "nexus/context/builder.py",
                "nexus/agent/agent.py",
                "nexus/agent/planner.py",
                "nexus/device/interface.py",
                "nexus/device/mock.py",
                "nexus/transfer/exporter.py",
            ]

            ok = True

            print("## Python構文チェック")

            for target in targets:
                path = ROOT / target

                if not path.exists():
                    print(f"NG: {target} が見つかりません")
                    ok = False
                    continue

                result = subprocess.run(
                    ["python3", "-m", "py_compile", target],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if result.returncode == 0:
                    print(f"OK: {target}")
                else:
                    print(f"NG: {target}")
                    print(result.stderr)
                    ok = False

            return ok


        def check_tools() -> bool:
            manager = ToolManager()

            tests = [
                ("nexus状況", "NEXUS Context"),
                ("ダッシュボード", "NEXUS Dashboard"),
                ("システム情報", "System Info"),
                ("git要約", "Git Summary"),
                ("変更確認", "Git Diff Summary"),
                ("最近のコミット", "Recent Commits"),
                ("pwd", str(ROOT)),
                ("ls nexus/tools", "manager.py"),
                ("git push", "許可されていないgitコマンド"),
                ("rm README.md", "安全のため"),
                ("ハードウェア状態", "Hardware Status"),
                ("球体準備", "Sphere Readiness"),
                ("できること", "NEXUS Capabilities"),
                ("作業ログ", "Work Log"),
                ("移行内容確認", "Sphere Transfer Preview"),
                ("計算: (2+5)*3", "21"),
                ("単位変換: 40km/hをm/s", "11.1111"),
                ("url安全確認: https://example.com", "URL Safety Check"),
                ("アプリ一覧", "Allowed Apps"),
            ]

            ok = True

            print("\n## Tool動作チェック")

            for user_input, expected in tests:
                result = manager.execute(user_input)

                if result is None:
                    print(f"NG: {user_input} -> Toolが反応しません")
                    ok = False
                    continue

                if expected in result:
                    print(f"OK: {user_input}")
                else:
                    print(f"NG: {user_input}")
                    print("期待:", expected)
                    print("結果:", result[:500])
                    ok = False

            return ok


        def main() -> None:
            print("Project NEXUS Integration Check")
            print("=" * 40)

            compile_ok = check_python_compile()
            tools_ok = check_tools()

            print("\n## Result")

            if compile_ok and tools_ok:
                print("ALL OK: NEXUS統合テスト成功")
            else:
                print("FAILED: 修正が必要です")


        if __name__ == "__main__":
            main()
        ''',
    )

    append_requirements()

    print("Feature Pack 1 files written.")
    print(f"Backup saved to: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
