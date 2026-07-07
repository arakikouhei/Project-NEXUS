"""
Project NEXUS
Memory Answer Tool v1

Answers simple project/memory questions using Project Memory,
Knowledge Core, and Work Notes.
"""

from __future__ import annotations

from pathlib import Path
import json

from nexus.tools.base_tool import BaseTool


class MemoryAnswerTool(BaseTool):
    """Answers questions from memory-related data."""

    name = "memory_answer"
    description = "Project Memory / Knowledge / Work Notes を使って記憶回答します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return (
            text.startswith("記憶回答:")
            or text in {
                "NEXUSは今どこまで進んだ？",
                "次に何を作るべき？",
                "v0.6の状態を教えて",
                "記憶の状態を教えて",
            }
        )

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith("記憶回答:"):
            question = text.split(":", 1)[1].strip()
            return self._answer(question)

        return self._answer(text)

    def _answer(self, question: str) -> str:
        if not question:
            return "質問が空です。例: 記憶回答: NEXUSは今どこまで進んだ？"

        project_memory = self._load_json("data/project/project_memory.json", {})
        knowledge = self._load_json("data/knowledge/knowledge.json", [])
        work_notes = self._load_json("data/work_notes/work_notes.json", [])

        q = question.lower()

        if self._is_current_position_question(question, q):
            return self._answer_current_position(project_memory, knowledge, work_notes)

        if self._is_next_action_question(question, q):
            return self._answer_next_action(project_memory)

        if "v0.6" in q or "v0.6" in question:
            return self._answer_v06_status(project_memory, knowledge, work_notes)

        if "記憶" in question or "memory" in q:
            return self._answer_memory_status(project_memory, knowledge, work_notes)

        return self._generic_memory_answer(question, project_memory, knowledge, work_notes)

    def _answer_current_position(self, project_memory: dict, knowledge, work_notes) -> str:
        current_stage = project_memory.get("current_stage", "unknown") if isinstance(project_memory, dict) else "unknown"
        next_stage = project_memory.get("recommended_next_stage", "unknown") if isinstance(project_memory, dict) else "unknown"

        return f"""## Memory Answer

質問: NEXUSは今どこまで進んだ？

### Answer

NEXUSは現在、**{current_stage}** の段階です。

全体ロードマップでは、v1.0実用版に向けた中盤前半で、今は **v0.6：記憶システム強化** を進めています。

### Current State

- Current Stage: {current_stage}
- Recommended Next Stage: {next_stage}
- Knowledge Entries: {len(knowledge) if isinstance(knowledge, list) else 0}
- Work Notes: {len(work_notes) if isinstance(work_notes, list) else 0}

### Evidence

- data/project/project_memory.json
- data/knowledge/knowledge.json
- data/work_notes/work_notes.json
"""

    def _answer_next_action(self, project_memory: dict) -> str:
        next_stage = project_memory.get("recommended_next_stage", "unknown") if isinstance(project_memory, dict) else "unknown"

        return f"""## Memory Answer

質問: 次に何を作るべき？

### Answer

次は **{next_stage}** を基準に進めるのが自然です。

今のv0.6計画では、記憶システム強化の流れとして以下を順番に進めています。

### Recommended Order

1. Memory Index v1 ✅
2. Project Memory Snapshot v1 ✅
3. Personal Work Notes v1 ✅
4. Memory Review v1 ✅
5. Memory Answer v1 ← 今ここ

### Next Practical Step

Memory Answer v1が完了したら、次は **Project Memoryをv0.6状態へ同期** して、その後 **v0.6 Release Snapshot** に進むのが安全です。

### Evidence

- data/project/project_memory.json
- docs/V0_6_PLAN.md
"""

    def _answer_v06_status(self, project_memory: dict, knowledge, work_notes) -> str:
        current_stage = project_memory.get("current_stage", "unknown") if isinstance(project_memory, dict) else "unknown"

        completed = [
            "Memory Index v1",
            "Project Memory Snapshot v1",
            "Personal Work Notes v1",
            "Memory Review v1",
        ]

        return f"""## Memory Answer

質問: v0.6の状態を教えて

### Answer

v0.6は **記憶システム強化** の段階です。

現在までに以下が完了しています。

### Completed

{self._bullet_list(completed)}

### In Progress

- Memory Answer v1

### Current Stage in Project Memory

- {current_stage}

### Memory Counts

- Knowledge Entries: {len(knowledge) if isinstance(knowledge, list) else 0}
- Work Notes: {len(work_notes) if isinstance(work_notes, list) else 0}

### Evidence

- docs/V0_6_PLAN.md
- data/project/project_memory.json
"""

    def _answer_memory_status(self, project_memory: dict, knowledge, work_notes) -> str:
        categories = self._category_counts(knowledge)

        return f"""## Memory Answer

質問: 記憶の状態を教えて

### Answer

NEXUSの記憶は、現在この3系統で整理されています。

### Memory Areas

- Project Memory: NEXUS自身の現在地・マイルストーン
- Knowledge Core: 論文・研究・インポート・世界更新など
- Work Notes: 日々の作業メモ

### Counts

- Knowledge Entries: {len(knowledge) if isinstance(knowledge, list) else 0}
- Knowledge Categories: {len(categories)}
- Work Notes: {len(work_notes) if isinstance(work_notes, list) else 0}

### Main Knowledge Categories

{self._format_categories(categories)}

### Useful Commands

- 記憶インデックス
- 記憶カテゴリ一覧
- 記憶レビュー
- 作業メモ一覧
- NEXUS記憶
"""

    def _generic_memory_answer(self, question: str, project_memory: dict, knowledge, work_notes) -> str:
        matches = self._search_memory(question, project_memory, knowledge, work_notes)

        lines = [
            "## Memory Answer",
            "",
            f"質問: {question}",
            "",
        ]

        if not matches:
            lines.extend([
                "### Answer",
                "",
                "この質問に強く一致する記憶は見つかりませんでした。",
                "",
                "確認に使えるコマンド:",
                "- 記憶インデックス",
                "- 記憶レビュー",
                "- 知識横断検索: query",
                "- 作業メモ検索: query",
            ])
            return "\n".join(lines)

        lines.extend([
            "### Related Memory",
            "",
        ])

        for item in matches[:8]:
            lines.append(f"- {item['type']} | {item['id']} | {item['title']} | score={item['score']}")

        lines.extend([
            "",
            "### Next",
            "",
            "- 詳しく見るなら、該当IDを詳細表示してください。",
            "- 知識IDなら `知識詳細: id`",
            "- 作業メモIDなら `作業メモ詳細: id`",
        ])

        return "\n".join(lines)

    def _search_memory(self, question: str, project_memory: dict, knowledge, work_notes) -> list[dict]:
        terms = [x.lower() for x in question.replace("　", " ").split() if x.strip()]
        results = []

        if isinstance(project_memory, dict):
            text = json.dumps(project_memory, ensure_ascii=False).lower()
            score = sum(10 for term in terms if term in text)
            if score:
                results.append({
                    "type": "project_memory",
                    "id": "project_memory",
                    "title": project_memory.get("current_stage", "Project Memory"),
                    "score": score,
                })

        if isinstance(knowledge, list):
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

                score = sum(10 for term in terms if term in text)

                if score:
                    results.append({
                        "type": "knowledge",
                        "id": entry.get("id", "unknown"),
                        "title": entry.get("title", "untitled"),
                        "score": score,
                    })

        if isinstance(work_notes, list):
            for note in work_notes:
                if not isinstance(note, dict):
                    continue

                text = " ".join([
                    str(note.get("id", "")),
                    str(note.get("summary", "")),
                    str(note.get("content", "")),
                    " ".join(note.get("tags", []) if isinstance(note.get("tags", []), list) else []),
                ]).lower()

                score = sum(10 for term in terms if term in text)

                if score:
                    results.append({
                        "type": "work_note",
                        "id": note.get("id", "unknown"),
                        "title": note.get("summary", "untitled"),
                        "score": score,
                    })

        results.sort(key=lambda x: (-x["score"], x["id"]))
        return results

    def _is_current_position_question(self, question: str, q: str) -> bool:
        return (
            "今どこ" in question
            or "どこまで" in question
            or "現在地" in question
            or "current" in q
        )

    def _is_next_action_question(self, question: str, q: str) -> bool:
        return (
            "次に何" in question
            or "次なに" in question
            or "何を作る" in question
            or "next" in q
        )

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

    def _format_categories(self, categories: dict) -> str:
        if not categories:
            return "- なし"

        lines = []
        for category, count in sorted(categories.items(), key=lambda x: (-x[1], x[0]))[:10]:
            lines.append(f"- {category}: {count}")

        return "\n".join(lines)

    def _bullet_list(self, items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)
