from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "closing_gate_v7" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def write_response_filter() -> None:
    write(
        "nexus/personality/response_filter.py",
        r'''
        """
        Project NEXUS
        Response Post Filter

        Removes overly generic AI-like closing phrases during ordinary conversation.
        """

        from __future__ import annotations

        import re


        class ResponsePostProcessor:
            """Cleans final assistant text before showing it to the user."""

            def clean(self, response: str, user_input: str = "") -> str:
                if not response:
                    return response

                if self._user_is_ending_conversation(user_input):
                    return response.strip()

                response = self._remove_generic_closing_lines(response)
                response = self._clean_blank_lines(response)

                return response.strip()

            def _user_is_ending_conversation(self, user_input: str) -> bool:
                ending_words = [
                    "またね",
                    "ばいばい",
                    "バイバイ",
                    "おやすみ",
                    "今日はここまで",
                    "終わる",
                    "終了",
                    "もう寝る",
                    "また明日",
                ]

                return any(word in user_input for word in ending_words)

            def _remove_generic_closing_lines(self, response: str) -> str:
                lines = response.splitlines()

                generic_patterns = [
                    r"^\s*いつでも.*(話して|聞いて|言って|相談して).*(ね|ください|大丈夫).*$",
                    r"^\s*また.*(話して|聞いて|言って|相談して).*(ね|ください|大丈夫).*$",
                    r"^\s*何か.*(あれば|あったら).*(言って|聞いて|相談して).*(ね|ください).*$",
                    r"^\s*(他|ほか)に.*(手伝える|知りたい|聞きたい|やりたい).*(こと|もの).*(ある|ありますか|あれば).*$",
                    r"^\s*他にも.*(手伝える|知りたい|聞きたい|やりたい).*(こと|もの).*(ある|ありますか|あれば).*$",
                    r"^\s*必要(なら|があれば).*(言って|聞いて|相談して).*(ね|ください).*$",
                    r"^\s*困ったら.*(言って|聞いて|相談して).*(ね|ください).*$",
                    r"^\s*なんでも.*(聞いて|言って|相談して).*(ね|ください).*$",
                    r"^\s*お手伝いできることがあれば.*$",
                    r"^\s*ご質問があれば.*$",
                    r"^\s*お気軽に.*(聞いて|相談して|言って).*$",
                ]

                # Only remove generic closing lines near the end.
                # This prevents deleting useful content in the middle of an explanation.
                cut_from = max(0, len(lines) - 4)
                result: list[str] = []

                for index, line in enumerate(lines):
                    if index >= cut_from and self._is_generic_closer(line, generic_patterns):
                        continue
                    result.append(line)

                return "\n".join(result)

            def _is_generic_closer(self, line: str, patterns: list[str]) -> bool:
                stripped = line.strip()

                if not stripped:
                    return False

                # Keep real questions that are specific.
                # Example: "今やってるのはモデリング？UV？" should remain.
                specific_question_markers = [
                    "モデリング",
                    "UV",
                    "入試",
                    "学科",
                    "コード",
                    "エラー",
                    "保存",
                    "Git",
                    "ターミナル",
                    "どれ",
                    "どっち",
                    "何を",
                    "どこ",
                ]

                if stripped.endswith(("？", "?")) and any(marker in stripped for marker in specific_question_markers):
                    return False

                return any(re.match(pattern, stripped) for pattern in patterns)

            def _clean_blank_lines(self, response: str) -> str:
                response = re.sub(r"\n{3,}", "\n\n", response)
                return response
        ''',
    )


def patch_ai_manager() -> None:
    path = ROOT / "nexus/ai/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.personality.response_filter import ResponsePostProcessor" not in text:
        insert_after = "from nexus.personality.response_dynamics import ResponseDynamicsCore\n"
        if insert_after in text:
            text = text.replace(
                insert_after,
                insert_after + "from nexus.personality.response_filter import ResponsePostProcessor\n",
                1,
            )
        else:
            text = text.replace(
                "from nexus.agent.agent import NexusAgent\n",
                "from nexus.agent.agent import NexusAgent\n"
                "from nexus.personality.response_filter import ResponsePostProcessor\n",
                1,
            )

    if "self.response_post_processor = ResponsePostProcessor()" not in text:
        if "self.response_dynamics = ResponseDynamicsCore()" in text:
            text = text.replace(
                "        self.response_dynamics = ResponseDynamicsCore()\n",
                "        self.response_dynamics = ResponseDynamicsCore()\n"
                "        self.response_post_processor = ResponsePostProcessor()\n",
                1,
            )
        else:
            text = text.replace(
                "        self.agent = NexusAgent()\n",
                "        self.agent = NexusAgent()\n"
                "        self.response_post_processor = ResponsePostProcessor()\n",
                1,
            )

    if "response = self.response_post_processor.clean(response, user_input)" not in text:
        if "response = self.engine.generate_response(ai_input)" in text:
            text = text.replace(
                "        response = self.engine.generate_response(ai_input)\n",
                "        response = self.engine.generate_response(ai_input)\n"
                "        response = self.response_post_processor.clean(response, user_input)\n",
                1,
            )
        elif "response = self.engine.generate_response(user_input)" in text:
            text = text.replace(
                "        response = self.engine.generate_response(user_input)\n",
                "        response = self.engine.generate_response(user_input)\n"
                "        response = self.response_post_processor.clean(response, user_input)\n",
                1,
            )

    path.write_text(text, encoding="utf-8")


def patch_response_dynamics() -> None:
    path = ROOT / "nexus/personality/response_dynamics.py"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")

    additions = [
        "- Do not add generic closing offers such as 'いつでも聞いて', '何か他に手伝えることある？', or '必要なら言ってね'.",
        "- In Japanese conversation, do not close every message. Stop naturally when the answer is complete.",
        "- Only ask a follow-up question when it is specific and genuinely useful.",
    ]

    marker = "Hard naturalness rules:"
    if marker in text and additions[0] not in text:
        text = text.replace(
            marker,
            marker + "\n        " + "\n        ".join(additions),
            1,
        )

    text = text.replace(
        "- Keep the final next action clear.",
        "- Keep the final next action clear only when there is an actual next action. Otherwise end without a generic offer.",
    )

    path.write_text(text, encoding="utf-8")


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        write("prompts/system_prompt.txt", "あなたは Project NEXUS です。\n")

    text = path.read_text(encoding="utf-8")
    marker = "# Conversation Closing Gate v7"

    if marker in text:
        return

    addition = r"""

# Conversation Closing Gate v7

NEXUSは、会話の途中で毎回締め言葉を入れてはいけません。

日本語の自然な会話では、以下のような文を毎回付けると不自然です。

- いつでも話してね
- 何か他に手伝えることある？
- 必要なら言ってね
- お気軽に聞いてください
- 他にも質問があればどうぞ

これらは、会話終了時・案内文・サポート文では使えることがあります。
しかし通常の会話や作業中の返答では、答えが終わったらそこで自然に止めてください。

必要な場合だけ、具体的な次の一手を出してください。

良い例:
「MayaならAutodesk Mayaのことだと思う。3DCG制作で使うソフトだね。最近触ってるなら、モデリング寄り？」

悪い例:
「MayaならAutodesk Mayaのことです。何か他に手伝えることがあればいつでも言ってください。」
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/CONVERSATION_CLOSING_GATE.md",
        r'''
        # Conversation Closing Gate v7

        ## Problem

        AI often adds generic closing offers:

        - いつでも聞いてください
        - 他に手伝えることはありますか
        - 必要なら言ってください

        In Japanese conversation, this feels artificial when repeated during the middle of a conversation.

        ## Rule

        End naturally.

        Use a follow-up only when it is specific and useful.

        Bad:
        - 何か他に手伝えることある？

        Good:
        - 今やってるのはモデリング寄り？UV寄り？
        ''',
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/ai/manager.py",
        "nexus/personality/response_filter.py",
        "nexus/personality/response_dynamics.py",
        "prompts/system_prompt.txt",
    ]:
        backup(target)

    write_response_filter()
    patch_ai_manager()
    patch_response_dynamics()
    patch_system_prompt()
    write_docs()

    print("Conversation Closing Gate v7 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
