"""
Project NEXUS
Knowledge Tool v1
"""

from __future__ import annotations

from nexus.memory.knowledge_store import KnowledgeStore
from nexus.tools.base_tool import BaseTool


class KnowledgeTool(BaseTool):
    """Adds and searches local knowledge."""

    name = "knowledge"
    description = "知識ベースに知識を追加・検索します"

    def __init__(self) -> None:
        self.store = KnowledgeStore()

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "知識ヘルプ"
            or text == "知識カテゴリ"
            or text == "知識一覧"
            or text.startswith("知識一覧:")
            or text.startswith("知識一覧：")
            or text.startswith("知識追加:")
            or text.startswith("知識追加：")
            or text.startswith("知識検索:")
            or text.startswith("知識検索：")
            or text.startswith("知識詳細:")
            or text.startswith("知識詳細：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "知識ヘルプ":
            return self._help()

        if text == "知識カテゴリ":
            return self._categories()

        if text == "知識一覧":
            return self._list(None)

        if text.startswith(("知識一覧:", "知識一覧：")):
            category = self._after_separator(text)
            return self._list(category)

        if text.startswith(("知識追加:", "知識追加：")):
            body = self._after_separator(text)
            return self._add(body)

        if text.startswith(("知識検索:", "知識検索：")):
            query = self._after_separator(text)
            return self._search(query)

        if text.startswith(("知識詳細:", "知識詳細：")):
            entry_id = self._after_separator(text)
            return self._detail(entry_id)

        return "対応していない知識操作です。"

    def _after_separator(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _add(self, body: str) -> str:
        if "|" not in body:
            return (
                "形式が違います。\n\n"
                "例:\n"
                "知識追加: 3dcg | MayaのUVは3Dモデル表面を2D座標に展開する仕組み。"
            )

        category, content = [part.strip() for part in body.split("|", 1)]

        if not category or not content:
            return "カテゴリまたは本文が空です。"

        try:
            entry = self.store.add(category=category, content=content)
        except Exception as error:
            return f"知識追加に失敗しました: {error}"

        return (
            "## Knowledge Added\n\n"
            f"- ID: {entry['id']}\n"
            f"- Category: {entry['category']}\n"
            f"- Source: {entry['source']}\n"
            f"- Tags: {', '.join(entry.get('tags', []))}\n\n"
            f"{entry['content']}"
        )

    def _search(self, query: str) -> str:
        if not query:
            return "検索語がありません。"

        results = self.store.search(query, limit=10)

        if not results:
            return f"## Knowledge Search\n\n検索語: {query}\n\n該当する知識は見つかりませんでした。"

        lines = [
            "## Knowledge Search",
            "",
            f"検索語: {query}",
            "",
        ]

        for index, item in enumerate(results, start=1):
            content = item.get("content", "")
            if len(content) > 180:
                content = content[:180].rstrip() + "..."

            lines.append(f"### {index}. {item.get('id')}")
            lines.append(f"- Category: {item.get('category')}")
            lines.append(f"- Created: {item.get('created_at')}")
            lines.append(f"- Tags: {', '.join(item.get('tags', []))}")
            lines.append("")
            lines.append(content)
            lines.append("")

        return "\n".join(lines).rstrip()

    def _list(self, category: str | None) -> str:
        category = category.strip() if category else None
        entries = self.store.list_entries(category=category, limit=20)

        title = "## Knowledge List"
        if category:
            title += f" / {self.store.normalize_category(category)}"

        if not entries:
            return title + "\n\nまだ知識は登録されていません。"

        lines = [title, ""]

        for item in entries:
            content = item.get("content", "")
            if len(content) > 120:
                content = content[:120].rstrip() + "..."

            lines.append(f"### {item.get('id')}")
            lines.append(f"- Category: {item.get('category')}")
            lines.append(f"- Created: {item.get('created_at')}")
            lines.append(f"- Content: {content}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _detail(self, entry_id: str) -> str:
        if not entry_id:
            return "IDがありません。例: 知識詳細: 3dcg-xxxxxxxx"

        item = self.store.get(entry_id)

        if not item:
            return f"知識IDが見つかりません: {entry_id}"

        return (
            "## Knowledge Detail\n\n"
            f"- ID: {item.get('id')}\n"
            f"- Category: {item.get('category')}\n"
            f"- Source: {item.get('source')}\n"
            f"- Created: {item.get('created_at')}\n"
            f"- Updated: {item.get('updated_at')}\n"
            f"- Tags: {', '.join(item.get('tags', []))}\n\n"
            f"{item.get('content')}"
        )

    def _categories(self) -> str:
        lines = ["## Knowledge Categories", ""]

        for key, description in self.store.categories().items():
            lines.append(f"- {key}: {description}")

        return "\n".join(lines)

    def _help(self) -> str:
        return (
            "## Knowledge Help\n\n"
            "使えるコマンド:\n"
            "- 知識カテゴリ\n"
            "- 知識追加: 3dcg | MayaのUVは3Dモデル表面を2D座標に展開する仕組み。\n"
            "- 知識検索: Maya UV\n"
            "- 知識一覧\n"
            "- 知識一覧: 3dcg\n"
            "- 知識詳細: 3dcg-xxxxxxxx\n\n"
            "カテゴリ:\n"
            "- general: 一般知識\n"
            "- world: 社会情勢・ニュース\n"
            "- papers: 論文\n"
            "- 3dcg: 3DCG\n"
            "- programming: プログラミング\n"
            "- development: 開発\n"
            "- source_registry: 情報源\n\n"
            "保存先:\n"
            "- data/knowledge/knowledge.json"
        )
