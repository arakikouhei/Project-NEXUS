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


# KNOWLEDGE_DIGEST_V1_SAFE_PATCH

def _kd_v1_all_entries(self) -> list[dict]:
    try:
        return self.store.list_entries(limit=2000)
    except TypeError:
        return self.store.list_entries()


def _kd_v1_short(content: str, limit: int = 220) -> str:
    content = str(content).replace("\n", " ").strip()
    if len(content) > limit:
        return content[:limit].rstrip() + "..."
    return content


def _kd_v1_digest(self) -> str:
    entries = _kd_v1_all_entries(self)

    if not entries:
        return "## Knowledge Digest\n\n保存済み知識はまだありません。"

    by_category = {}
    by_source = {}
    tag_counts = {}

    for entry in entries:
        category = entry.get("category", "unknown")
        source = entry.get("source", "unknown")

        by_category[category] = by_category.get(category, 0) + 1
        by_source[source] = by_source.get(source, 0) + 1

        for tag in entry.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    lines = [
        "## Knowledge Digest",
        "",
        f"Total Entries: {len(entries)}",
        "",
        "### Categories",
    ]

    for category, count in sorted(by_category.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- {category}: {count}")

    lines.append("")
    lines.append("### Sources")

    for source, count in sorted(by_source.items(), key=lambda x: (-x[1], x[0]))[:12]:
        lines.append(f"- {source}: {count}")

    lines.append("")
    lines.append("### Frequent Tags")

    top_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))[:15]

    if top_tags:
        for tag, count in top_tags:
            lines.append(f"- {tag}: {count}")
    else:
        lines.append("- タグはまだ少なめです。")

    lines.append("")
    lines.append("### Recent Entries")

    for entry in list(reversed(entries[-8:])):
        lines.append(f"- [{entry.get('id')}] {entry.get('category')} / {entry.get('source')}")
        lines.append(f"  {_kd_v1_short(entry.get('content', ''), 180)}")

    lines.append("")
    lines.append("Note: Knowledge Core内の保存済み知識を簡易集計しています。")

    return "\n".join(lines)


def _kd_v1_category整理(self) -> str:
    entries = _kd_v1_all_entries(self)

    if not entries:
        return "## Knowledge Category Review\n\n保存済み知識はまだありません。"

    categories = {}
    uncategorized = []

    for entry in entries:
        category = entry.get("category", "unknown")
        categories.setdefault(category, []).append(entry)

        if category in {"", "unknown", "general"}:
            uncategorized.append(entry)

    lines = [
        "## Knowledge Category Review",
        "",
        "### Category Counts",
    ]

    for category, items in sorted(categories.items(), key=lambda x: (-len(x[1]), x[0])):
        lines.append(f"- {category}: {len(items)}")

    lines.append("")
    lines.append("### Category Notes")

    if uncategorized:
        lines.append(f"- general/unknown系が {len(uncategorized)} 件あります。必要ならカテゴリを分ける候補です。")
    else:
        lines.append("- 大きな未分類偏りは見つかりませんでした。")

    if len(categories) <= 2 and len(entries) >= 10:
        lines.append("- 知識数に対してカテゴリ数が少なめです。papers/world/3dcg/development等に分けると探しやすくなります。")

    lines.append("")
    lines.append("### Samples")

    for category, items in sorted(categories.items(), key=lambda x: x[0])[:10]:
        lines.append(f"#### {category}")
        for entry in items[:3]:
            lines.append(f"- {entry.get('id')}: {_kd_v1_short(entry.get('content', ''), 120)}")

    return "\n".join(lines)


def _kd_v1_duplicates(self) -> str:
    entries = _kd_v1_all_entries(self)

    if not entries:
        return "## Knowledge Duplicate Check\n\n保存済み知識はまだありません。"

    seen = {}
    duplicates = []

    for entry in entries:
        content = str(entry.get("content", "")).strip().lower()
        normalized = " ".join(content.split())

        key = normalized[:220]

        if key in seen:
            duplicates.append((seen[key], entry))
        else:
            seen[key] = entry

    # タイトル/URLっぽい重複も軽く見る
    url_seen = {}
    url_duplicates = []

    for entry in entries:
        content = str(entry.get("content", ""))
        urls = []
        for part in content.split():
            if part.startswith("http://") or part.startswith("https://"):
                urls.append(part.strip())

        for url in urls:
            if url in url_seen:
                url_duplicates.append((url_seen[url], entry, url))
            else:
                url_seen[url] = entry

    lines = [
        "## Knowledge Duplicate Check",
        "",
        f"Total Entries: {len(entries)}",
        f"Exact-like Duplicates: {len(duplicates)}",
        f"URL Duplicates: {len(url_duplicates)}",
        "",
    ]

    if not duplicates and not url_duplicates:
        lines.append("大きな重複は見つかりませんでした。")
        return "\n".join(lines)

    if duplicates:
        lines.append("### Exact-like Duplicates")
        for a, b in duplicates[:10]:
            lines.append(f"- {a.get('id')} <-> {b.get('id')}")
            lines.append(f"  {_kd_v1_short(b.get('content', ''), 160)}")

    if url_duplicates:
        lines.append("")
        lines.append("### URL Duplicates")
        for a, b, url in url_duplicates[:10]:
            lines.append(f"- {a.get('id')} <-> {b.get('id')}")
            lines.append(f"  URL: {url}")

    lines.append("")
    lines.append("Note: v1は削除せず、候補を表示するだけです。")

    return "\n".join(lines)


def _kd_v1_staleness(self) -> str:
    from datetime import datetime

    entries = _kd_v1_all_entries(self)

    if not entries:
        return "## Knowledge Staleness Check\n\n保存済み知識はまだありません。"

    now = datetime.now()
    oldish = []
    time_sensitive = []

    for entry in entries:
        content = str(entry.get("content", "")).lower()
        source = str(entry.get("source", "")).lower()
        category = str(entry.get("category", "")).lower()

        created = entry.get("created_at") or entry.get("updated_at") or ""
        age_days = None

        try:
            dt = datetime.fromisoformat(str(created).replace("Z", ""))
            age_days = (now - dt).days
        except Exception:
            pass

        is_time_sensitive = (
            category == "world"
            or "world_update" in source
            or "news" in content
            or "fetched_at" in content
            or "expires_at" in content
        )

        if is_time_sensitive:
            time_sensitive.append((age_days, entry))

        if age_days is not None and age_days >= 90:
            oldish.append((age_days, entry))

    lines = [
        "## Knowledge Staleness Check",
        "",
        f"Total Entries: {len(entries)}",
        f"Time-sensitive Entries: {len(time_sensitive)}",
        f"Old Entries 90+ days: {len(oldish)}",
        "",
        "### Time-sensitive Samples",
    ]

    if time_sensitive:
        for age_days, entry in time_sensitive[:10]:
            age_text = "unknown" if age_days is None else f"{age_days} days"
            lines.append(f"- [{entry.get('id')}] age={age_text} / {entry.get('category')} / {entry.get('source')}")
            lines.append(f"  {_kd_v1_short(entry.get('content', ''), 140)}")
    else:
        lines.append("- 時間で古くなりやすい知識は少なめです。")

    lines.append("")
    lines.append("### Old Entries")

    if oldish:
        for age_days, entry in oldish[:10]:
            lines.append(f"- [{entry.get('id')}] age={age_days} days / {entry.get('category')} / {entry.get('source')}")
    else:
        lines.append("- 90日以上古い知識は見つかりませんでした。")

    lines.append("")
    lines.append("Note: v1は古さの候補表示のみ。削除や更新はしません。")

    return "\n".join(lines)


def _kd_v1_maintenance(self) -> str:
    entries = _kd_v1_all_entries(self)

    if not entries:
        return "## Knowledge Maintenance\n\n保存済み知識はまだありません。"

    digest = _kd_v1_digest(self)
    duplicates = _kd_v1_duplicates(self)
    staleness = _kd_v1_staleness(self)

    lines = [
        "## Knowledge Maintenance",
        "",
        "### Quick Status",
        f"- Total Entries: {len(entries)}",
        "",
        "### Recommended Checks",
        "- 知識ダイジェスト: 全体量・カテゴリ・ソースを見る",
        "- 知識重複チェック: 同じ内容や同じURLの重複候補を見る",
        "- 知識古さチェック: world/news系の古さを見る",
        "",
        "### Digest Preview",
    ]

    # 長すぎないように一部だけ
    for line in digest.splitlines()[:28]:
        lines.append(line)

    lines.append("")
    lines.append("### Duplicate Preview")

    for line in duplicates.splitlines()[:16]:
        lines.append(line)

    lines.append("")
    lines.append("### Staleness Preview")

    for line in staleness.splitlines()[:18]:
        lines.append(line)

    return "\n".join(lines)


_kd_v1_can_handle_base = KnowledgeTool.can_handle
_kd_v1_execute_base = KnowledgeTool.execute

def _kd_v1_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()
    return (
        _kd_v1_can_handle_base(self, user_input)
        or text == "知識ダイジェスト"
        or text == "知識カテゴリ整理"
        or text == "知識重複チェック"
        or text == "知識古さチェック"
        or text == "知識メンテナンス"
    )


def _kd_v1_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text == "知識ダイジェスト":
        return _kd_v1_digest(self)

    if text == "知識カテゴリ整理":
        return _kd_v1_category整理(self)

    if text == "知識重複チェック":
        return _kd_v1_duplicates(self)

    if text == "知識古さチェック":
        return _kd_v1_staleness(self)

    if text == "知識メンテナンス":
        return _kd_v1_maintenance(self)

    return _kd_v1_execute_base(self, user_input)


KnowledgeTool.can_handle = _kd_v1_can_handle
KnowledgeTool.execute = _kd_v1_execute


# KNOWLEDGE_CLEANUP_V1_SAFE_PATCH

def _kc_v1_all_entries(self) -> list[dict]:
    try:
        return self.store.list_entries(limit=2000)
    except TypeError:
        return self.store.list_entries()


def _kc_v1_save_entries(self, entries: list[dict]) -> None:
    # KnowledgeStoreの内部保存先に直接保存する。
    # 既存構造を壊さないため、entries/list形式のみ扱う。
    import json

    path = getattr(self.store, "path", None)
    if path is None:
        path = getattr(self.store, "knowledge_path", None)
    if path is None:
        path = getattr(self.store, "file_path", None)

    if path is None:
        from pathlib import Path
        path = Path("data/knowledge/knowledge.json")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _kc_v1_short(content: str, limit: int = 180) -> str:
    content = str(content).replace("\n", " ").strip()
    if len(content) > limit:
        return content[:limit].rstrip() + "..."
    return content


def _kc_v1_find_entry(entries: list[dict], entry_id: str):
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry
    return None


def _kc_v1_candidates(self) -> str:
    entries = _kc_v1_all_entries(self)

    if not entries:
        return "## Knowledge Archive Candidates\n\n保存済み知識はまだありません。"

    active = [e for e in entries if not e.get("archived")]
    candidates = []

    # URL重複候補
    url_seen = {}

    for entry in active:
        content = str(entry.get("content", ""))
        urls = []

        for part in content.split():
            if part.startswith("http://") or part.startswith("https://"):
                urls.append(part.strip())

        for url in urls:
            if url in url_seen:
                candidates.append({
                    "reason": "URL重複",
                    "keep": url_seen[url],
                    "archive": entry,
                    "url": url,
                })
            else:
                url_seen[url] = entry

    # world_update_v2の重複候補。同じcategory=world/source=world_update_v2なら古い方を候補にする
    world_updates = [
        e for e in active
        if e.get("category") == "world" and e.get("source") == "world_update_v2"
    ]

    if len(world_updates) >= 2:
        sorted_world = sorted(world_updates, key=lambda e: str(e.get("created_at", "")), reverse=True)
        keep = sorted_world[0]
        for old in sorted_world[1:]:
            candidates.append({
                "reason": "world_update_v2の重複候補",
                "keep": keep,
                "archive": old,
                "url": "",
            })

    lines = [
        "## Knowledge Archive Candidates",
        "",
        f"Total Entries: {len(entries)}",
        f"Active Entries: {len(active)}",
        f"Candidates: {len(candidates)}",
        "",
    ]

    if not candidates:
        lines.append("アーカイブ候補は見つかりませんでした。")
        return "\n".join(lines)

    for item in candidates[:15]:
        keep = item["keep"]
        archive = item["archive"]

        lines.append(f"### Candidate: {archive.get('id')}")
        lines.append(f"- Reason: {item.get('reason')}")
        lines.append(f"- Keep: {keep.get('id')}")
        lines.append(f"- Archive Candidate: {archive.get('id')}")
        if item.get("url"):
            lines.append(f"- Duplicate URL: {item.get('url')}")
        lines.append(f"- Preview: {_kc_v1_short(archive.get('content', ''))}")
        lines.append(f"- Archive Command: 知識アーカイブ: {archive.get('id')}")
        lines.append("")

    lines.append("Note: v1は削除しません。archived=true を付けるだけです。")

    return "\n".join(lines).rstrip()


def _kc_v1_archive(self, entry_id: str) -> str:
    entry_id = entry_id.strip()

    if not entry_id:
        return "IDがありません。例: 知識アーカイブ: world-a40a20ca"

    entries = _kc_v1_all_entries(self)
    entry = _kc_v1_find_entry(entries, entry_id)

    if not entry:
        return f"知識IDが見つかりません: {entry_id}"

    if entry.get("archived"):
        return f"## Knowledge Archive\n\nすでにアーカイブ済みです: {entry_id}"

    from datetime import datetime

    entry["archived"] = True
    entry["archived_at"] = datetime.now().isoformat(timespec="seconds")
    entry["archive_reason"] = entry.get("archive_reason") or "manual"

    _kc_v1_save_entries(self, entries)

    return (
        "## Knowledge Archived\n\n"
        f"- ID: {entry.get('id')}\n"
        f"- Category: {entry.get('category')}\n"
        f"- Source: {entry.get('source')}\n"
        f"- Archived: true\n\n"
        "削除はしていません。復元する場合:\n"
        f"知識復元: {entry.get('id')}"
    )


def _kc_v1_archive_list(self) -> str:
    entries = _kc_v1_all_entries(self)
    archived = [e for e in entries if e.get("archived")]

    lines = [
        "## Knowledge Archive List",
        "",
        f"Archived Entries: {len(archived)}",
        "",
    ]

    if not archived:
        lines.append("アーカイブ済み知識はまだありません。")
        return "\n".join(lines)

    for entry in archived[:30]:
        lines.append(f"### {entry.get('id')}")
        lines.append(f"- Category: {entry.get('category')}")
        lines.append(f"- Source: {entry.get('source')}")
        lines.append(f"- Archived At: {entry.get('archived_at')}")
        lines.append(f"- Reason: {entry.get('archive_reason')}")
        lines.append(f"- Preview: {_kc_v1_short(entry.get('content', ''))}")
        lines.append(f"- Restore Command: 知識復元: {entry.get('id')}")
        lines.append("")

    return "\n".join(lines).rstrip()


def _kc_v1_restore(self, entry_id: str) -> str:
    entry_id = entry_id.strip()

    if not entry_id:
        return "IDがありません。例: 知識復元: world-a40a20ca"

    entries = _kc_v1_all_entries(self)
    entry = _kc_v1_find_entry(entries, entry_id)

    if not entry:
        return f"知識IDが見つかりません: {entry_id}"

    if not entry.get("archived"):
        return f"## Knowledge Restore\n\nこの知識はアーカイブされていません: {entry_id}"

    entry["archived"] = False
    entry["restored_at"] = __import__("datetime").datetime.now().isoformat(timespec="seconds")

    _kc_v1_save_entries(self, entries)

    return (
        "## Knowledge Restored\n\n"
        f"- ID: {entry.get('id')}\n"
        f"- Category: {entry.get('category')}\n"
        f"- Source: {entry.get('source')}\n"
        f"- Archived: false"
    )


_kc_v1_can_handle_base = KnowledgeTool.can_handle
_kc_v1_execute_base = KnowledgeTool.execute

def _kc_v1_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()
    return (
        _kc_v1_can_handle_base(self, user_input)
        or text == "知識アーカイブ候補"
        or text == "知識アーカイブ一覧"
        or text.startswith("知識アーカイブ:")
        or text.startswith("知識アーカイブ：")
        or text.startswith("知識復元:")
        or text.startswith("知識復元：")
    )


def _kc_v1_sep(text: str) -> str:
    for s in [":", "："]:
        if s in text:
            return text.split(s, 1)[1].strip()
    return ""


def _kc_v1_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text == "知識アーカイブ候補":
        return _kc_v1_candidates(self)

    if text == "知識アーカイブ一覧":
        return _kc_v1_archive_list(self)

    if text.startswith(("知識アーカイブ:", "知識アーカイブ：")):
        return _kc_v1_archive(self, _kc_v1_sep(text))

    if text.startswith(("知識復元:", "知識復元：")):
        return _kc_v1_restore(self, _kc_v1_sep(text))

    return _kc_v1_execute_base(self, user_input)


KnowledgeTool.can_handle = _kc_v1_can_handle
KnowledgeTool.execute = _kc_v1_execute


# ARCHIVE_FILTER_V1_SAFE_PATCH

def _af_v1_settings_path():
    from pathlib import Path
    return Path("data/knowledge/search_settings.json")


def _af_v1_load_settings() -> dict:
    import json

    path = _af_v1_settings_path()

    if not path.exists():
        return {
            "include_archived": False,
        }

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {
                "include_archived": bool(data.get("include_archived", False)),
            }
    except Exception:
        pass

    return {
        "include_archived": False,
    }


def _af_v1_save_settings(settings: dict) -> None:
    import json

    path = _af_v1_settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _af_v1_is_cleanup_command(text: str) -> bool:
    return (
        text == "知識アーカイブ候補"
        or text == "知識アーカイブ一覧"
        or text.startswith("知識アーカイブ:")
        or text.startswith("知識アーカイブ：")
        or text.startswith("知識復元:")
        or text.startswith("知識復元：")
    )


def _af_v1_filter_entries(entries: list[dict]) -> list[dict]:
    return [entry for entry in entries if not entry.get("archived")]


def _af_v1_settings_report() -> str:
    settings = _af_v1_load_settings()
    include_archived = settings.get("include_archived", False)

    mode = "アーカイブ込み" if include_archived else "アーカイブ除外"

    return (
        "## Knowledge Search Settings\n\n"
        f"- Current Mode: {mode}\n"
        f"- include_archived: {include_archived}\n\n"
        "Commands:\n"
        "- 知識検索アーカイブ含む\n"
        "- 知識検索アーカイブ除外\n\n"
        "Note:\n"
        "- 通常はアーカイブ除外がおすすめです。\n"
        "- アーカイブ済みを確認したい時だけ「含む」にしてください。"
    )


def _af_v1_include_archived() -> str:
    settings = _af_v1_load_settings()
    settings["include_archived"] = True
    _af_v1_save_settings(settings)

    return (
        "## Knowledge Search Settings Updated\n\n"
        "- Mode: アーカイブ込み\n"
        "- include_archived: true\n\n"
        "通常検索・横断検索・ダイジェストで archived=true も含めます。"
    )


def _af_v1_exclude_archived() -> str:
    settings = _af_v1_load_settings()
    settings["include_archived"] = False
    _af_v1_save_settings(settings)

    return (
        "## Knowledge Search Settings Updated\n\n"
        "- Mode: アーカイブ除外\n"
        "- include_archived: false\n\n"
        "通常検索・横断検索・ダイジェストで archived=true を除外します。"
    )


_af_v1_can_handle_base = KnowledgeTool.can_handle
_af_v1_execute_base = KnowledgeTool.execute

def _af_v1_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()

    return (
        _af_v1_can_handle_base(self, user_input)
        or text == "知識検索設定"
        or text == "知識検索アーカイブ含む"
        or text == "知識検索アーカイブ除外"
    )


def _af_v1_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text == "知識検索設定":
        return _af_v1_settings_report()

    if text == "知識検索アーカイブ含む":
        return _af_v1_include_archived()

    if text == "知識検索アーカイブ除外":
        return _af_v1_exclude_archived()

    settings = _af_v1_load_settings()

    # アーカイブ管理コマンドは、必ず全件を見られるようにする。
    if settings.get("include_archived", False) or _af_v1_is_cleanup_command(text):
        return _af_v1_execute_base(self, user_input)

    store = self.store

    original_list_entries = getattr(store, "list_entries", None)
    original_search = getattr(store, "search", None)

    def filtered_list_entries(*args, **kwargs):
        if original_list_entries is None:
            return []

        entries = original_list_entries(*args, **kwargs)

        if isinstance(entries, list):
            return _af_v1_filter_entries(entries)

        return entries

    def filtered_search(*args, **kwargs):
        if original_search is None:
            return []

        results = original_search(*args, **kwargs)

        if isinstance(results, list):
            return _af_v1_filter_entries(results)

        return results

    try:
        if original_list_entries is not None:
            store.list_entries = filtered_list_entries

        if original_search is not None:
            store.search = filtered_search

        return _af_v1_execute_base(self, user_input)

    finally:
        if original_list_entries is not None:
            store.list_entries = original_list_entries

        if original_search is not None:
            store.search = original_search


KnowledgeTool.can_handle = _af_v1_can_handle
KnowledgeTool.execute = _af_v1_execute


# SOURCE_TRUST_V1_SAFE_PATCH

def _st_v1_all_entries(self) -> list[dict]:
    try:
        return self.store.list_entries(limit=2000)
    except TypeError:
        return self.store.list_entries()


def _st_v1_sep(text: str) -> str:
    for s in [":", "："]:
        if s in text:
            return text.split(s, 1)[1].strip()
    return ""


def _st_v1_short(content: str, limit: int = 180) -> str:
    content = str(content).replace("\n", " ").strip()
    if len(content) > limit:
        return content[:limit].rstrip() + "..."
    return content


def _st_v1_score_entry(entry: dict) -> dict:
    source = str(entry.get("source", "")).lower()
    category = str(entry.get("category", "")).lower()
    content = str(entry.get("content", "")).lower()
    tags = " ".join(entry.get("tags", [])).lower()

    text = f"{source} {category} {content} {tags}"

    score = 50
    reasons = []
    cautions = []

    # 高信頼寄り
    if "official" in text or "公式" in text:
        score += 20
        reasons.append("公式/officialらしさ")

    if source in {"arxiv"} or "arxiv" in source:
        score += 12
        reasons.append("arXiv由来")
        cautions.append("arXivは有用だが査読済みとは限らない")

    if "pubmed" in text or "pmc" in text:
        score += 18
        reasons.append("研究・論文系データベース")

    if "python docs" in text or "python.org" in text:
        score += 22
        reasons.append("Python公式系")

    if "autodesk" in text or "blender manual" in text or "docs.blender.org" in text:
        score += 20
        reasons.append("3DCG公式ドキュメント系")

    if "github" in text and "blog" not in text:
        score += 10
        reasons.append("開発系ソース")

    # 補助情報扱い
    if "world_update_v2" in source or "world_update" in text:
        score -= 12
        cautions.append("world_update由来。ニュース要約なので補助情報扱い")

    if "google news" in text or "news.google" in text:
        score -= 15
        cautions.append("Google News経由。元記事確認が必要")

    if source in {"user", "manual", ""}:
        score -= 5
        cautions.append("ユーザー/手動追加知識。根拠確認が必要")

    if category == "world":
        score -= 8
        cautions.append("社会情勢系。古くなる可能性が高い")

    if entry.get("archived"):
        score -= 20
        cautions.append("アーカイブ済み")

    if "license" not in text and category in {"papers", "3dcg", "development"}:
        cautions.append("ライセンス情報は未確認")

    score = max(0, min(100, score))

    if score >= 80:
        label = "high"
    elif score >= 60:
        label = "medium"
    elif score >= 40:
        label = "low-medium"
    else:
        label = "low"

    return {
        "score": score,
        "label": label,
        "reasons": list(dict.fromkeys(reasons)),
        "cautions": list(dict.fromkeys(cautions)),
    }


def _st_v1_source_list(self) -> str:
    entries = _st_v1_all_entries(self)

    if not entries:
        return "## Source Trust List\n\n保存済み知識はまだありません。"

    source_data = {}

    for entry in entries:
        source = entry.get("source", "unknown")
        result = _st_v1_score_entry(entry)

        if source not in source_data:
            source_data[source] = {
                "count": 0,
                "scores": [],
                "labels": {},
                "reasons": {},
                "cautions": {},
            }

        data = source_data[source]
        data["count"] += 1
        data["scores"].append(result["score"])
        data["labels"][result["label"]] = data["labels"].get(result["label"], 0) + 1

        for reason in result["reasons"]:
            data["reasons"][reason] = data["reasons"].get(reason, 0) + 1

        for caution in result["cautions"]:
            data["cautions"][caution] = data["cautions"].get(caution, 0) + 1

    lines = [
        "## Source Trust List",
        "",
        f"Sources: {len(source_data)}",
        "",
    ]

    ranked = []

    for source, data in source_data.items():
        avg = round(sum(data["scores"]) / max(len(data["scores"]), 1), 1)
        ranked.append((avg, source, data))

    ranked.sort(key=lambda x: (-x[0], x[1]))

    for avg, source, data in ranked:
        lines.append(f"### {source}")
        lines.append(f"- Entries: {data['count']}")
        lines.append(f"- Average Trust Score: {avg}/100")
        lines.append(f"- Labels: {data['labels']}")

        reasons = sorted(data["reasons"].items(), key=lambda x: (-x[1], x[0]))[:5]
        cautions = sorted(data["cautions"].items(), key=lambda x: (-x[1], x[0]))[:5]

        if reasons:
            lines.append("- Reasons:")
            for reason, count in reasons:
                lines.append(f"  - {reason}: {count}")

        if cautions:
            lines.append("- Cautions:")
            for caution, count in cautions:
                lines.append(f"  - {caution}: {count}")

        lines.append("")

    return "\n".join(lines).rstrip()


def _st_v1_check_all(self) -> str:
    entries = _st_v1_all_entries(self)

    if not entries:
        return "## Source Trust Check\n\n保存済み知識はまだありません。"

    scored = []

    for entry in entries:
        result = _st_v1_score_entry(entry)
        scored.append((result["score"], result, entry))

    scored.sort(key=lambda x: x[0])

    low = [x for x in scored if x[0] < 60]
    high = [x for x in scored if x[0] >= 80]

    lines = [
        "## Source Trust Check",
        "",
        f"Total Entries: {len(entries)}",
        f"High Trust 80+: {len(high)}",
        f"Needs Caution <60: {len(low)}",
        "",
        "### Needs Caution",
    ]

    if low:
        for score, result, entry in low[:12]:
            lines.append(f"#### {entry.get('id')}")
            lines.append(f"- Trust: {score}/100 ({result['label']})")
            lines.append(f"- Category: {entry.get('category')}")
            lines.append(f"- Source: {entry.get('source')}")
            lines.append(f"- Cautions: {', '.join(result['cautions']) if result['cautions'] else 'なし'}")
            lines.append(f"- Preview: {_st_v1_short(entry.get('content', ''))}")
            lines.append("")
    else:
        lines.append("- 注意度が高い知識は見つかりませんでした。")

    lines.append("")
    lines.append("### High Trust Samples")

    if high:
        for score, result, entry in sorted(high, key=lambda x: -x[0])[:8]:
            lines.append(f"- [{score}/100] {entry.get('id')} / {entry.get('source')} / {entry.get('category')}")
    else:
        lines.append("- high扱いの知識はまだ少なめです。")

    lines.append("")
    lines.append("Note: v1はヒューリスティック評価です。最終判断には原文・公式情報確認が必要です。")

    return "\n".join(lines)


def _st_v1_confirm(self, query: str) -> str:
    query = query.strip()

    if not query:
        return "検索語またはIDがありません。例: 知識信頼度確認: diffusion"

    entries = _st_v1_all_entries(self)

    target = None
    for entry in entries:
        if entry.get("id") == query:
            target = entry
            break

    if target:
        targets = [target]
        title = f"Knowledge Trust / {query}"
    else:
        q = query.lower()
        targets = []

        for entry in entries:
            text = " ".join([
                str(entry.get("id", "")),
                str(entry.get("category", "")),
                str(entry.get("source", "")),
                str(entry.get("content", "")),
                " ".join(entry.get("tags", [])),
            ]).lower()

            if q in text:
                targets.append(entry)

        title = f"Knowledge Trust Search / {query}"

    if not targets:
        return f"## {title}\n\n該当する知識が見つかりませんでした。"

    lines = [
        f"## {title}",
        "",
        f"Matched Entries: {len(targets)}",
        "",
    ]

    scored = []
    for entry in targets:
        result = _st_v1_score_entry(entry)
        scored.append((result["score"], result, entry))

    scored.sort(key=lambda x: -x[0])

    for score, result, entry in scored[:12]:
        lines.append(f"### {entry.get('id')}")
        lines.append(f"- Trust Score: {score}/100")
        lines.append(f"- Trust Label: {result['label']}")
        lines.append(f"- Category: {entry.get('category')}")
        lines.append(f"- Source: {entry.get('source')}")
        lines.append(f"- Reasons: {', '.join(result['reasons']) if result['reasons'] else 'なし'}")
        lines.append(f"- Cautions: {', '.join(result['cautions']) if result['cautions'] else 'なし'}")
        lines.append(f"- Preview: {_st_v1_short(entry.get('content', ''))}")
        lines.append("")

    lines.append("Note: 信頼度は目安です。重要な判断には一次情報・公式情報を確認してください。")

    return "\n".join(lines).rstrip()


_st_v1_can_handle_base = KnowledgeTool.can_handle
_st_v1_execute_base = KnowledgeTool.execute

def _st_v1_can_handle(self, user_input: str) -> bool:
    text = user_input.strip()
    return (
        _st_v1_can_handle_base(self, user_input)
        or text == "情報源信頼度一覧"
        or text == "情報源信頼度チェック"
        or text.startswith("知識信頼度確認:")
        or text.startswith("知識信頼度確認：")
    )


def _st_v1_execute(self, user_input: str) -> str:
    text = user_input.strip()

    if text == "情報源信頼度一覧":
        return _st_v1_source_list(self)

    if text == "情報源信頼度チェック":
        return _st_v1_check_all(self)

    if text.startswith(("知識信頼度確認:", "知識信頼度確認：")):
        return _st_v1_confirm(self, _st_v1_sep(text))

    return _st_v1_execute_base(self, user_input)


KnowledgeTool.can_handle = _st_v1_can_handle
KnowledgeTool.execute = _st_v1_execute
