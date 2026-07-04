from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import shutil
import textwrap
import uuid


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "source_registry_v1" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def write_source_store() -> None:
    write(
        "nexus/memory/source_registry.py",
        r'''
        """
        Project NEXUS
        Source Registry Store v1

        Stores trusted or semi-trusted information sources.
        """

        from __future__ import annotations

        from datetime import datetime
        from pathlib import Path
        import json
        import uuid


        class SourceRegistryStore:
            """Local registry for information sources."""

            def __init__(self, path: str = "data/knowledge/source_registry.json") -> None:
                self.path = Path(path)
                self.allowed_categories = {
                    "general": "一般知識・辞典・百科事典",
                    "world": "社会情勢・ニュース・時事",
                    "papers": "論文・研究・学術情報",
                    "3dcg": "3DCG・DCCツール・CG制作",
                    "programming": "プログラミング・公式ドキュメント",
                    "development": "開発・設計・セキュリティ",
                    "official": "企業・大学・団体などの公式サイト",
                }

            def add(
                self,
                category: str,
                name: str,
                url: str,
                note: str = "",
                trust_level: str = "medium",
            ) -> dict:
                category = self.normalize_category(category)
                trust_level = self.normalize_trust_level(trust_level)

                if category not in self.allowed_categories:
                    raise ValueError(f"unknown category: {category}")

                if not self._looks_like_url(url):
                    raise ValueError("URLの形式が正しくありません。http:// または https:// で始めてください。")

                records = self._load()
                now = datetime.now().isoformat(timespec="seconds")

                # 同じURLは重複登録しない
                for item in records:
                    if item.get("url") == url:
                        item["updated_at"] = now
                        item["category"] = category
                        item["name"] = name.strip()
                        item["note"] = note.strip()
                        item["trust_level"] = trust_level
                        self._save(records)
                        return item

                entry = {
                    "id": self._new_id(category),
                    "category": category,
                    "name": name.strip(),
                    "url": url.strip(),
                    "note": note.strip(),
                    "trust_level": trust_level,
                    "created_at": now,
                    "updated_at": now,
                    "status": "active",
                }

                records.append(entry)
                self._save(records)
                return entry

            def search(self, query: str, limit: int = 10) -> list[dict]:
                query = query.strip()
                if not query:
                    return []

                records = self._load()
                q_key = self._key(query)
                results = []

                for item in records:
                    haystack = self._key(
                        " ".join(
                            [
                                item.get("category", ""),
                                item.get("name", ""),
                                item.get("url", ""),
                                item.get("note", ""),
                                item.get("trust_level", ""),
                            ]
                        )
                    )

                    score = 0

                    if q_key in haystack:
                        score += 10

                    for term in query.split():
                        if self._key(term) in haystack:
                            score += 4

                    if score > 0:
                        results.append((score, item))

                results.sort(key=lambda pair: pair[0], reverse=True)
                return [item for score, item in results[:limit]]

            def list_sources(self, category: str | None = None, limit: int = 50) -> list[dict]:
                records = self._load()

                if category:
                    normalized = self.normalize_category(category)
                    records = [item for item in records if item.get("category") == normalized]

                return list(reversed(records[-limit:]))

            def get(self, source_id: str) -> dict | None:
                for item in self._load():
                    if item.get("id") == source_id:
                        return item
                return None

            def categories(self) -> dict[str, str]:
                return dict(self.allowed_categories)

            def normalize_category(self, category: str) -> str:
                text = category.strip().lower()

                aliases = {
                    "一般": "general",
                    "常識": "general",
                    "辞典": "general",
                    "社会": "world",
                    "社会情勢": "world",
                    "ニュース": "world",
                    "時事": "world",
                    "論文": "papers",
                    "paper": "papers",
                    "papers": "papers",
                    "研究": "papers",
                    "学術": "papers",
                    "3d": "3dcg",
                    "cg": "3dcg",
                    "3dcg": "3dcg",
                    "maya": "3dcg",
                    "blender": "3dcg",
                    "プログラミング": "programming",
                    "programming": "programming",
                    "python": "programming",
                    "コード": "programming",
                    "開発": "development",
                    "dev": "development",
                    "development": "development",
                    "設計": "development",
                    "セキュリティ": "development",
                    "公式": "official",
                    "official": "official",
                }

                return aliases.get(text, text)

            def normalize_trust_level(self, trust_level: str) -> str:
                text = trust_level.strip().lower()

                aliases = {
                    "高": "high",
                    "高い": "high",
                    "公式": "high",
                    "中": "medium",
                    "普通": "medium",
                    "低": "low",
                    "低い": "low",
                }

                text = aliases.get(text, text)

                if text not in {"high", "medium", "low"}:
                    return "medium"

                return text

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
                return f"source-{category}-{uuid.uuid4().hex[:8]}"

            def _looks_like_url(self, url: str) -> bool:
                lowered = url.strip().lower()
                return lowered.startswith("https://") or lowered.startswith("http://")

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


def write_source_tool() -> None:
    write(
        "nexus/tools/source_registry.py",
        r'''
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
        ''',
    )


def patch_manager() -> None:
    path = ROOT / "nexus/tools/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.tools.source_registry import SourceRegistryTool" not in text:
        text = text.replace(
            "from nexus.tools.knowledge import KnowledgeTool\n",
            "from nexus.tools.knowledge import KnowledgeTool\n"
            "from nexus.tools.source_registry import SourceRegistryTool\n",
            1,
        )

    if "self.register(SourceRegistryTool())" not in text:
        text = text.replace(
            "        self.register(KnowledgeTool())\n",
            "        self.register(KnowledgeTool())\n"
            "        self.register(SourceRegistryTool())\n",
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_agent_bypass() -> None:
    path = ROOT / "nexus/agent/agent.py"
    text = path.read_text(encoding="utf-8")

    if "# SOURCE_REGISTRY_ROUTING_BYPASS_V1" in text:
        return

    target = '''        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)
'''

    insert = '''        # SOURCE_REGISTRY_ROUTING_BYPASS_V1
        # 情報源系コマンドはInputNormalizerより前に専用ツールへ渡す。
        source_prefixes = (
            "情報源ヘルプ",
            "情報源カテゴリ",
            "情報源一覧",
            "情報源追加:",
            "情報源追加：",
            "情報源検索:",
            "情報源検索：",
            "情報源詳細:",
            "情報源詳細：",
        )

        if stripped_input.startswith(source_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)
'''

    if target not in text:
        # Knowledge bypassがある場合は、その後に追加されていて target が1回だけ残っている想定。
        raise SystemExit("agent.py の挿入位置が見つかりません。")

    text = text.replace(target, insert, 1)
    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"情報源ヘルプ"' not in text:
        text = text.replace(
            '                    "知識検索: Maya UV",\n',
            '                    "知識検索: Maya UV",\n'
            '                    "情報源ヘルプ",\n'
            '                    "情報源検索: arXiv",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def seed_sources() -> None:
    from nexus.memory.source_registry import SourceRegistryStore

    store = SourceRegistryStore()

    seeds = [
        ("papers", "arXiv", "https://arxiv.org/", "論文・プレプリント。CS/AI/数学/物理などの調査入口。", "high"),
        ("papers", "PubMed", "https://pubmed.ncbi.nlm.nih.gov/", "医学・生命科学系の論文検索入口。", "high"),
        ("papers", "PubMed Central", "https://pmc.ncbi.nlm.nih.gov/", "無料全文が読める生命科学系論文の入口。", "high"),
        ("papers", "Semantic Scholar", "https://www.semanticscholar.org/", "論文・著者・引用関係の調査入口。", "medium"),
        ("programming", "Python Docs", "https://docs.python.org/3/", "Python公式ドキュメント。", "high"),
        ("programming", "Git Documentation", "https://git-scm.com/doc", "Git公式ドキュメント。", "high"),
        ("3dcg", "Autodesk Maya Help", "https://help.autodesk.com/view/MAYAUL/2026/ENU/", "Autodesk Maya公式ヘルプ。", "high"),
        ("3dcg", "Blender Manual", "https://docs.blender.org/manual/en/latest/", "Blender公式マニュアル。", "high"),
        ("development", "OWASP", "https://owasp.org/", "Web/アプリケーションセキュリティの代表的な情報源。", "high"),
    ]

    for category, name, url, note, trust in seeds:
        store.add(category=category, name=name, url=url, note=note, trust_level=trust)


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        path.write_text("あなたは Project NEXUS です。\n", encoding="utf-8")

    text = path.read_text(encoding="utf-8")
    marker = "# Source Registry v1"

    if marker in text:
        return

    addition = """

# Source Registry v1

NEXUSは信頼できる情報源をローカルに登録・検索できます。

使える例:
- 情報源ヘルプ
- 情報源カテゴリ
- 情報源追加: papers | arXiv | https://arxiv.org/ | オープンアクセス論文・プレプリント | high
- 情報源検索: arXiv
- 情報源一覧
- 情報源一覧: papers
- 情報源詳細: source-papers-xxxxxxxx

方針:
- 社会情勢や論文更新は、登録済みの情報源を優先する
- highでも100%正しいとは扱わず、必要に応じて複数ソースで確認する
- ニュースや時事情報は取得日時と情報源を残す
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/SOURCE_REGISTRY_V1.md",
        """
        # Source Registry v1

        Local registry of trusted information sources.

        ## Commands

        - 情報源ヘルプ
        - 情報源カテゴリ
        - 情報源追加: papers | arXiv | https://arxiv.org/ | Open access papers | high
        - 情報源検索: arXiv
        - 情報源一覧
        - 情報源一覧: papers
        - 情報源詳細: source-papers-xxxxxxxx

        ## Storage

        - data/knowledge/source_registry.json

        ## Next

        - World Update v1
        - Paper Intake v1
        - Knowledge RAG v1
        """,
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/memory/source_registry.py",
        "nexus/tools/source_registry.py",
        "nexus/tools/manager.py",
        "nexus/agent/agent.py",
        "nexus/tools/diagnostics.py",
        "prompts/system_prompt.txt",
    ]:
        backup(target)

    write_source_store()
    write_source_tool()
    patch_manager()
    patch_agent_bypass()
    patch_diagnostics()
    patch_system_prompt()
    write_docs()
    seed_sources()

    print("Source Registry v1 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
