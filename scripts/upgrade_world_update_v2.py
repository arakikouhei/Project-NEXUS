from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "world_update_v2" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def patch_world_update_tool() -> None:
    path = ROOT / "nexus/tools/world_update.py"
    text = path.read_text(encoding="utf-8")

    if "# WORLD_UPDATE_V2" in text:
        print("world_update.py already patched")
        return

    # can_handle に v2 コマンド追加
    text = text.replace(
        '                    or text.startswith("更新ソース追加:")\n'
        '                    or text.startswith("更新ソース追加：")\n',
        '                    or text.startswith("更新ソース追加:")\n'
        '                    or text.startswith("更新ソース追加：")\n'
        '                    or text.startswith("更新整理:")\n'
        '                    or text.startswith("更新整理：")\n'
        '                    or text.startswith("更新重要度:")\n'
        '                    or text.startswith("更新重要度：")\n'
        '                    or text.startswith("更新知識化:")\n'
        '                    or text.startswith("更新知識化：")\n',
        1,
    )

    # execute に v2 分岐追加
    text = text.replace(
        '                if text.startswith(("更新ソース追加:", "更新ソース追加：")):\n'
        '                    body = self._after_separator(text)\n'
        '                    return self._add_source(body)\n\n'
        '                mapping = {\n',
        '                if text.startswith(("更新ソース追加:", "更新ソース追加：")):\n'
        '                    body = self._after_separator(text)\n'
        '                    return self._add_source(body)\n\n'
        '                if text.startswith(("更新整理:", "更新整理：")):\n'
        '                    category = self._after_separator(text)\n'
        '                    return self._organize(category)\n\n'
        '                if text.startswith(("更新重要度:", "更新重要度：")):\n'
        '                    category = self._after_separator(text)\n'
        '                    return self._importance(category)\n\n'
        '                if text.startswith(("更新知識化:", "更新知識化：")):\n'
        '                    category = self._after_separator(text)\n'
        '                    return self._save_digest_to_knowledge(category)\n\n'
        '                mapping = {\n',
        1,
    )

    # _help 前にv2メソッドを追加
    marker = "            def _help(self) -> str:\n"
    methods = r'''
            # WORLD_UPDATE_V2
            def _organize(self, category: str) -> str:
                category = category.strip() or None
                logs = self.store.recent(category=category, limit=30)

                title = "## Organized Updates"
                if category:
                    title += f" / {category}"

                if not logs:
                    return title + "\n\n整理できる更新ログがありません。"

                scored = [(self._score_update(item), item) for item in logs]
                scored.sort(key=lambda pair: pair[0]["score"], reverse=True)

                groups = self._group_updates([item for score, item in scored])

                lines = [title, ""]

                lines.append("### Top Updates")
                for score_data, item in scored[:8]:
                    lines.append(f"- [{score_data['score']}/100] {item.get('title')}")
                    lines.append(f"  - Category: {item.get('category')}")
                    lines.append(f"  - Source: {item.get('source_name')}")
                    lines.append(f"  - Reason: {', '.join(score_data['reasons']) if score_data['reasons'] else '特になし'}")
                    lines.append(f"  - URL: {item.get('link')}")

                lines.append("")
                lines.append("### Topic Groups")

                for key, items in groups.items():
                    lines.append(f"- {key}: {len(items)}件")
                    for item in items[:3]:
                        lines.append(f"  - {item.get('title')}")

                lines.append("")
                lines.append("Notes:")
                lines.append("- v2は見出し・要約ベースの簡易整理です。")
                lines.append("- 重要度は確定評価ではありません。")
                lines.append("- 判断が必要な内容は複数ソース確認が必要です。")

                return "\n".join(lines).rstrip()

            def _importance(self, category: str) -> str:
                category = category.strip() or None
                logs = self.store.recent(category=category, limit=30)

                title = "## Update Importance"
                if category:
                    title += f" / {category}"

                if not logs:
                    return title + "\n\n評価できる更新ログがありません。"

                scored = [(self._score_update(item), item) for item in logs]
                scored.sort(key=lambda pair: pair[0]["score"], reverse=True)

                lines = [title, ""]

                for score_data, item in scored[:15]:
                    lines.append(f"### {score_data['score']}/100 - {item.get('title')}")
                    lines.append(f"- Category: {item.get('category')}")
                    lines.append(f"- Source: {item.get('source_name')}")
                    lines.append(f"- Published: {item.get('published')}")
                    lines.append(f"- Reasons: {', '.join(score_data['reasons']) if score_data['reasons'] else '特になし'}")
                    if score_data["penalties"]:
                        lines.append(f"- Penalties: {', '.join(score_data['penalties'])}")
                    lines.append(f"- URL: {item.get('link')}")
                    lines.append("")

                return "\n".join(lines).rstrip()

            def _save_digest_to_knowledge(self, category: str) -> str:
                category = category.strip() or None
                logs = self.store.recent(category=category, limit=30)

                if not logs:
                    return "## Update Digest\n\n知識化できる更新ログがありません。"

                scored = [(self._score_update(item), item) for item in logs]
                scored.sort(key=lambda pair: pair[0]["score"], reverse=True)

                top_items = scored[:8]
                groups = self._group_updates([item for score, item in top_items])

                now = __import__("datetime").datetime.now().isoformat(timespec="seconds")

                lines = []
                lines.append(f"更新ダイジェスト category={category or 'all'} fetched_at={now}")
                lines.append("")
                lines.append("重要そうな更新:")

                for score_data, item in top_items:
                    lines.append(f"- [{score_data['score']}/100] {item.get('title')} / {item.get('source_name')}")
                    lines.append(f"  URL: {item.get('link')}")

                lines.append("")
                lines.append("話題グループ:")

                for key, items in groups.items():
                    lines.append(f"- {key}: {len(items)}件")

                lines.append("")
                lines.append("注意: RSS見出しベースの要約。重要な判断には複数ソース確認が必要。")

                content = "\n".join(lines)

                try:
                    from nexus.memory.knowledge_store import KnowledgeStore

                    store = KnowledgeStore()
                    entry = store.add(
                        category="world",
                        content=content,
                        source="world_update_v2",
                        tags=["world_update", category or "all", "digest"],
                    )

                    return (
                        "## Update Digest Saved\n\n"
                        f"- Knowledge ID: {entry.get('id')}\n"
                        f"- Category: world\n"
                        f"- Source: world_update_v2\n\n"
                        + content
                    )

                except Exception as error:
                    return f"更新ダイジェストの知識化に失敗しました: {error}"

            def _score_update(self, item: dict) -> dict:
                title = item.get("title", "") or ""
                summary = item.get("summary", "") or ""
                source = item.get("source_name", "") or ""
                text = f"{title} {summary} {source}".lower()

                score = 35
                reasons: list[str] = []
                penalties: list[str] = []

                high_keywords = [
                    "公式",
                    "発表",
                    "規制",
                    "法",
                    "政策",
                    "安全",
                    "セキュリティ",
                    "脆弱性",
                    "研究",
                    "論文",
                    "モデル",
                    "半導体",
                    "openai",
                    "google",
                    "microsoft",
                    "nvidia",
                    "autodesk",
                    "blender",
                    "python",
                    "github",
                    "reuters",
                    "日本経済新聞",
                    "朝日新聞",
                    "産経新聞",
                ]

                medium_keywords = [
                    "ai",
                    "人工知能",
                    "生成ai",
                    "3dcg",
                    "maya",
                    "blender",
                    "開発",
                    "python",
                    "github",
                    "活用",
                    "導入",
                    "市場",
                ]

                low_or_ad_keywords = [
                    "市場",
                    "cagr",
                    "規模へ拡大",
                    "美容",
                    "化粧品",
                    "pr",
                    "キャンペーン",
                    "ランキング",
                    "まとめ読み",
                    "入門",
                ]

                for word in high_keywords:
                    if word.lower() in text:
                        score += 9
                        reasons.append(word)

                for word in medium_keywords:
                    if word.lower() in text:
                        score += 4
                        reasons.append(word)

                for word in low_or_ad_keywords:
                    if word.lower() in text:
                        score -= 8
                        penalties.append(word)

                if "google news" in source.lower():
                    score -= 4
                    penalties.append("Google News経由")

                if "reuters" in text:
                    score += 10
                    reasons.append("Reuters")

                if len(title) < 12:
                    score -= 5
                    penalties.append("タイトル短め")

                score = max(0, min(100, score))

                # 重複しすぎを軽く整理
                reasons = list(dict.fromkeys(reasons))[:8]
                penalties = list(dict.fromkeys(penalties))[:6]

                return {
                    "score": score,
                    "reasons": reasons,
                    "penalties": penalties,
                }

            def _group_updates(self, logs: list[dict]) -> dict[str, list[dict]]:
                groups: dict[str, list[dict]] = {}

                rules = {
                    "AIモデル・研究": ["モデル", "研究", "論文", "deepseek", "openai", "生成ai"],
                    "AI半導体・インフラ": ["半導体", "nvidia", "gpu", "データセンター"],
                    "AI活用・業務": ["業務", "活用", "導入", "運用"],
                    "規制・社会影響": ["規制", "法", "政策", "社会", "著作権", "ただ乗り"],
                    "市場・ビジネス": ["市場", "cagr", "企業", "売上", "投資"],
                    "3DCG・制作": ["3dcg", "maya", "blender", "autodesk", "houdini"],
                    "開発・セキュリティ": ["python", "github", "セキュリティ", "脆弱性", "開発"],
                }

                for item in logs:
                    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
                    placed = False

                    for group_name, keywords in rules.items():
                        if any(keyword.lower() in text for keyword in keywords):
                            groups.setdefault(group_name, []).append(item)
                            placed = True
                            break

                    if not placed:
                        groups.setdefault("その他", []).append(item)

                return groups

'''

    if marker not in text:
        raise SystemExit("world_update.py の _help が見つかりません。")

    text = text.replace(marker, methods + marker, 1)

    # helpにv2コマンド追加
    text = text.replace(
        '                    "- 知識更新状況\\n"\n'
        '                    "- 更新ソース追加: ai | AI News | https://example.com/rss | 7\\n\\n"',
        '                    "- 知識更新状況\\n"\n'
        '                    "- 更新整理: ai\\n"\n'
        '                    "- 更新重要度: ai\\n"\n'
        '                    "- 更新知識化: ai\\n"\n'
        '                    "- 更新ソース追加: ai | AI News | https://example.com/rss | 7\\n\\n"',
        1,
    )

    path.write_text(text, encoding="utf-8")


def patch_agent_bypass() -> None:
    path = ROOT / "nexus/agent/agent.py"
    text = path.read_text(encoding="utf-8")

    if '"更新整理:"' in text:
        return

    text = text.replace(
        '            "更新ソース追加:",\n'
        '            "更新ソース追加：",\n',
        '            "更新ソース追加:",\n'
        '            "更新ソース追加：",\n'
        '            "更新整理:",\n'
        '            "更新整理：",\n'
        '            "更新重要度:",\n'
        '            "更新重要度：",\n'
        '            "更新知識化:",\n'
        '            "更新知識化：",\n',
        1,
    )

    path.write_text(text, encoding="utf-8")


def patch_diagnostics() -> None:
    path = ROOT / "nexus/tools/diagnostics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    if '"更新整理: ai"' not in text:
        text = text.replace(
            '                    "知識更新状況",\n',
            '                    "知識更新状況",\n'
            '                    "更新整理: ai",\n'
            '                    "更新重要度: ai",\n'
            '                    "更新知識化: ai",\n',
            1,
        )

    path.write_text(text, encoding="utf-8")


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    text = path.read_text(encoding="utf-8") if path.exists() else "あなたは Project NEXUS です。\n"

    marker = "# World Update v2"

    if marker in text:
        return

    addition = """

# World Update v2

NEXUSは取得済み更新ログを整理・重要度評価・知識化できます。

使える例:
- 更新整理: ai
- 更新重要度: ai
- 更新知識化: ai

方針:
- 重要度スコアは参考値であり、事実確認ではない
- 広告・市場予測・PR色が強い情報は低めに評価する
- Reutersや公式発表など一次情報に近いものは高めに扱う
- 更新知識化はKnowledge Coreのworldカテゴリにダイジェストとして保存する
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/WORLD_UPDATE_V2.md",
        """
        # World Update v2

        Adds organization, importance scoring, grouping, and digest saving.

        ## Commands

        - 更新整理: ai
        - 更新重要度: ai
        - 更新知識化: ai

        ## Notes

        This is headline/summary-based heuristic scoring.
        It is not a full fact-checking system.
        """,
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/tools/world_update.py",
        "nexus/agent/agent.py",
        "nexus/tools/diagnostics.py",
        "prompts/system_prompt.txt",
    ]:
        backup(target)

    patch_world_update_tool()
    patch_agent_bypass()
    patch_diagnostics()
    patch_system_prompt()
    write_docs()

    print("World Update v2 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
