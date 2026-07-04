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
        "nexus/context/builder.py",
        "nexus/agent/agent.py",
        "nexus/agent/planner.py",
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
        ("システム情報", "System Info"),
        ("git要約", "Git Summary"),
        ("変更確認", "Git Diff Summary"),
        ("最近のコミット", "Recent Commits"),
        ("pwd", str(ROOT)),
        ("ls nexus/tools", "manager.py"),
        ("git push", "許可されていないgitコマンド"),
        ("rm README.md", "安全のため"),
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
            print("結果:", result[:300])
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
