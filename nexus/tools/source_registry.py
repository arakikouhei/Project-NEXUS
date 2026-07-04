"""
Project NEXUS
Source Registry Tool v1
"""

from __future__ import annotations

from nexus.memory.source_registry import SourceRegistryStore
from nexus.tools.base_tool import BaseTool


class SourceRegistryTool(BaseTool):
    """Manages trusted information sources."""

    name = "source_registry"
    description = "信頼できる情報源を登録・検索します"

    def __init__(self) -> None:
        self.store = SourceRegistryStore()

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text == "情報源ヘルプ"
            or text == "情報源カテゴリ"
            or text == "情報源一覧"
            or text.startswith("情報源一覧:")
            or text.startswith("情報源一覧：")
            or text.startswith("情報源追加:")
            or text.startswith("情報源追加：")
            or text.startswith("情報源検索:")
            or text.startswith("情報源検索：")
            or text.startswith("情報源詳細:")
            or text.startswith("情報源詳細：")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "情報源ヘルプ":
            return self._help()

        if text == "情報源カテゴリ":
            return self._categories()

        if text == "情報源一覧":
            return self._list(None)

        if text.startswith(("情報源一覧:", "情報源一覧：")):
            category = self._after_separator(text)
            return self._list(category)

        if text.startswith(("情報源追加:", "情報源追加：")):
            body = self._after_separator(text)
            return self._add(body)

        if text.startswith(("情報源検索:", "情報源検索：")):
            query = self._after_separator(text)
            return self._search(query)

        if text.startswith(("情報源詳細:", "情報源詳細：")):
            source_id = self._after_separator(text)
            return self._detail(source_id)

        return "対応していない情報源操作です。"

    def _after_separator(self, text: str) -> str:
        for separator in [":", "："]:
            if separator in text:
                return text.split(separator, 1)[1].strip()
        return ""

    def _add(self, body: str) -> str:
        parts = [part.strip() for part in body.split("|")]

        if len(parts) < 3:
            return (
                "形式が違います。\n\n"
                "例:\n"
                "情報源追加: papers | arXiv | https://arxiv.org/ | オープンアクセス論文・プレプリント\n\n"
                "形式:\n"
                "情報源追加: category | name | url | note | trust_level"
            )

        category = parts[0]
        name = parts[1]
        url = parts[2]
        note = parts[3] if len(parts) >= 4 else ""
        trust_level = parts[4] if len(parts) >= 5 else "medium"

        try:
            entry = self.store.add(
                category=category,
                name=name,
                url=url,
                note=note,
                trust_level=trust_level,
            )
        except Exception as error:
            return f"情報源追加に失敗しました: {error}"

        return (
            "## Source Added\n\n"
            f"- ID: {entry.get('id')}\n"
            f"- Category: {entry.get('category')}\n"
            f"- Name: {entry.get('name')}\n"
            f"- URL: {entry.get('url')}\n"
            f"- Trust Level: {entry.get('trust_level')}\n"
            f"- Note: {entry.get('note')}"
        )

    def _search(self, query: str) -> str:
        if not query:
            return "検索語がありません。"

        results = self.store.search(query, limit=10)

        if not results:
            return f"## Source Search\n\n検索語: {query}\n\n該当する情報源は見つかりませんでした。"

        lines = [
            "## Source Search",
            "",
            f"検索語: {query}",
            "",
        ]

        for index, item in enumerate(results, start=1):
            lines.append(f"### {index}. {item.get('id')}")
            lines.append(f"- Category: {item.get('category')}")
            lines.append(f"- Name: {item.get('name')}")
            lines.append(f"- URL: {item.get('url')}")
            lines.append(f"- Trust Level: {item.get('trust_level')}")
            if item.get("note"):
                lines.append(f"- Note: {item.get('note')}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _list(self, category: str | None) -> str:
        category = category.strip() if category else None
        sources = self.store.list_sources(category=category, limit=50)

        title = "## Source List"
        if category:
            title += f" / {self.store.normalize_category(category)}"

        if not sources:
            return title + "\n\nまだ情報源は登録されていません。"

        lines = [title, ""]

        for item in sources:
            lines.append(f"### {item.get('id')}")
            lines.append(f"- Category: {item.get('category')}")
            lines.append(f"- Name: {item.get('name')}")
            lines.append(f"- URL: {item.get('url')}")
            lines.append(f"- Trust Level: {item.get('trust_level')}")
            if item.get("note"):
                lines.append(f"- Note: {item.get('note')}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _detail(self, source_id: str) -> str:
        if not source_id:
            return "IDがありません。例: 情報源詳細: source-papers-xxxxxxxx"

        item = self.store.get(source_id)

        if not item:
            return f"情報源IDが見つかりません: {source_id}"

        return (
            "## Source Detail\n\n"
            f"- ID: {item.get('id')}\n"
            f"- Category: {item.get('category')}\n"
            f"- Name: {item.get('name')}\n"
            f"- URL: {item.get('url')}\n"
            f"- Trust Level: {item.get('trust_level')}\n"
            f"- Status: {item.get('status')}\n"
            f"- Created: {item.get('created_at')}\n"
            f"- Updated: {item.get('updated_at')}\n"
            f"- Note: {item.get('note')}"
        )

    def _categories(self) -> str:
        lines = ["## Source Categories", ""]

        for key, description in self.store.categories().items():
            lines.append(f"- {key}: {description}")

        return "\n".join(lines)

    def _help(self) -> str:
        return (
            "## Source Registry Help\n\n"
            "使えるコマンド:\n"
            "- 情報源カテゴリ\n"
            "- 情報源追加: papers | arXiv | https://arxiv.org/ | オープンアクセス論文・プレプリント | high\n"
            "- 情報源検索: arXiv\n"
            "- 情報源一覧\n"
            "- 情報源一覧: papers\n"
            "- 情報源詳細: source-papers-xxxxxxxx\n\n"
            "カテゴリ:\n"
            "- general\n"
            "- world\n"
            "- papers\n"
            "- 3dcg\n"
            "- programming\n"
            "- development\n"
            "- official\n\n"
            "Trust Level:\n"
            "- high: 公式・一次情報に近い\n"
            "- medium: 参考にできるが確認が必要\n"
            "- low: 参考程度\n\n"
            "保存先:\n"
            "- data/knowledge/source_registry.json"
        )
