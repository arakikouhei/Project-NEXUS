"""
Project NEXUS
Research Workflow Tool v1

Guides paper research workflow:
search -> save -> summarize -> keyword extraction -> knowledge conversion.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json
import re

from nexus.tools.base_tool import BaseTool


class ResearchWorkflowTool(BaseTool):
    """Guided research workflow helper."""

    name = "research_workflow"
    description = "論文検索から知識化までの研究ワークフローを案内します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("研究ワークフロー開始:")
            or text.startswith("論文ワークフロー:")
            or text.startswith("論文から知識化:")
            or text.startswith("研究まとめ:")
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith("研究ワークフロー開始:"):
            topic = text.split(":", 1)[1].strip()
            return self._start_workflow(topic)

        if text.startswith("論文ワークフロー:"):
            topic = text.split(":", 1)[1].strip()
            return self._start_workflow(topic)

        if text.startswith("論文から知識化:"):
            paper_id = text.split(":", 1)[1].strip()
            return self._paper_to_knowledge(paper_id)

        if text.startswith("研究まとめ:"):
            topic = text.split(":", 1)[1].strip()
            return self._research_summary(topic)

        return "対応していない研究ワークフロー操作です。"

    def _start_workflow(self, topic: str) -> str:
        if not topic:
            return "研究トピックが空です。例: 研究ワークフロー開始: 3D reconstruction"

        return f"""## Research Workflow Started

Topic: {topic}

### Step 1: Search Papers

まず論文検索:

- 論文検索: {topic}

### Step 2: Save a Paper

検索結果からarXiv IDを選んで保存:

- 論文保存: arXiv ID

### Step 3: Review Saved Paper

保存後に papers-id を確認:

- 論文一覧
- 論文詳細: papers-xxxxxxxx

### Step 4: Summarize

- 論文3行まとめ: papers-xxxxxxxx
- 論文要点整理: papers-xxxxxxxx
- 論文キーワード抽出: papers-xxxxxxxx
- 論文安全評価: papers-xxxxxxxx

### Step 5: Convert to Knowledge

内容を確認してから知識化:

- 論文から知識化: papers-xxxxxxxx

### Step 6: Topic Summary

関連知識を確認:

- 研究まとめ: {topic}
- 知識横断検索: {topic}
"""

    def _paper_to_knowledge(self, paper_id: str) -> str:
        if not paper_id:
            return "paper IDが空です。例: 論文から知識化: papers-fafab9fc"

        knowledge_path = Path("data/knowledge/knowledge.json")
        knowledge = self._load_knowledge(knowledge_path)

        paper = self._find_entry(knowledge, paper_id)

        if not paper:
            return f"""## Paper Knowledge Conversion Failed

指定された論文IDが見つかりません。

- Paper ID: {paper_id}

確認:
- 論文一覧
- 知識検索: {paper_id}
"""

        if paper.get("category") != "papers":
            return f"""## Paper Knowledge Conversion Skipped

指定IDは papers カテゴリではありません。

- ID: {paper_id}
- Category: {paper.get("category", "unknown")}
"""

        existing_id = f"research-{paper_id.replace('papers-', '')}"

        if self._find_entry(knowledge, existing_id):
            return f"""## Paper Already Converted

この論文は既に研究知識として変換済みです。

- Existing ID: {existing_id}

確認:
- 知識詳細: {existing_id}
"""

        title = paper.get("title", paper_id)
        content = paper.get("content", "")
        tags = paper.get("tags", [])

        research_content = self._build_research_content(paper)

        entry = {
            "id": existing_id,
            "category": "research",
            "title": f"Research Note: {title}",
            "content": research_content,
            "tags": self._merge_tags(tags, ["research", "paper_workflow"]),
            "source": paper.get("source", "papers"),
            "source_type": "derived_from_paper",
            "source_paper_id": paper_id,
            "source_url": paper.get("source_url", paper.get("url", "")),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "archived": False,
        }

        knowledge.append(entry)
        knowledge_path.write_text(
            json.dumps(knowledge, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return f"""## Paper Converted to Knowledge

- New ID: {existing_id}
- Source Paper: {paper_id}
- Title: Research Note: {title}
- Category: research
- Tags: {", ".join(entry["tags"])}

確認:
- 知識詳細: {existing_id}
- 知識関連検索: {paper_id}
- 研究まとめ: {title}
"""

    def _research_summary(self, topic: str) -> str:
        if not topic:
            return "研究トピックが空です。例: 研究まとめ: diffusion"

        knowledge = self._load_knowledge(Path("data/knowledge/knowledge.json"))
        matches = self._search_entries(knowledge, topic)

        lines = [
            "## Research Summary",
            "",
            f"Topic: {topic}",
            "",
        ]

        if not matches:
            lines.extend([
                "関連する知識がまだ見つかりません。",
                "",
                "次に実行:",
                f"- 研究ワークフロー開始: {topic}",
                f"- 論文検索: {topic}",
            ])
            return "\n".join(lines)

        lines.append("### Related Knowledge")
        lines.append("")

        for entry, score in matches[:8]:
            lines.append(f"- {entry.get('id', 'unknown')} | {entry.get('title', 'untitled')} | category={entry.get('category', 'unknown')} | score={score}")

        lines.extend([
            "",
            "### Next Actions",
            "",
            f"- 知識横断検索: {topic}",
            f"- 知識まとめ: {topic}",
            f"- 論文検索: {topic}",
        ])

        return "\n".join(lines)

    def _load_knowledge(self, path: Path) -> list:
        if not path.exists():
            return []

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _find_entry(self, knowledge: list, entry_id: str) -> dict | None:
        for entry in knowledge:
            if isinstance(entry, dict) and entry.get("id") == entry_id:
                return entry
        return None

    def _build_research_content(self, paper: dict) -> str:
        title = paper.get("title", "untitled")
        content = paper.get("content", "")
        source = paper.get("source", "unknown")
        paper_id = paper.get("id", "unknown")

        return f"""# Research Note

## Source Paper

- ID: {paper_id}
- Title: {title}
- Source: {source}

## Summary Basis

This research note was generated from the saved paper metadata/abstract in Knowledge Core.

## Original Content

{content}

## Workflow Notes

- Review the original paper before using this as a strong claim.
- arXiv papers may not be peer-reviewed.
- Use this note as a research index, not final proof.
"""

    def _merge_tags(self, tags: list, extra: list) -> list:
        result = []

        for tag in tags + extra:
            if not tag:
                continue
            if tag not in result:
                result.append(tag)

        return result

    def _search_entries(self, knowledge: list, topic: str) -> list:
        terms = self._terms(topic)
        scored = []

        for entry in knowledge:
            if not isinstance(entry, dict):
                continue

            text = " ".join([
                str(entry.get("id", "")),
                str(entry.get("title", "")),
                str(entry.get("category", "")),
                str(entry.get("content", "")),
                " ".join(entry.get("tags", []) if isinstance(entry.get("tags", []), list) else []),
            ]).lower()

            score = 0
            for term in terms:
                if term in text:
                    score += 10
                if term and term in str(entry.get("title", "")).lower():
                    score += 8
                if term and term in str(entry.get("id", "")).lower():
                    score += 5

            if score > 0:
                scored.append((entry, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def _terms(self, topic: str) -> list:
        raw = re.split(r"[\s,、。:：/]+", topic.lower())
        return [x for x in raw if len(x) >= 2]
