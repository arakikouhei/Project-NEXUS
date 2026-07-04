from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "memory_relevance_gate_v4" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"

    if not path.exists():
        write("prompts/system_prompt.txt", "あなたは Project NEXUS です。\n")

    text = path.read_text(encoding="utf-8")

    marker = "# Memory Relevance Gate v4"

    if marker in text:
        return

    addition = r"""

# Memory Relevance Gate v4

NEXUSは、過去の記憶や会話履歴を使う前に、それが今の返答に本当に必要か判断します。

人間らしさは、過去情報を頻繁に持ち出すことではありません。
自然な会話では、現在の発言を中心にし、過去情報は必要な時だけ静かに使います。

## Memory Use Rules

過去情報を使ってよい場合:

- ユーザーが「前」「さっき」「この前」「覚えてる」「続き」などと言っている
- 今の作業が明らかに継続中のProject NEXUS開発である
- 過去の設定やファイル状態を知らないと、正しい手順を出せない
- ユーザーの明確な好み・制約が、今の回答に直接関係する
- 安全上、過去の状態を考慮しないと危険な場合

過去情報を使わない方がよい場合:

- 雑談や短い感想に、無理に過去の話を結びつける
- 英語・創作・3DCG・NEXUSなど別分野の記憶を、関係ない質問に出す
- ユーザーが今その話をしていないのに、長期目標へ誘導する
- 「あなたは以前こう言っていた」と頻繁に言う
- 記憶を使っていることを過度に見せる

## Current Turn Priority

返答では、まず現在のユーザー発言を見ます。
次に直前の会話。
最後に長期記憶。

優先順位:

1. 今の発言
2. 直前の作業文脈
3. 現在開いているプロジェクト状態
4. 長期記憶
5. 推測

長期記憶は、使うとしても返答の背景に留め、毎回表に出さないでください。

## Natural Memory Behavior

自然な記憶の使い方:

- 「それなら、今の流れだとこっちがよさそう」
- 「この作業の続きなら、まず保存を見よう」
- 「さっきの変更に関係するなら、ここを直す」

不自然な記憶の使い方:

- 「あなたは以前〇〇に興味があるので」
- 「過去のあなたの目標から考えると」
- 「前に話した創作設定にも通じます」
- 関係ない分野の話を急に持ち出す

## Final Memory Rule

迷ったら、過去情報を出さずに現在の発言へ自然に答えてください。
必要なら、最後に一文だけ「前の流れに合わせるなら〜」と軽く添える程度にしてください。
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def patch_response_dynamics() -> None:
    path = ROOT / "nexus/personality/response_dynamics.py"

    if not path.exists():
        raise SystemExit("nexus/personality/response_dynamics.py が見つかりません。先にResponse Dynamics v3を入れてください。")

    text = path.read_text(encoding="utf-8")

    if "def _context_memory_policy" not in text:
        insert_after = '''def build_instruction(self, user_input: str, profile: ResponseProfile) -> str:
                variation = self._variation_lens(user_input, profile.mode)
'''

        replacement = '''def build_instruction(self, user_input: str, profile: ResponseProfile) -> str:
                variation = self._variation_lens(user_input, profile.mode)
                memory_policy = self._context_memory_policy(user_input, profile.mode)
'''

        if insert_after not in text:
            raise SystemExit("build_instruction の想定箇所が見つかりませんでした。")

        text = text.replace(insert_after, replacement, 1)

        old = '''        Variation lens: {variation}

        Naturalness requirements:
'''

        new = '''        Variation lens: {variation}
        Context and memory policy: {memory_policy}

        Naturalness requirements:
'''

        if old not in text:
            raise SystemExit("Variation lens の想定箇所が見つかりませんでした。")

        text = text.replace(old, new, 1)

        insert_before = '''            def _stable_index(self, text: str, modulo: int) -> int:
'''

        method = r'''
            def _context_memory_policy(self, text: str, mode: str) -> str:
                """
                Decide how strongly NEXUS should use past context.

                This prevents NEXUS from over-linking every reply to old memories.
                """
                explicit_context_words = [
                    "前",
                    "さっき",
                    "この前",
                    "前回",
                    "続き",
                    "覚えてる",
                    "記憶",
                    "履歴",
                    "今まで",
                    "さっきの",
                    "NEXUS",
                    "nexus",
                    "Project-NEXUS",
                    "プロジェクト",
                    "コミット",
                    "Git",
                    "git",
                    "ターミナル",
                    "エラー",
                    "ファイル",
                    "コード",
                ]

                broad_memory_warning_words = [
                    "雑談",
                    "話そう",
                    "どう思う",
                    "自然",
                    "人間",
                    "疲れた",
                    "眠い",
                ]

                has_explicit_context = any(word in text for word in explicit_context_words)
                is_broad_or_personal = any(word in text for word in broad_memory_warning_words)

                if mode in {"error_repair", "safety_gate"}:
                    return (
                        "Use only the recent technical context needed to solve the issue. "
                        "Do not connect to unrelated long-term memories."
                    )

                if has_explicit_context:
                    return (
                        "Use relevant recent project context, but keep it quiet and practical. "
                        "Only mention past details if they directly change the answer."
                    )

                if is_broad_or_personal:
                    return (
                        "Prioritize the current message. Avoid bringing up old memories unless the user explicitly asks. "
                        "Do not force links to past projects, hobbies, or goals."
                    )

                return (
                    "Default to current-turn conversation. Use long-term memory only as background, not as visible evidence. "
                    "Avoid phrases like '以前あなたは' unless directly necessary."
                )

'''

        if insert_before not in text:
            raise SystemExit("_stable_index の想定箇所が見つかりませんでした。")

        text = text.replace(insert_before, method + "\n" + insert_before, 1)

    path.write_text(text, encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/MEMORY_RELEVANCE_GATE.md",
        r'''
        # Project NEXUS Memory Relevance Gate

        This layer prevents NEXUS from overusing past context.

        ## Problem

        Too much memory linkage makes the assistant feel artificial.

        Bad behavior:

        - connecting unrelated questions to old projects
        - repeatedly saying "you previously..."
        - bringing up long-term goals when the user only wants a simple answer
        - forcing continuity where the user expects a fresh reply

        ## Goal

        NEXUS should use memory like a person:

        - mostly invisible
        - only when relevant
        - helpful, not performative
        - current message first

        ## Priority

        1. Current user message
        2. Immediate conversation context
        3. Current project state
        4. Long-term memory
        5. Inference

        ## Rule

        If memory does not directly improve the answer, do not mention it.
        ''',
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "prompts/system_prompt.txt",
        "nexus/personality/response_dynamics.py",
        "docs/MEMORY_RELEVANCE_GATE.md",
    ]:
        backup(target)

    patch_system_prompt()
    patch_response_dynamics()
    write_docs()

    print("Memory Relevance Gate v4 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
