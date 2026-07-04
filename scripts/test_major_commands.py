"""
Project NEXUS
Major Command Test Suite v1

Run:
    python3 scripts/test_major_commands.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@dataclass
class CommandTest:
    name: str
    command: str
    expected: str | None = None
    must_handle: bool = True


TESTS = [
    CommandTest(
        name="Command list",
        command="コマンド一覧",
        expected="## NEXUS Command List",
    ),
    CommandTest(
        name="Knowledge commands",
        command="知識コマンド",
        expected="## Knowledge Commands",
    ),
    CommandTest(
        name="Paper commands",
        command="論文コマンド",
        expected="## Paper Commands",
    ),
    CommandTest(
        name="Update commands",
        command="更新コマンド",
        expected="## World / Update Commands",
    ),
    CommandTest(
        name="Backup commands",
        command="バックアップコマンド",
        expected="## Backup / Export Commands",
    ),
    CommandTest(
        name="Diagnostic commands",
        command="診断コマンド",
        expected="## Diagnostic Commands",
    ),
    CommandTest(
        name="Recommended next actions",
        command="おすすめ次操作",
        expected="## Recommended Next Actions",
    ),
    CommandTest(
        name="System health",
        command="システム健康診断",
        expected="System Health",
    ),
    CommandTest(
        name="Feature list",
        command="機能一覧",
        expected="Feature List",
    ),
    CommandTest(
        name="Settings list",
        command="設定一覧",
        expected="Settings",
    ),
    CommandTest(
        name="Backup list",
        command="バックアップ一覧",
        expected="## Backup / Export List",
    ),
    CommandTest(
        name="Project memory overview",
        command="NEXUS記憶",
        expected="## NEXUS Project Memory",
    ),
    CommandTest(
        name="Project memory status",
        command="NEXUS開発状況",
        expected="## NEXUS Development Status",
    ),
    CommandTest(
        name="Project memory position",
        command="NEXUS現在地",
        expected="## NEXUS Current Position",
    ),
    CommandTest(
        name="Project memory milestones",
        command="NEXUSマイルストーン",
        expected="## NEXUS Milestones",
    ),
    CommandTest(
        name="Tool collision check",
        command="ツール衝突チェック",
        expected="Tool Collision Check",
    ),
    CommandTest(
        name="Knowledge digest",
        command="知識ダイジェスト",
        expected="Knowledge",
    ),
    CommandTest(
        name="Knowledge answer PointDiT",
        command="知識回答: PointDiTは何の論文？",
        expected="papers-fafab9fc",
    ),
    CommandTest(
        name="Knowledge answer Maya UV",
        command="知識回答: MayaのUVとは？",
        expected="3dcg-seed-maya-uv",
    ),
]


def shorten(text: str, limit: int = 500) -> str:
    text = text.replace("\n", "\\n")
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def main() -> int:
    from nexus.agent.agent import NexusAgent

    agent = NexusAgent()

    passed = 0
    failed = 0
    results = []

    print("===================================")
    print("Project NEXUS Major Command Tests")
    print("===================================")
    print(f"Total: {len(TESTS)}")
    print("")

    for test in TESTS:
        try:
            handled, result = agent.process(test.command)
            result = result or ""
        except Exception as exc:
            handled = False
            result = f"EXCEPTION: {type(exc).__name__}: {exc}"

        ok = True
        reasons = []

        if test.must_handle and not handled:
            ok = False
            reasons.append("not handled")

        if test.expected and test.expected not in result:
            ok = False
            reasons.append(f"missing expected text: {test.expected}")

        status = "PASS" if ok else "FAIL"

        if ok:
            passed += 1
        else:
            failed += 1

        results.append((status, test, handled, result, reasons))

        print(f"[{status}] {test.name}")
        print(f"  command: {test.command}")
        print(f"  handled: {handled}")

        if not ok:
            print(f"  reasons: {', '.join(reasons)}")
            print(f"  output: {shorten(result)}")

        print("")

    print("===================================")
    print("Summary")
    print("===================================")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("")
        print("Failed Commands:")
        for status, test, handled, result, reasons in results:
            if status == "FAIL":
                print(f"- {test.name}: {test.command}")
                print(f"  reasons: {', '.join(reasons)}")
        return 1

    print("")
    print("All major command tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
