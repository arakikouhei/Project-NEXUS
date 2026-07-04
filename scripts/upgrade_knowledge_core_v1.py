from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "knowledge_core_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path_text: str) -> None:
    path = ROOT / path_text
    if not path.exists():
        return

    target = BACKUP_DIR / path_text
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def write(path_text: str, content: str) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def write_knowledge_store() -> None:
    write(
        "nexus/memory/knowledge_store.py",
        r'''
        """
        Project NEXUS
        Knowledge Store v1

        Stores categorized knowledge entries locally.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from datetime import datetime
        from pathlib import Path
        import json
        import re
        import uuid


        @dataclass(frozen=True)
        class KnowledgeEntry:
            id: str
            category: str
            content: str
            created_at: str
            updated_at: str
            source: str
            tags: list[str]


        class KnowledgeStore:
            """Simple local knowledge base."""

            def __init__(self, path: str = "data/knowledge/knowledge.json") -> None:
                self.path = Path(path)
                self.allowed_categories = {
                    "general": "一般知識・雑学・文化・歴史・科学",
                    "world": "社会情勢・ニュース・時事",
                    "papers": "安全な論文メタ情報・要約",
                    "3dcg": "Maya / Blender / Mudbox / UV / モデリング / レンダリング",
                    "programming": "Python / Git / API / アルゴリズム",
                    "development": "設計 / セキュリティ / テスト / AI開発",
                    "source_registry": "信頼できる情報源リスト",
                }

            def add(
                self,
                category: str,
                content: str,
                source: str = "manual",
                tags: list[str] | None = None,
            ) -> dict:
                category = self.normalize_category(category)

                if category not in self.allowed_categories:
                    raise ValueError(f"unknown category: {category}")

                now = datetime.now().isoformat(timespec="seconds")
                entry = {
                    "id": self._new_id(category),
                    "category": category,
                    "content": content.strip(),
                    "created_at": now,
                    "updated_at": now,
                    "source": source,
                    "tags": tags or self._auto_tags(content),
                }

                records = self._load()
                records.append(entry)
                self._save(records)

                return entry

            def search(self, query: str, limit: int = 10) -> list[dict]:
                query = query.strip()
                if not query:
                    return []

                records = self._load()
                scored = []

                q_key = self._key(query)
                query_terms = [self._key(term) for term in query.split() if term.strip()]

                for item in records:
                    content = item.get("content", "")
                    category = item.get("category", "")
                    tags = " ".join(item.get("tags", []))
                    haystack = self._key(" ".join([content, category, tags]))

                    score = 0

                    if q_key in haystack:
                        score += 10

                    for term in query_terms:
                        if term and term in haystack:
                            score += 4

                    # 日本語やスペースなし検索用。文字単位でざっくり一致。
                    if score == 0:
                        overlap = len(set(q_key) & set(haystack))
                        score += min(3, overlap // 2)

                    if score > 0:
                        scored.append((score, item))

                scored.sort(key=lambda pair: pair[0], reverse=True)
                return [item for score, item in scored[:limit]]

            def list_entries(self, category: str | None = None, limit: int = 20) -> list[dict]:
                records = self._load()

                if category:
                    category = self.normalize_category(category)
                    records = [item for item in records if item.get("category") == category]

                return list(reversed(records[-limit:]))

            def get(self, entry_id: str) -> dict | None:
                for item in self._load():
                    if item.get("id") == entry_id:
                        return item
                return None

            def categories(self) -> dict[str, str]:
                return dict(self.allowed_categories)

            def normalize_category(self, category: str) -> str:
                text = category.strip().lower()

                aliases = {
                    "一般": "general",
                    "常識": "general",
                    "一般常識": "general",
                    "雑学": "general",
                    "社会": "world",
                    "社会情勢": "world",
                    "ニュース": "world",
                    "時事": "world",
                    "論文": "papers",
                    "paper": "papers",
                    "papers": "papers",
                    "3d": "3dcg",
                    "cg": "3dcg",
                    "maya": "3dcg",
                    "blender": "3dcg",
                    "mudbox": "3dcg",
                    "プログラミング": "programming",
                    "program": "programming",
                    "code": "programming",
                    "コード": "programming",
                    "python": "programming",
                    "開発": "development",
                    "dev": "development",
                    "development": "development",
                    "設計": "development",
                    "情報源": "source_registry",
                    "ソース": "source_registry",
                    "source": "source_registry",
                }

                return aliases.get(text, text)

            def _load(self) -> list[dict]:
                if not self.path.exists():
                    return []

                try:
                    data = json.loads(self.path.read_text(encoding="utf-8"))
                    if isinstance(data, list):
                        return data
                    return []
                except Exception:
                    return []

            def _save(self, records: list[dict]) -> None:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.write_text(
                    json.dumps(records, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

            def _new_id(self, category: str) -> str:
                short = uuid.uuid4().hex[:8]
                return f"{category}-{short}"

            def _auto_tags(self, content: str) -> list[str]:
                words = re.findall(r"[A-Za-z][A-Za-z0-9_+\-.#]*|[一-龥ぁ-んァ-ン]{2,}", content)
                tags = []

                for word in words:
                    if word not in tags:
                        tags.append(word)

                    if len(tags) >= 12:
                        break

                return tags

            def _key(self, text: str) -> str:
                return (
                    text.lower()
                    .replace(" ", "")
                    .replace("　", "")
                    .replace("\n", "")
                    .replace("\t", "")
                )
        ''',
    )


def write_knowledge_tool() -> None:
    write(
        "nexus/tools/knowledge.py",
        r'''
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
        ''',
    )


def patch_manager() -> None:
    path = ROOT / "nexus/tools/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.tools.knowledge import KnowledgeTool" not in text:
        text = text.replace(
            "from nexus.tools.vision_memory import VisionMemoryTool\n",
            "from nexus.tools.vision_memory import VisionMemoryTool\n"
            "from nexus.tools.knowledge import KnowledgeTool\n",
            1,
        )

    if "self.register(KnowledgeTool())" not in text:
        text = text.replace(
            "        self.register(VisionMemoryTool())\n",
            "        self.register(VisionMemoryTool())\n"
            "        self.register(KnowledgeTool())\n",
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"知識ヘルプ"' not in text:
        text = text.replace(
            '                    "前回画像分析: tests/assets/sample_vision.png",\n',
            '                    "前回画像分析: tests/assets/sample_vision.png",\n'
            '                    "知識ヘルプ",\n'
            '                    "知識検索: Maya UV",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        path.write_text("あなたは Project NEXUS です。\n", encoding="utf-8")

    text = path.read_text(encoding="utf-8")
    marker = "# Knowledge Core v1"

    if marker in text:
        return

    addition = """

# Knowledge Core v1

NEXUSはローカル知識ベースを持ちます。

使える例:
- 知識ヘルプ
- 知識カテゴリ
- 知識追加: 3dcg | MayaのUVは3Dモデル表面を2D座標に展開する仕組み。
- 知識検索: Maya UV
- 知識一覧
- 知識一覧: 3dcg
- 知識詳細: 3dcg-xxxxxxxx

方針:
- 知らないことを知ったふりしない
- 専門知識・論文・社会情勢は出典や日時を重視する
- 古くなる情報はworldカテゴリやsource_registryで管理する
- 論文は安全なオープンアクセスや公式APIから段階的に扱う
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/KNOWLEDGE_CORE_V1.md",
        """
        # Knowledge Core v1

        Local categorized knowledge base for Project NEXUS.

        ## Commands

        - 知識ヘルプ
        - 知識カテゴリ
        - 知識追加: 3dcg | MayaのUVは3Dモデル表面を2D座標に展開する仕組み。
        - 知識検索: Maya UV
        - 知識一覧
        - 知識一覧: 3dcg
        - 知識詳細: 3dcg-xxxxxxxx

        ## Categories

        - general
        - world
        - papers
        - 3dcg
        - programming
        - development
        - source_registry

        ## Storage

        - data/knowledge/knowledge.json

        ## Next

        - Source Registry
        - World Update
        - Paper Intake
        - Knowledge RAG
        """,
    )


def seed_initial_knowledge() -> None:
    from nexus.memory.knowledge_store import KnowledgeStore

    store = KnowledgeStore()

    if store.list_entries(limit=1):
        return

    seeds = [
        (
            "3dcg",
            "MayaのUVは、3Dモデルの表面を2D座標に展開して、テクスチャを貼るための仕組み。",
        ),
        (
            "programming",
            "Gitは変更履歴を管理するバージョン管理システム。commitで履歴を作り、pushでリモートへ送る。",
        ),
        (
            "development",
            "安全なローカルAI開発では、危険なコマンド実行を制限し、ログ・バックアップ・Git管理を組み合わせる。",
        ),
        (
            "papers",
            "論文知識は、安全なオープンアクセス、公式API、ライセンス確認済みソースから段階的に取り込む。",
        ),
        (
            "world",
            "社会情勢やニュースは古くなるため、取得日時・情報源・有効期限を持たせて管理する必要がある。",
        ),
    ]

    for category, content in seeds:
        store.add(category=category, content=content, source="seed")


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/memory/knowledge_store.py",
        "nexus/tools/knowledge.py",
        "nexus/tools/manager.py",
        "nexus/tools/diagnostics.py",
        "prompts/system_prompt.txt",
    ]:
        backup(target)

    write_knowledge_store()
    write_knowledge_tool()
    patch_manager()
    patch_diagnostics()
    patch_system_prompt()
    write_docs()
    seed_initial_knowledge()

    print("Knowledge Core v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
