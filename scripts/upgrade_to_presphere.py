from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / datetime.now().strftime("presphere_%Y%m%d_%H%M%S")


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


def append_gitignore() -> None:
    path = ROOT / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    additions = [
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        "logs/",
        "*.log",
        "backups/",
        "data/worklog.json",
    ]

    lines = existing.splitlines()
    changed = False

    for item in additions:
        if item not in lines:
            lines.append(item)
            changed = True

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_readme() -> None:
    path = ROOT / "README.md"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    marker = "## Pre-Sphere Core"

    if marker in text:
        return

    addition = """

---

## Pre-Sphere Core

Project NEXUS has reached the **Pre-Sphere Core** stage.

This means the software foundation is ready for future hardware integration.

Current Pre-Sphere capabilities include:

- Local AI assistant foundation
- Memory and context foundation
- Safe tool execution
- Git and terminal support
- Self-test system
- Voice output
- Work log support
- System status dashboard
- Hardware mock interface
- Sphere readiness check

Actual physical hardware control is intentionally not enabled yet.
Hardware integration will be added after additional safety layers are implemented.
"""

    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in [
        ".gitignore",
        "README.md",
        "nexus/context/builder.py",
        "nexus/tools/manager.py",
        "scripts/integration_check.py",
    ]:
        backup(file_path)

    write_file(
        "nexus/context/builder.py",
        r'''
        """
        Project NEXUS
        Context Builder
        """

        from __future__ import annotations

        import json
        import subprocess
        from pathlib import Path


        class ContextBuilder:
            """Builds the current execution context."""

            def __init__(self) -> None:
                self.root = Path.cwd()
                self.worklog_path = self.root / "data" / "worklog.json"

            def build(self) -> dict:
                return {
                    "project": "Project NEXUS",
                    "version": "v0.95.0-pre-sphere",
                    "stage": "Pre-Sphere Core",
                    "working_directory": str(self.root),
                    "git_branch": self._git_branch(),
                    "git_status": self._git_status(),
                    "available_tools": self._available_tools(),
                    "recent_worklog": self._recent_worklog(),
                    "recent_terminal_logs": self._recent_terminal_logs(),
                    "sphere_ready": False,
                    "hardware_mode": "mock",
                }

            def _git_branch(self) -> str:
                try:
                    result = subprocess.run(
                        ["git", "branch", "--show-current"],
                        cwd=self.root,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                    return result.stdout.strip() or "unknown"
                except Exception:
                    return "unknown"

            def _git_status(self) -> str:
                try:
                    result = subprocess.run(
                        ["git", "status", "--porcelain"],
                        cwd=self.root,
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )

                    if result.stdout.strip():
                        return "dirty"

                    return "clean"

                except Exception:
                    return "unknown"

            def _available_tools(self) -> list[str]:
                return [
                    "ClockTool",
                    "GitTool",
                    "TerminalTool",
                    "ContextTool",
                    "SystemTool",
                    "VoiceTool",
                    "TestTool",
                    "DashboardTool",
                    "WorkLogTool",
                    "HardwareTool",
                    "CapabilityTool",
                    "CalculatorTool",
                    "FileSystemTool",
                    "ProjectTool",
                    "CodeTool",
                ]

            def _recent_worklog(self) -> list[str]:
                if not self.worklog_path.exists():
                    return []

                try:
                    data = json.loads(self.worklog_path.read_text(encoding="utf-8"))
                    entries = data.get("entries", [])
                    recent = entries[-5:]
                    return [
                        f"{entry.get('time', 'unknown')} - {entry.get('text', '')}"
                        for entry in recent
                    ]
                except Exception:
                    return []

            def _recent_terminal_logs(self) -> list[str]:
                log_path = self.root / "logs" / "terminal.log"

                if not log_path.exists():
                    return []

                try:
                    lines = log_path.read_text(encoding="utf-8").splitlines()
                    return lines[-5:]
                except Exception:
                    return []
        ''',
    )

    write_file(
        "nexus/tools/capability.py",
        r'''
        """
        Project NEXUS
        Capability Tool
        """

        from nexus.tools.base_tool import BaseTool


        class CapabilityTool(BaseTool):
            """Shows what NEXUS can do."""

            name = "capability"
            description = "NEXUSのできることを表示します"

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "できること",
                    "機能一覧",
                    "ヘルプ",
                    "help",
                    "何ができる",
                    "使い方",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                return (
                    "## NEXUS Capabilities\n\n"
                    "現在のNEXUSは Pre-Sphere Core 段階です。\n\n"
                    "### 状態確認\n"
                    "- nexus状況\n"
                    "- ダッシュボード\n"
                    "- システム情報\n"
                    "- ハードウェア状態\n"
                    "- 球体準備\n\n"
                    "### Git\n"
                    "- git要約\n"
                    "- git状態\n"
                    "- 変更確認\n"
                    "- 最近のコミット\n"
                    "- コミット準備\n"
                    "- コミットして: メッセージ\n\n"
                    "### Terminal\n"
                    "- pwd\n"
                    "- ls\n"
                    "- ls nexus/tools\n"
                    "- git log --oneline -5\n\n"
                    "### Self Test\n"
                    "- テスト実行\n\n"
                    "### Work Log\n"
                    "- 作業記録: 内容\n"
                    "- 作業ログ\n\n"
                    "### Voice\n"
                    "- 読み上げ: テキスト\n\n"
                    "### Project / Code\n"
                    "- AIManagerはどこ？\n"
                    "- nexus/tools/git.pyを解析して\n"
                )
        ''',
    )

    write_file(
        "nexus/tools/worklog.py",
        r'''
        """
        Project NEXUS
        Work Log Tool
        """

        from __future__ import annotations

        from datetime import datetime
        import json
        from pathlib import Path

        from nexus.tools.base_tool import BaseTool


        class WorkLogTool(BaseTool):
            """Records and shows work logs."""

            name = "worklog"
            description = "作業ログを記録・表示します"

            def __init__(self) -> None:
                self.root = Path.cwd()
                self.path = self.root / "data" / "worklog.json"

            def can_handle(self, user_input: str) -> bool:
                return (
                    user_input.startswith("作業記録:")
                    or user_input.startswith("作業記録：")
                    or user_input in {"作業ログ", "最近の作業", "作業履歴"}
                )

            def execute(self, user_input: str) -> str:
                if user_input.startswith("作業記録:") or user_input.startswith("作業記録："):
                    text = self._extract_text(user_input)

                    if not text:
                        return "記録する内容がありません。"

                    if len(text) > 300:
                        return "作業記録は300文字以内にしてください。"

                    return self._add_entry(text)

                return self._show_entries()

            def _extract_text(self, user_input: str) -> str:
                for separator in [":", "："]:
                    if separator in user_input:
                        return user_input.split(separator, 1)[1].strip()
                return ""

            def _load(self) -> dict:
                if not self.path.exists():
                    return {"entries": []}

                try:
                    return json.loads(self.path.read_text(encoding="utf-8"))
                except Exception:
                    return {"entries": []}

            def _save(self, data: dict) -> None:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

            def _add_entry(self, text: str) -> str:
                data = self._load()

                entry = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": text,
                }

                data.setdefault("entries", []).append(entry)
                self._save(data)

                return f"作業記録に追加しました: {text}"

            def _show_entries(self) -> str:
                data = self._load()
                entries = data.get("entries", [])

                lines = ["## Work Log", ""]

                if not entries:
                    lines.append("作業ログはまだありません。")
                    return "\n".join(lines)

                for entry in entries[-10:]:
                    lines.append(f"- {entry.get('time', 'unknown')} | {entry.get('text', '')}")

                return "\n".join(lines)
        ''',
    )

    write_file(
        "nexus/tools/dashboard.py",
        r'''
        """
        Project NEXUS
        Dashboard Tool
        """

        from nexus.context.builder import ContextBuilder
        from nexus.tools.base_tool import BaseTool


        class DashboardTool(BaseTool):
            """Shows a NEXUS dashboard."""

            name = "dashboard"
            description = "NEXUSのダッシュボードを表示します"

            def __init__(self) -> None:
                self.builder = ContextBuilder()

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "ダッシュボード",
                    "nexusダッシュボード",
                    "ホーム",
                    "ホーム画面",
                    "現在のまとめ",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                context = self.builder.build()

                lines = [
                    "## NEXUS Dashboard",
                    "",
                    f"Stage: {context['stage']}",
                    f"Version: {context['version']}",
                    f"Git: {context['git_branch']} / {context['git_status']}",
                    f"Hardware Mode: {context['hardware_mode']}",
                    f"Sphere Ready: {context['sphere_ready']}",
                    "",
                    "Available Core Commands:",
                    "- nexus状況",
                    "- システム情報",
                    "- git要約",
                    "- コミット準備",
                    "- テスト実行",
                    "- ハードウェア状態",
                    "- 作業ログ",
                    "- できること",
                    "",
                ]

                worklog = context.get("recent_worklog", [])
                if worklog:
                    lines.append("Recent Work Log:")
                    for item in worklog:
                        lines.append(f"- {item}")
                else:
                    lines.append("Recent Work Log: none")

                return "\n".join(lines)
        ''',
    )

    write_file(
        "nexus/device/__init__.py",
        r'''
        """
        Project NEXUS
        Device package
        """
        ''',
    )

    write_file(
        "nexus/device/interface.py",
        r'''
        """
        Project NEXUS
        Device Interface
        """

        from __future__ import annotations

        from abc import ABC, abstractmethod


        class DeviceInterface(ABC):
            """Base interface for future physical devices."""

            @abstractmethod
            def status(self) -> dict:
                """Return device status."""

            @abstractmethod
            def is_connected(self) -> bool:
                """Return whether the device is connected."""
        ''',
    )

    write_file(
        "nexus/device/mock.py",
        r'''
        """
        Project NEXUS
        Mock Sphere Device
        """

        from nexus.device.interface import DeviceInterface


        class MockSphereDevice(DeviceInterface):
            """Mock device used before real sphere hardware is connected."""

            def status(self) -> dict:
                return {
                    "device": "Mock Sphere Device",
                    "connected": False,
                    "microphone": "not connected",
                    "speaker": "software voice only",
                    "camera": "not connected",
                    "sensors": "not connected",
                    "motion": "disabled",
                    "safety": "hardware control disabled",
                }

            def is_connected(self) -> bool:
                return False
        ''',
    )

    write_file(
        "nexus/tools/hardware.py",
        r'''
        """
        Project NEXUS
        Hardware Tool
        """

        from nexus.device.mock import MockSphereDevice
        from nexus.tools.base_tool import BaseTool


        class HardwareTool(BaseTool):
            """Shows pre-sphere hardware readiness."""

            name = "hardware"
            description = "球体AI用ハードウェア準備状況を表示します"

            def __init__(self) -> None:
                self.device = MockSphereDevice()

            def can_handle(self, user_input: str) -> bool:
                keywords = {
                    "ハードウェア状態",
                    "球体準備",
                    "sphere readiness",
                    "デバイス状態",
                    "球体状態",
                }
                return any(keyword in user_input for keyword in keywords)

            def execute(self, user_input: str) -> str:
                status = self.device.status()

                lines = [
                    "## Hardware Status",
                    "",
                    f"Device: {status['device']}",
                    f"Connected: {status['connected']}",
                    f"Microphone: {status['microphone']}",
                    f"Speaker: {status['speaker']}",
                    f"Camera: {status['camera']}",
                    f"Sensors: {status['sensors']}",
                    f"Motion: {status['motion']}",
                    f"Safety: {status['safety']}",
                    "",
                    "## Sphere Readiness",
                    "",
                    "- Software Core: ready",
                    "- Tool System: ready",
                    "- Context System: ready",
                    "- Voice Output: basic ready",
                    "- Hardware Interface: mock ready",
                    "- Real Hardware Control: not enabled",
                    "",
                    "次の段階では、実機のマイク・スピーカー・カメラを安全層経由で接続します。",
                ]

                return "\n".join(lines)
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
        "docs/PRE_SPHERE_PLAN.md",
        r'''
        # Project NEXUS Pre-Sphere Plan

        This document describes the stage immediately before physical sphere AI integration.

        ## Current Stage

        NEXUS is currently in the Pre-Sphere Core stage.

        The software system can:

        - Maintain context
        - Use safe tools
        - Read project status
        - Summarize Git changes
        - Run self-tests
        - Speak short messages through macOS
        - Record work logs
        - Show hardware readiness through a mock interface

        ## Hardware Integration Policy

        Real hardware control is intentionally disabled.

        Before enabling hardware control, NEXUS needs:

        - Device permission checks
        - Hardware safety layer
        - Emergency stop logic
        - Input validation
        - Command approval system
        - Persistent hardware logs
        - Manual override mode

        ## Next Stage

        The next stage is Sphere Hardware Bridge.

        Planned components:

        - Microphone input
        - Speaker output
        - Camera input
        - Sensor input
        - Hardware status monitor
        - Safe device command router
        - Emergency stop command
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
                "nexus/context/builder.py",
                "nexus/agent/agent.py",
                "nexus/agent/planner.py",
                "nexus/device/interface.py",
                "nexus/device/mock.py",
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

    append_gitignore()
    append_readme()

    print("Pre-Sphere Core files written.")
    print(f"Backup saved to: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
