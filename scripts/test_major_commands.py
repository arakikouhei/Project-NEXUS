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
        name="Command help research commands",
        command="研究コマンド",
        expected="## Research Workflow Commands",
    ),
    CommandTest(
        name="Command help import commands",
        command="インポートコマンド",
        expected="## Import Commands",
    ),
    CommandTest(
        name="Command help project memory commands",
        command="NEXUS記憶コマンド",
        expected="## NEXUS Project Memory Commands",
    ),
    CommandTest(
        name="Command help development commands",
        command="開発コマンド",
        expected="## Development / Maintenance Commands",
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
        name="Work notes help",
        command="作業メモヘルプ",
        expected="## Work Notes Help",
    ),
    CommandTest(
        name="Work notes list",
        command="作業メモ一覧",
        expected="## Work Notes",
    ),
    CommandTest(
        name="Work notes search",
        command="作業メモ検索: UI 音声 カメラ",
        expected="work-10056317",
    ),
    CommandTest(
        name="File index overview",
        command="ファイルインデックス",
        expected="## File Index",
    ),
    CommandTest(
        name="File index important files",
        command="重要ファイル一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="File index docs",
        command="docs一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="File index data",
        command="data一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="File index tools",
        command="tools一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="File index scripts",
        command="scripts一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="File index prompts",
        command="prompts一覧",
        expected="## File Index",
    ),
    CommandTest(
        name="Memory answer current position",
        command="NEXUSは今どこまで進んだ？",
        expected="## Memory Answer",
    ),
    CommandTest(
        name="Memory answer next action",
        command="次に何を作るべき？",
        expected="## Memory Answer",
    ),
    CommandTest(
        name="Memory answer v0.6 status",
        command="v0.6の状態を教えて",
        expected="## Memory Answer",
    ),
    CommandTest(
        name="Memory answer memory status",
        command="記憶の状態を教えて",
        expected="## Memory Answer",
    ),
    CommandTest(
        name="Memory answer UI voice camera",
        command="記憶回答: UI 音声 カメラ",
        expected="work-10056317",
    ),
    CommandTest(
        name="Memory review overview",
        command="記憶レビュー",
        expected="## Memory Review",
    ),
    CommandTest(
        name="Old memory candidates",
        command="古い記憶候補",
        expected="## Old Memory Candidates",
    ),
    CommandTest(
        name="Duplicate memory candidates",
        command="重複記憶候補",
        expected="## Duplicate Memory Candidates",
    ),
    CommandTest(
        name="Memory safety check",
        command="記憶安全確認",
        expected="## Memory Safety Check",
    ),
    CommandTest(
        name="Memory index overview",
        command="記憶インデックス",
        expected="## NEXUS Memory Index",
    ),
    CommandTest(
        name="Memory categories",
        command="記憶カテゴリ一覧",
        expected="## Memory Categories",
    ),
    CommandTest(
        name="Memory important items",
        command="記憶重要項目",
        expected="## Important Memory Items",
    ),
    CommandTest(
        name="Memory files",
        command="記憶ファイル一覧",
        expected="## Memory Files",
    ),
    CommandTest(
        name="System health v0.5 overview",
        command="システム健康診断",
        expected="## v0.5 Project Overview",
    ),
    CommandTest(
        name="Project memory v0.6 stage",
        command="NEXUS現在地",
        expected="v0.6 memory strengthening",
    ),
    CommandTest(
        name="Project memory v0.6 next stage",
        command="NEXUS現在地",
        expected="v0.6 Release Snapshot, then v0.7 planning",
    ),
    CommandTest(
        name="Command list v0.5 research help",
        command="コマンド一覧",
        expected="研究コマンド",
    ),
    CommandTest(
        name="Command list v0.5 import help",
        command="コマンド一覧",
        expected="インポートコマンド",
    ),
    CommandTest(
        name="Command list v0.5 project memory help",
        command="コマンド一覧",
        expected="NEXUS記憶コマンド",
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
        name="Research workflow start",
        command="研究ワークフロー開始: diffusion",
        expected="## Research Workflow Started",
    ),
    CommandTest(
        name="Research workflow summary",
        command="研究まとめ: diffusion",
        expected="## Research Summary",
    ),
    CommandTest(
        name="Research workflow converted knowledge",
        command="知識検索: research-fafab9fc",
        expected="research-fafab9fc",
    ),
    CommandTest(
        name="Knowledge import preview",
        command="インポート確認: tmp/import_test_note.md",
        expected="## Import Preview",
    ),
    CommandTest(
        name="Knowledge import search",
        command="知識検索: NEXUS Import Test Note",
        expected="imported-c5c64a3f",
    ),
    CommandTest(
        name="Project memory save status",
        command="NEXUS記憶保存状況",
        expected="## Project Memory Save Status",
    ),
    CommandTest(
        name="Project memory snapshot create",
        command="NEXUS記憶スナップショット",
        expected="## Project Memory Snapshot Created",
    ),
    CommandTest(
        name="Project memory snapshot history",
        command="NEXUS記憶履歴",
        expected="## Project Memory Snapshot History",
    ),
    CommandTest(
        name="Project memory restore candidates",
        command="NEXUS記憶復元候補",
        expected="## Project Memory Restore Candidates",
    ),
    CommandTest(
        name="Project memory current stage",
        command="NEXUS現在地",
        expected="v0.6 memory strengthening",
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
