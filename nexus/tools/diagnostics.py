"""
Project NEXUS
Tool Diagnostics v1

Diagnoses tool routing, tool order, and command collisions.
"""

from __future__ import annotations

from nexus.tools.base_tool import BaseTool


class ToolDiagnosticsTool(BaseTool):
    """Diagnoses which tools can handle an input."""

    name = "tool_diagnostics"
    description = "ツールの順序・衝突・横取りを診断します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "ツール順序"
            or text == "ツール一覧"
            or text == "ツール衝突チェック"
            or text.startswith("ツール診断:")
            or text.startswith("ツール診断：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text in {"ツール順序", "ツール一覧"}:
            return self._tool_order()

        if text == "ツール衝突チェック":
            return self._collision_check()

        if text.startswith(("ツール診断:", "ツール診断：")):
            query = self._extract_query(text)
            return self._diagnose_query(query)

        return "対応していないツール診断です。"

    def _manager(self):
        # 遅延import。ToolManagerの循環importを避ける。
        from nexus.tools.manager import ToolManager

        return ToolManager()

    def _extract_query(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _tool_order(self) -> str:
        manager = self._manager()

        lines = ["## Tool Order", ""]

        for index, tool in enumerate(manager.tools, start=1):
            lines.append(f"{index:02d}. {tool.__class__.__name__} / {getattr(tool, 'name', 'unknown')}")

        lines.append("")
        lines.append("Notes:")
        lines.append("- 上にあるツールほど先に判定されます。")
        lines.append("- CalculatorToolのような広いツールは、専用ツールより後ろが安全です。")

        return "\n".join(lines)

    def _diagnose_query(self, query: str) -> str:
        if not query:
            return "診断する入力がありません。例: ツール診断: 画像分析: tests/assets/sample_vision.png"

        manager = self._manager()
        hits = []

        for index, tool in enumerate(manager.tools, start=1):
            try:
                can = tool.can_handle(query)
            except Exception as error:
                hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown"), f"ERROR: {error}"))
                continue

            if can:
                hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown"), "MATCH"))

        lines = [
            "## Tool Diagnosis",
            "",
            f"Input: {query}",
            "",
        ]

        if not hits:
            lines.append("Result: どのツールも反応しませんでした。")
            return "\n".join(lines)

        lines.append("Matched tools:")
        for index, class_name, name, status in hits:
            lines.append(f"- {index:02d}. {class_name} / {name} [{status}]")

        first = hits[0]
        lines.append("")
        lines.append(f"Selected: {first[1]} / {first[2]}")

        if len(hits) >= 2:
            lines.append("")
            lines.append("Warning:")
            lines.append("- 複数ツールが同じ入力に反応しています。")
            lines.append("- 実際には一番上のツールだけが実行されます。")
            lines.append("- 意図しない横取りが起きる可能性があります。")

        return "\n".join(lines)

    def _collision_check(self) -> str:
        sample_inputs = [
            "画像ヘルプ",
            "画像安全確認: tests/assets/sample_vision.png",
            "画像分析: tests/assets/sample_vision.png",
            "計算: (2+5)*3",
            "単位変換: 40km/hをm/s",
            "安全検索: 東京造形",
            "調べて: 東京造形",
            "web要約: https://example.com",
            "url安全確認: https://example.com",
            "アプリ一覧",
            "git状態",
            "ls nexus/tools",
            "できること",
            "ダッシュボード",
            "テスト実行",
        ]

        manager = self._manager()

        lines = [
            "## Tool Collision Check",
            "",
        ]

        has_warning = False

        for query in sample_inputs:
            hits = []

            for index, tool in enumerate(manager.tools, start=1):
                try:
                    if tool.can_handle(query):
                        hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown")))
                except Exception as error:
                    hits.append((index, tool.__class__.__name__, getattr(tool, "name", "unknown") + f" ERROR:{error}"))

            if len(hits) == 0:
                lines.append(f"MISS: {query}")
                has_warning = True
            elif len(hits) == 1:
                index, class_name, name = hits[0]
                lines.append(f"OK: {query} -> {index:02d}. {class_name}")
            else:
                has_warning = True
                first = hits[0]
                rest = ", ".join(f"{i:02d}.{c}" for i, c, n in hits[1:])
                lines.append(f"WARN: {query} -> selected {first[0]:02d}. {first[1]} / also {rest}")

        lines.append("")
        if has_warning:
            lines.append("Result: 注意が必要な項目があります。")
            lines.append("WARNは必ずしも失敗ではありませんが、横取りの原因になります。")
        else:
            lines.append("Result: 主要コマンドに大きな衝突は見つかりませんでした。")

        return "\n".join(lines)


# SYSTEM_HEALTH_V1_SAFE_PATCH

def _sh_v1_load_json(path_text: str, default):
    import json
    from pathlib import Path

    path = Path(path_text)

    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _sh_v1_git_status() -> dict:
    import subprocess

    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=8,
        )

        output = result.stdout.strip()

        return {
            "ok": result.returncode == 0,
            "clean": output == "",
            "output": output,
        }
    except Exception as error:
        return {
            "ok": False,
            "clean": False,
            "output": str(error),
        }


def _sh_v1_py_compile() -> dict:
    import py_compile
    from pathlib import Path

    files = [
        "main.py",
        "nexus/agent/agent.py",
        "nexus/tools/manager.py",
        "nexus/tools/diagnostics.py",
        "nexus/tools/knowledge.py",
        "nexus/tools/paper_intake.py",
        "nexus/tools/world_update.py",
        "nexus/tools/source_registry.py",
        "nexus/memory/knowledge_store.py",
        "nexus/memory/source_registry.py",
        "nexus/memory/world_update_store.py",
    ]

    ok = []
    errors = []

    for file in files:
        path = Path(file)

        if not path.exists():
            errors.append(f"{file}: missing")
            continue

        try:
            py_compile.compile(str(path), doraise=True)
            ok.append(file)
        except Exception as error:
            errors.append(f"{file}: {error}")

    return {
        "ok_count": len(ok),
        "error_count": len(errors),
        "errors": errors,
    }


def _sh_v1_knowledge_stats() -> dict:
    knowledge = _sh_v1_load_json("data/knowledge/knowledge.json", [])
    world_updates = _sh_v1_load_json("data/knowledge/world_updates.json", [])
    source_registry = _sh_v1_load_json("data/knowledge/source_registry.json", [])

    if not isinstance(knowledge, list):
        knowledge = []

    if not isinstance(world_updates, list):
        world_updates = []

    if not isinstance(source_registry, list):
        source_registry = []

    by_category = {}
    by_source = {}
    archived = 0

    for entry in knowledge:
        category = entry.get("category", "unknown")
        source = entry.get("source", "unknown")

        by_category[category] = by_category.get(category, 0) + 1
        by_source[source] = by_source.get(source, 0) + 1

        if entry.get("archived"):
            archived += 1

    return {
        "knowledge_total": len(knowledge),
        "papers": by_category.get("papers", 0),
        "world": by_category.get("world", 0),
        "three_dcg": by_category.get("3dcg", 0),
        "development": by_category.get("development", 0),
        "archived": archived,
        "world_updates": len(world_updates),
        "source_registry": len(source_registry),
        "by_category": by_category,
        "by_source": by_source,
    }


def _sh_v1_settings() -> dict:
    search_settings = _sh_v1_load_json(
        "data/knowledge/search_settings.json",
        {"include_archived": False},
    )

    auto_recall = _sh_v1_load_json(
        "data/knowledge/auto_recall_settings.json",
        {"enabled": False, "max_results": 3, "min_score": 18},
    )

    return {
        "search_settings": search_settings,
        "auto_recall": auto_recall,
    }


def _sh_v1_feature_list() -> list[tuple[str, bool]]:
    from pathlib import Path

    checks = [
        ("Knowledge Core", Path("nexus/tools/knowledge.py").exists()),
        ("Source Registry", Path("nexus/tools/source_registry.py").exists()),
        ("World Update", Path("nexus/tools/world_update.py").exists()),
        ("Paper Intake", Path("nexus/tools/paper_intake.py").exists()),
        ("Knowledge Search v2", "KNOWLEDGE_SEARCH_V2_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Knowledge Digest v1", "KNOWLEDGE_DIGEST_V1_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Knowledge Cleanup v1", "KNOWLEDGE_CLEANUP_V1_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Archive Filter v1", "ARCHIVE_FILTER_V1_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Source Trust v1", "SOURCE_TRUST_V1_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Knowledge Answer v2", "KNOWLEDGE_ANSWER_V2_NATURAL_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Knowledge Auto Recall Guard", "KNOWLEDGE_AUTO_RECALL_GUARD_V1_SAFE_PATCH" in Path("nexus/tools/knowledge.py").read_text(encoding="utf-8")),
        ("Knowledge Auto Recall v1", "KNOWLEDGE_AUTO_RECALL_V1" in Path("nexus/agent/agent.py").read_text(encoding="utf-8")),
    ]

    return checks


def _sh_v1_feature_report() -> str:
    features = _sh_v1_feature_list()

    lines = [
        "## NEXUS Feature List",
        "",
    ]

    for name, enabled in features:
        mark = "✅" if enabled else "❌"
        lines.append(f"- {mark} {name}")

    return "\n".join(lines)


def _sh_v1_settings_report() -> str:
    settings = _sh_v1_settings()
    search = settings["search_settings"]
    recall = settings["auto_recall"]

    include_archived = bool(search.get("include_archived", False))
    auto_enabled = bool(recall.get("enabled", False))

    lines = [
        "## NEXUS Settings",
        "",
        "### Knowledge Search",
        f"- include_archived: {include_archived}",
        f"- Mode: {'アーカイブ込み' if include_archived else 'アーカイブ除外'}",
        "",
        "### Knowledge Auto Recall",
        f"- enabled: {auto_enabled}",
        f"- Mode: {'ON' if auto_enabled else 'OFF'}",
        f"- max_results: {recall.get('max_results', 3)}",
        f"- min_score: {recall.get('min_score', 18)}",
    ]

    return "\n".join(lines)


def _sh_v1_status_report() -> str:
    git = _sh_v1_git_status()
    stats = _sh_v1_knowledge_stats()
    settings = _sh_v1_settings()

    search = settings["search_settings"]
    recall = settings["auto_recall"]

    lines = [
        "## NEXUS Status",
        "",
        f"- Git Clean: {git.get('clean')}",
        f"- Knowledge Entries: {stats.get('knowledge_total')}",
        f"- Papers: {stats.get('papers')}",
        f"- World Knowledge: {stats.get('world')}",
        f"- World Update Logs: {stats.get('world_updates')}",
        f"- Archived Entries: {stats.get('archived')}",
        f"- Source Registry Entries: {stats.get('source_registry')}",
        f"- Archive Filter: {'include archived' if search.get('include_archived') else 'exclude archived'}",
        f"- Auto Recall: {'ON' if recall.get('enabled') else 'OFF'}",
    ]

    return "\n".join(lines)


def _sh_v1_health_report() -> str:
    git = _sh_v1_git_status()
    compile_result = _sh_v1_py_compile()
    stats = _sh_v1_knowledge_stats()
    settings = _sh_v1_settings()
    features = _sh_v1_feature_list()

    feature_ok = sum(1 for name, ok in features if ok)
    feature_total = len(features)

    lines = [
        "## System Health",
        "",
        "### Overall",
        f"- Git Clean: {git.get('clean')}",
        f"- Python Compile Errors: {compile_result.get('error_count')}",
        f"- Features Detected: {feature_ok}/{feature_total}",
        "",
        "### Git",
    ]

    if git.get("clean"):
        lines.append("- working tree clean")
    else:
        lines.append("- working tree has changes:")
        output = git.get("output") or "(no output)"
        for line in output.splitlines()[:20]:
            lines.append(f"  {line}")

    lines.append("")
    lines.append("### Python Compile")

    if compile_result.get("error_count") == 0:
        lines.append(f"- OK: {compile_result.get('ok_count')} files")
    else:
        lines.append(f"- Errors: {compile_result.get('error_count')}")
        for error in compile_result.get("errors", [])[:12]:
            lines.append(f"  - {error}")

    lines.append("")
    lines.append("### Knowledge")
    lines.append(f"- Total: {stats.get('knowledge_total')}")
    lines.append(f"- Papers: {stats.get('papers')}")
    lines.append(f"- World: {stats.get('world')}")
    lines.append(f"- 3DCG: {stats.get('three_dcg')}")
    lines.append(f"- Development: {stats.get('development')}")
    lines.append(f"- Archived: {stats.get('archived')}")
    lines.append(f"- World Update Logs: {stats.get('world_updates')}")
    lines.append(f"- Source Registry: {stats.get('source_registry')}")

    lines.append("")
    lines.append("### Settings")
    lines.append(f"- Archive Filter include_archived: {settings['search_settings'].get('include_archived', False)}")
    lines.append(f"- Auto Recall enabled: {settings['auto_recall'].get('enabled', False)}")

    lines.append("")
    lines.append("### Features")
    for name, enabled in features:
        mark = "✅" if enabled else "❌"
        lines.append(f"- {mark} {name}")

    lines.append("")
    lines.append("Note: System Health v1 は状態確認のみです。ファイルの変更・削除はしません。")

    return "\n".join(lines)


_sh_v1_can_handle_base = ToolDiagnosticsTool.can_handle
_sh_v1_execute_base = ToolDiagnosticsTool.execute

def _sh_v1_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()

    return (
        _sh_v1_can_handle_base(self, user_input)
        or text == "システム健康診断"
        or text == "NEXUS状態確認"
        or text == "機能一覧"
        or text == "設定一覧"
    )


def _sh_v1_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text == "システム健康診断":
        return _sh_v1_health_report()

    if text == "NEXUS状態確認":
        return _sh_v1_status_report()

    if text == "機能一覧":
        return _sh_v1_feature_report()

    if text == "設定一覧":
        return _sh_v1_settings_report()

    return _sh_v1_execute_base(self, user_input)


ToolDiagnosticsTool.can_handle = _sh_v1_can_handle
ToolDiagnosticsTool.execute = _sh_v1_execute
