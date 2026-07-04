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


# KNOWLEDGE_SEARCH_V2_SAFE_PATCH

def _ks_v2_sep(text: str) -> str:
    for s in [":", "："]:
        if s in text:
            return text.split(s, 1)[1].strip()
    return ""


def _ks_v2_all_entries(self) -> list[dict]:
    try:
        return self.store.list_entries(limit=1000)
    except TypeError:
        return self.store.list_entries()


def _ks_v2_score(entry: dict, query: str) -> int:
    q = query.lower().strip()
    if not q:
        return 0

    content = str(entry.get("content", ""))
    source = str(entry.get("source", ""))
    category = str(entry.get("category", ""))
    tags = " ".join(entry.get("tags", []))

    text = f"{content} {source} {category} {tags}"
    low = text.lower()

    score = 0

    for token in q.split():
        if not token:
            continue

        token_low = token.lower()

        if token_low in low:
            score += 10

        if token_low in category.lower():
            score += 8

        if token_low in source.lower():
            score += 6

        if token_low in tags.lower():
            score += 12

    if q in low:
        score += 20

    if q in tags.lower():
        score += 20

    if q in category.lower():
        score += 10

    return score


def _ks_v2_cross_search(self, query: str) -> str:
    query = query.strip()

    if not query:
        return "検索語がありません。例: 知識横断検索: diffusion"

    entries = _ks_v2_all_entries(self)
    scored = []

    for entry in entries:
        score = _ks_v2_score(entry, query)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return f"## Knowledge Cross Search\n\nQuery: {query}\n\n該当する知識が見つかりませんでした。"

    lines = [
        "## Knowledge Cross Search",
        "",
        f"Query: {query}",
        "",
    ]

    for score, entry in scored[:12]:
        content = str(entry.get("content", ""))
        preview = content.replace("\n", " ")

        if len(preview) > 260:
            preview = preview[:260].rstrip() + "..."

        lines.append(f"### {entry.get('id')}")
        lines.append(f"- Score: {score}")
        lines.append(f"- Category: {entry.get('category')}")
        lines.append(f"- Source: {entry.get('source')}")
        lines.append(f"- Tags: {', '.join(entry.get('tags', []))}")
        lines.append(f"- Preview: {preview}")
        lines.append("")

    return "\n".join(lines).rstrip()


def _ks_v2_summary(self, query: str) -> str:
    query = query.strip()

    if not query:
        return "検索語がありません。例: 知識まとめ: diffusion"

    entries = _ks_v2_all_entries(self)
    scored = []

    for entry in entries:
        score = _ks_v2_score(entry, query)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:8]

    if not top:
        return f"## Knowledge Summary\n\nQuery: {query}\n\nまとめられる知識が見つかりませんでした。"

    by_category = {}
    sources = {}
    keywords = {}

    for score, entry in top:
        category = entry.get("category", "unknown")
        source = entry.get("source", "unknown")
        by_category[category] = by_category.get(category, 0) + 1
        sources[source] = sources.get(source, 0) + 1

        for tag in entry.get("tags", []):
            keywords[tag] = keywords.get(tag, 0) + 1

    lines = [
        "## Knowledge Summary",
        "",
        f"Query: {query}",
        f"Matched Entries: {len(scored)}",
        "",
        "### Categories",
    ]

    for category, count in sorted(by_category.items(), key=lambda x: -x[1]):
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("### Sources")

    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        lines.append(f"- {source}: {count}")

    lines.append("")
    lines.append("### Top Related Tags")

    top_tags = sorted(keywords.items(), key=lambda x: (-x[1], x[0]))[:12]

    if top_tags:
        for tag, count in top_tags:
            lines.append(f"- {tag}: {count}")
    else:
        lines.append("- タグは少なめです。")

    lines.append("")
    lines.append("### Top Entries")

    for score, entry in top[:5]:
        content = str(entry.get("content", "")).replace("\n", " ")
        if len(content) > 180:
            content = content[:180].rstrip() + "..."

        lines.append(f"- [{entry.get('id')}] {entry.get('category')} / {entry.get('source')} / score={score}")
        lines.append(f"  {content}")

    lines.append("")
    lines.append("Note: これは保存済みKnowledge Core内の簡易まとめです。")

    return "\n".join(lines)


def _ks_v2_related(self, entry_id: str) -> str:
    entry_id = entry_id.strip()

    if not entry_id:
        return "IDがありません。例: 知識関連検索: papers-fafab9fc"

    target = self.store.get(entry_id)

    if not target:
        # IDではなく検索語として扱う
        return _ks_v2_cross_search(self, entry_id)

    target_tags = set(target.get("tags", []))
    target_category = target.get("category", "")
    target_content = str(target.get("content", ""))
    target_words = set(target_content.lower().split()[:80])

    entries = _ks_v2_all_entries(self)
    scored = []

    for entry in entries:
        if entry.get("id") == target.get("id"):
            continue

        score = 0

        tags = set(entry.get("tags", []))
        score += len(target_tags & tags) * 12

        if entry.get("category") == target_category:
            score += 8

        content_words = set(str(entry.get("content", "")).lower().split()[:120])
        score += min(len(target_words & content_words), 20)

        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    lines = [
        "## Related Knowledge",
        "",
        f"Target: {target.get('id')}",
        f"Category: {target.get('category')}",
        f"Source: {target.get('source')}",
        "",
    ]

    if not scored:
        lines.append("関連知識はまだ見つかりませんでした。")
        return "\n".join(lines)

    for score, entry in scored[:10]:
        preview = str(entry.get("content", "")).replace("\n", " ")
        if len(preview) > 220:
            preview = preview[:220].rstrip() + "..."

        lines.append(f"### {entry.get('id')}")
        lines.append(f"- Related Score: {score}")
        lines.append(f"- Category: {entry.get('category')}")
        lines.append(f"- Source: {entry.get('source')}")
        lines.append(f"- Tags: {', '.join(entry.get('tags', []))}")
        lines.append(f"- Preview: {preview}")
        lines.append("")

    return "\n".join(lines).rstrip()


def _ks_v2_source_check(self, query: str) -> str:
    query = query.strip()

    if not query:
        return "検索語がありません。例: 知識ソース確認: diffusion"

    entries = _ks_v2_all_entries(self)
    scored = []

    for entry in entries:
        score = _ks_v2_score(entry, query)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return f"## Knowledge Source Check\n\nQuery: {query}\n\n該当する知識が見つかりませんでした。"

    source_counts = {}
    category_counts = {}

    for score, entry in scored:
        source = entry.get("source", "unknown")
        category = entry.get("category", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1

    lines = [
        "## Knowledge Source Check",
        "",
        f"Query: {query}",
        f"Matched Entries: {len(scored)}",
        "",
        "### Sources",
    ]

    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {source}: {count}")

    lines.append("")
    lines.append("### Categories")

    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("### Caution")
    lines.append("- source='user' や source='world_update_v2' は補助情報として扱う。")
    lines.append("- arXivは査読済みとは限らない。")
    lines.append("- 最新ニュースや論文は原文・公式情報の確認が必要。")

    return "\n".join(lines)


_ks_v1_can_handle = KnowledgeTool.can_handle
_ks_v1_execute = KnowledgeTool.execute

def _ks_v2_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()
    return (
        _ks_v1_can_handle(self, user_input)
        or text.startswith("知識横断検索:")
        or text.startswith("知識横断検索：")
        or text.startswith("知識まとめ:")
        or text.startswith("知識まとめ：")
        or text.startswith("知識関連検索:")
        or text.startswith("知識関連検索：")
        or text.startswith("知識ソース確認:")
        or text.startswith("知識ソース確認：")
    )


def _ks_v2_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text.startswith(("知識横断検索:", "知識横断検索：")):
        return _ks_v2_cross_search(self, _ks_v2_sep(text))

    if text.startswith(("知識まとめ:", "知識まとめ：")):
        return _ks_v2_summary(self, _ks_v2_sep(text))

    if text.startswith(("知識関連検索:", "知識関連検索：")):
        return _ks_v2_related(self, _ks_v2_sep(text))

    if text.startswith(("知識ソース確認:", "知識ソース確認：")):
        return _ks_v2_source_check(self, _ks_v2_sep(text))

    return _ks_v1_execute(self, user_input)


KnowledgeTool.can_handle = _ks_v2_can_handle
KnowledgeTool.execute = _ks_v2_execute
