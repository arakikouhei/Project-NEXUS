"""
Project NEXUS
Memory Index Tool v1

Shows an overview of NEXUS memory-related files, categories, and important entries.
"""

from __future__ import annotations

from pathlib import Path
import json

from nexus.tools.base_tool import BaseTool


class MemoryIndexTool(BaseTool):
    """Shows memory index and memory-related file overview."""

    name = "memory_index"
    description = "NEXUSの記憶系データの全体像を表示します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return text in {
            "記憶インデックス",
            "記憶カテゴリ一覧",
            "記憶重要項目",
            "記憶ファイル一覧",
        }

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "記憶インデックス":
            return self._memory_index()

        if text == "記憶カテゴリ一覧":
            return self._memory_categories()

        if text == "記憶重要項目":
            return self._important_memory_items()

        if text == "記憶ファイル一覧":
            return self._memory_files()

        return "対応していない記憶インデックス操作です。"

    def _memory_index(self) -> str:
        project_memory = self._load_json("data/project/project_memory.json", {})
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        sources = self._load_json("data/knowledge/source_registry.json", [])
        world_updates = self._load_json("data/knowledge/world_updates.json", [])

        categories = self._category_counts(knowledge)

        lines = [
            "## NEXUS Memory Index",
            "",
            "### Project Memory",
            "",
            f"- Current Stage: {project_memory.get('current_stage', 'unknown') if isinstance(project_memory, dict) else 'unknown'}",
            f"- Recommended Next Stage: {project_memory.get('recommended_next_stage', 'unknown') if isinstance(project_memory, dict) else 'unknown'}",
            "",
            "### Knowledge Core",
            "",
            f"- Knowledge Entries: {len(knowledge) if isinstance(knowledge, list) else 0}",
            f"- Categories: {len(categories)}",
            f"- Source Registry Entries: {len(sources) if isinstance(sources, list) else 0}",
            f"- World Update Logs: {len(world_updates) if isinstance(world_updates, list) else 0}",
            "",
            "### Main Categories",
            "",
        ]

        for category, count in sorted(categories.items(), key=lambda x: (-x[1], x[0]))[:10]:
            lines.append(f"- {category}: {count}")

        lines.extend([
            "",
            "### Related Commands",
            "",
            "- 記憶カテゴリ一覧",
            "- 記憶重要項目",
            "- 記憶ファイル一覧",
            "- NEXUS現在地",
            "- 知識ダイジェスト",
        ])

        return "\n".join(lines)

    def _memory_categories(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        categories = self._category_counts(knowledge)

        lines = [
            "## Memory Categories",
            "",
        ]

        if not categories:
            lines.append("- No categories found.")
            return "\n".join(lines)

        for category, count in sorted(categories.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {category}: {count}")

        return "\n".join(lines)

    def _important_memory_items(self) -> str:
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        project_memory = self._load_json("data/project/project_memory.json", {})

        lines = [
            "## Important Memory Items",
            "",
            "### Project",
            "",
            f"- Current Stage: {project_memory.get('current_stage', 'unknown') if isinstance(project_memory, dict) else 'unknown'}",
            f"- Recommended Next Stage: {project_memory.get('recommended_next_stage', 'unknown') if isinstance(project_memory, dict) else 'unknown'}",
            "",
            "### Key Knowledge Entries",
            "",
        ]

        if not isinstance(knowledge, list):
            knowledge = []

        preferred_categories = {"project", "research", "papers", "imported", "world", "3dcg", "development"}

        important = []
        for entry in knowledge:
            if not isinstance(entry, dict):
                continue

            category = entry.get("category", "unknown")
            entry_id = entry.get("id", "unknown")
            title = entry.get("title", "untitled")

            score = 0
            if category in preferred_categories:
                score += 10
            if str(entry_id).startswith(("research-", "papers-", "imported-")):
                score += 8
            if entry.get("archived"):
                score -= 20

            if score > 0:
                important.append((score, entry_id, title, category))

        important.sort(key=lambda x: (-x[0], x[1]))

        if not important:
            lines.append("- No important entries found.")
        else:
            for score, entry_id, title, category in important[:15]:
                lines.append(f"- {entry_id} | {title} | category={category}")

        lines.extend([
            "",
            "### Key Docs",
            "",
        ])

        for doc in self._key_docs():
            lines.append(f"- {doc}")

        return "\n".join(lines)

    def _memory_files(self) -> str:
        files = [
            "data/project/project_memory.json",
            "data/knowledge/knowledge.json",
            "data/knowledge/source_registry.json",
            "data/knowledge/world_updates.json",
            "data/knowledge/search_settings.json",
            "data/knowledge/auto_recall_settings.json",
            "docs/RELEASE_SNAPSHOT_V0_5.md",
            "docs/V0_6_PLAN.md",
            "docs/SAFE_REFACTOR_V1.md",
        ]

        lines = [
            "## Memory Files",
            "",
        ]

        for file in files:
            path = Path(file)
            if path.exists():
                size = self._format_size(path.stat().st_size)
                lines.append(f"- OK | {file} | {size}")
            else:
                lines.append(f"- MISSING | {file}")

        return "\n".join(lines)

    def _load_json(self, path_text: str, default):
        path = Path(path_text)

        if not path.exists():
            return default

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _category_counts(self, knowledge) -> dict:
        counts = {}

        if not isinstance(knowledge, list):
            return counts

        for entry in knowledge:
            if not isinstance(entry, dict):
                continue

            category = entry.get("category", "unknown")
            counts[category] = counts.get(category, 0) + 1

        return counts

    def _key_docs(self) -> list[str]:
        candidates = [
            "docs/RELEASE_SNAPSHOT_V0_5.md",
            "docs/V0_6_PLAN.md",
            "docs/V0_5_PLAN.md",
            "docs/SAFE_REFACTOR_V1.md",
            "docs/SYSTEM_HEALTH_V3.md",
            "docs/COMMAND_HELP_V2.md",
            "docs/TEST_SUITE_V2.md",
        ]

        return [item for item in candidates if Path(item).exists()]

    def _format_size(self, size: int) -> str:
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        if size >= 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size} B"
