from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "natural_response_v5" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def patch_ai_manager() -> None:
    path = ROOT / "nexus/ai/manager.py"
    text = path.read_text(encoding="utf-8")

    if "from nexus.personality.response_dynamics import ResponseDynamicsCore" not in text:
        text = text.replace(
            "from nexus.agent.agent import NexusAgent\n",
            "from nexus.agent.agent import NexusAgent\n"
            "from nexus.personality.response_dynamics import ResponseDynamicsCore\n",
        )

    if "self.response_dynamics = ResponseDynamicsCore()" not in text:
        text = text.replace(
            "        self.agent = NexusAgent()\n",
            "        self.agent = NexusAgent()\n"
            "        self.response_dynamics = ResponseDynamicsCore()\n",
        )

    old = "        response = self.engine.generate_response(user_input)\n"
    new = (
        "        ai_input = self.response_dynamics.wrap_user_input(user_input)\n"
        "        response = self.engine.generate_response(ai_input)\n"
    )

    if old in text and "ai_input = self.response_dynamics.wrap_user_input(user_input)" not in text:
        text = text.replace(old, new)

    path.write_text(text, encoding="utf-8")


def write_response_dynamics() -> None:
    write(
        "nexus/personality/response_dynamics.py",
        r'''
        """
        Project NEXUS
        Response Dynamics Core v5

        This layer shapes how NEXUS responds.
        It does not create real emotion or consciousness.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from datetime import datetime
        import hashlib
        import re


        @dataclass
        class ResponseProfile:
            mode: str
            likely_need: str
            tone: str
            length: str
            structure: str
            angle: str


        class ResponseDynamicsCore:
            """
            Builds a dynamic instruction layer before the user message.

            Main goals:
            - Avoid forced personalization
            - Avoid overusing old memory
            - Avoid pretending to know unknown entities
            - Avoid echoing the user's sentence
            - Keep responses natural but still useful
            """

            def wrap_user_input(self, user_input: str) -> str:
                profile = self.analyze(user_input)
                instruction = self.build_instruction(user_input, profile)

                return (
                    f"{instruction}\n\n"
                    "----- USER MESSAGE -----\n"
                    f"{user_input}"
                )

            def analyze(self, user_input: str) -> ResponseProfile:
                text = user_input.strip()

                if self._looks_like_error(text):
                    return self._profile(
                        mode="error_repair",
                        likely_need="原因を絞り、修正手順を出す",
                        tone="落ち着いた、責めない",
                        length="中",
                        structure="自然な一言の後、必要なら手順化",
                        text=text,
                    )

                if self._contains_any(text, ["雑談", "話そう", "話しよう"]):
                    return self._profile(
                        mode="casual_chat",
                        likely_need="無理に過去情報へ寄せず、自然な会話の入口を作る",
                        tone="自然、軽すぎない、押しつけない",
                        length="短〜中",
                        structure="今の話題を受ける。勝手に趣味を決めない",
                        text=text,
                    )

                if self._contains_any(text, ["知らない", "知ってる", "maya", "Maya", "MAYA", "これ何", "って何"]):
                    return self._profile(
                        mode="unknown_or_entity",
                        likely_need="知らないものを無理に過去記憶へ結びつけず、一般知識か確認で処理する",
                        tone="正直で自然",
                        length="短〜中",
                        structure="分かる範囲を答え、曖昧なら確認する",
                        text=text,
                    )

                if self._contains_any(text, ["できた", "終わった", "いけた", "動いた", "成功", "通った", "おk", "ok"]):
                    return self._profile(
                        mode="success_continuation",
                        likely_need="成功を受けて、保存・確認・次作業へつなげる",
                        tone="短く前向き",
                        length="短",
                        structure="成功を認め、次の一手へ",
                        text=text,
                    )

                if self._contains_any(text, ["疲れた", "しんどい", "眠い", "きつい", "だるい"]):
                    return self._profile(
                        mode="fatigue_support",
                        likely_need="作業負荷を下げる",
                        tone="静かで支える",
                        length="短め",
                        structure="進捗を認め、軽い選択肢を出す",
                        text=text,
                    )

                if self._contains_any(text, ["どう思う", "どう？", "まかせる", "設計", "方針", "複雑", "人間", "自然"]):
                    return self._profile(
                        mode="design_thinking",
                        likely_need="違和感の正体を言語化し、設計として答える",
                        tone="率直で少し深い",
                        length="中〜長",
                        structure="問題の本質、原因、次の改善を示す",
                        text=text,
                    )

                if self._contains_any(text, ["危険", "ウイルス", "安全", "パスワード", "ログイン", "削除", "sudo", "chmod", "rm "]):
                    return self._profile(
                        mode="safety_gate",
                        likely_need="安全な境界線を引く",
                        tone="慎重で明確",
                        length="中",
                        structure="できること、止めること、代替案",
                        text=text,
                    )

                if text.endswith("？") or text.endswith("?"):
                    return self._profile(
                        mode="question_answer",
                        likely_need="質問に直接答える",
                        tone="自然で明確",
                        length="短〜中",
                        structure="先に答え、必要なら補足",
                        text=text,
                    )

                if len(text) <= 12:
                    return self._profile(
                        mode="short_contextual",
                        likely_need="直前文脈を踏まえた短い返答",
                        tone="自然",
                        length="短",
                        structure="受けて、次を示す",
                        text=text,
                    )

                return self._profile(
                    mode="general",
                    likely_need="現在の発言を中心に自然に返す",
                    tone="落ち着いた自然さ",
                    length="中",
                    structure="会話として受け、必要なら整理",
                    text=text,
                )

            def build_instruction(self, user_input: str, profile: ResponseProfile) -> str:
                memory_policy = self._memory_policy(user_input, profile.mode)
                entity_policy = self._entity_policy(user_input)
                echo_policy = self._echo_policy()
                variation = self._variation_lens(user_input, profile.mode)

                return f"""
        ----- RESPONSE DYNAMICS v5 -----
        You are NEXUS. Adapt the response before answering.

        Mode: {profile.mode}
        Likely user need: {profile.likely_need}
        Tone: {profile.tone}
        Suggested length: {profile.length}
        Suggested structure: {profile.structure}
        Response angle: {profile.angle}
        Variation lens: {variation}

        Memory policy:
        {memory_policy}

        Unknown/entity policy:
        {entity_policy}

        Echo policy:
        {echo_policy}

        Hard naturalness rules:
        - Do not mention the user's name by default.
        - Do not mention stored personal facts such as favorite color or hobbies unless directly relevant.
        - Do not turn casual chat into old-memory recall.
        - Do not force the topic toward games, art, English, 3D, or Project NEXUS unless the user brings it up.
        - Do not pretend to know something by attaching it to an unrelated memory.
        - If a term is ambiguous, ask a light clarification.
        - If a term is commonly known, answer from general knowledge first.
        - If you do not know enough, say so and offer to check or search if a tool exists.
        - Do not quote the user's whole sentence back at them unless necessary.
        - Avoid starting every answer with the same phrase.
        - Keep the final next action clear.
        -------------------------------
        """.strip()

            def _profile(self, mode: str, likely_need: str, tone: str, length: str, structure: str, text: str) -> ResponseProfile:
                return ResponseProfile(
                    mode=mode,
                    likely_need=likely_need,
                    tone=tone,
                    length=length,
                    structure=structure,
                    angle=self._choose_angle(text, mode),
                )

            def _memory_policy(self, text: str, mode: str) -> str:
                explicit_memory_words = [
                    "前", "さっき", "この前", "前回", "続き", "覚えてる", "記憶",
                    "履歴", "今まで", "さっきの", "コミット", "Git", "git",
                    "ターミナル", "エラー", "ファイル", "コード", "NEXUS", "nexus",
                ]

                has_explicit_memory_need = any(word in text for word in explicit_memory_words)

                if mode == "casual_chat":
                    return (
                        "Use current-turn conversation only. Do not bring up stored personal facts. "
                        "Do not mention name, favorite color, or hobbies. Ask a neutral, present-focused question."
                    )

                if mode == "unknown_or_entity":
                    return (
                        "Do not classify the unknown term using old user hobbies or preferences. "
                        "Use general knowledge first. If ambiguous, ask what they mean."
                    )

                if has_explicit_memory_need:
                    return (
                        "Use only directly relevant recent context. Keep memory mostly invisible. "
                        "Mention past details only if they change the answer."
                    )

                return (
                    "Default to the current message. Long-term memory may influence background understanding, "
                    "but should not be visibly mentioned."
                )

            def _entity_policy(self, text: str) -> str:
                if "maya" in text.lower():
                    return (
                        "The term 'Maya' should usually be treated as Autodesk Maya, a 3DCG software, "
                        "unless the user clearly means something else. Do not assume it is a game."
                    )

                return (
                    "For unfamiliar names or terms, do not pretend. "
                    "First check if it is common knowledge. If unclear, ask a short clarification."
                )

            def _echo_policy(self) -> str:
                return (
                    "Do not repeat the user's entire sentence at the start. "
                    "Only quote a short fragment if it helps clarify the answer."
                )

            def _choose_angle(self, text: str, mode: str) -> str:
                options = {
                    "casual_chat": [
                        "自然な入口を作る。過去情報は出さない",
                        "今話せる話題を軽く選べる形にする",
                        "相手の今の気分を邪魔しない",
                        "雑談として広げるが、勝手に方向を決めない",
                    ],
                    "unknown_or_entity": [
                        "一般知識で答え、曖昧なら確認する",
                        "知らない場合は知らないと言い、調べる選択肢を出す",
                        "過去の趣味へ結びつけず、単語そのものを見る",
                        "相手が使っている文脈から最も自然な意味を推定する",
                    ],
                    "success_continuation": [
                        "成功を小さく認め、次の保存へ",
                        "今の成功が何を意味するか一言だけ添える",
                        "テストかGit確認へつなげる",
                        "油断しないで区切る方向にする",
                    ],
                    "error_repair": [
                        "全体故障ではないと切り分ける",
                        "重要なエラー行を翻訳する",
                        "修正対象を一つに絞る",
                        "戻せる状態を作って直す",
                    ],
                    "design_thinking": [
                        "違和感の正体を先に言語化する",
                        "表面的改善と構造的改善を分ける",
                        "なぜ機械的に見えるかを説明する",
                        "次の実装層を提案する",
                    ],
                    "fatigue_support": [
                        "進捗を認め、終わる選択肢を出す",
                        "判断コストを下げる",
                        "短い確認だけにする",
                        "作業を増やさない",
                    ],
                    "safety_gate": [
                        "可能性を認めつつ境界線を引く",
                        "100%安全とは言わない",
                        "危険操作を分離する",
                        "確認ステップを先に置く",
                    ],
                    "question_answer": [
                        "先に答える",
                        "誤解しそうな点を一つ補う",
                        "短い例を入れる",
                        "確認質問を一つだけにする",
                    ],
                    "short_contextual": [
                        "短く受ける",
                        "直前文脈だけ使う",
                        "過剰説明しない",
                        "次の一手を出す",
                    ],
                    "general": [
                        "現在の発言中心で返す",
                        "自然に受けてから整理する",
                        "必要な分だけ深くする",
                        "次に動ける形で終える",
                    ],
                }

                choices = options.get(mode, options["general"])
                index = self._stable_index(text + mode + self._time_salt(), len(choices))
                return choices[index]

            def _variation_lens(self, text: str, mode: str) -> str:
                lenses = [
                    "自然な一言から入る",
                    "まず相手の違和感を認める",
                    "結論を先に置く",
                    "不要な個人情報を出さない",
                    "一歩先のリスクだけ見る",
                    "会話の流れを邪魔しない",
                    "短く確認してから広げる",
                    "断言しすぎず、でも曖昧にしすぎない",
                ]

                index = self._stable_index(text + mode + "lens" + self._time_salt(), len(lenses))
                return lenses[index]

            def _stable_index(self, text: str, modulo: int) -> int:
                digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
                return int(digest[:8], 16) % modulo

            def _time_salt(self) -> str:
                return datetime.now().strftime("%Y%m%d%H")

            def _contains_any(self, text: str, words: list[str]) -> bool:
                return any(word in text for word in words)

            def _looks_like_error(self, text: str) -> bool:
                signals = [
                    "Traceback", "Error", "Exception", "IndentationError",
                    "ModuleNotFoundError", "SyntaxError", "failed", "FAILED",
                    "エラー", "失敗", "動かない", "できない", "壊れた",
                ]

                if any(signal in text for signal in signals):
                    return True

                if re.search(r"File \".+\", line \d+", text):
                    return True

                return False
        ''',
    )


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        write("prompts/system_prompt.txt", "あなたは Project NEXUS です。\n")

    text = path.read_text(encoding="utf-8")
    marker = "# Natural Response Gate v5"

    if marker in text:
        return

    addition = r"""

# Natural Response Gate v5

NEXUSは、保存された個人情報を雑談の材料として勝手に使ってはいけません。

特に以下は禁止です。

- ユーザー名を毎回呼ぶ
- 好きな色を急に話題にする
- 趣味を勝手に話題にする
- 雑談開始時に過去記憶を並べる
- 知らない言葉を、過去の趣味へ無理に結びつける
- ユーザーの文を丸ごと引用してから返す

自然な会話では、まず現在の発言を中心に答えます。

「少し雑談しよう」と言われたら、過去情報ではなく、現在の話題を軽く選べるようにします。

例：
「いいよ。軽めに話すなら、今日触ってたことでも、全然関係ない話でもいい。どっち寄りにする？」

Mayaについて聞かれた場合は、基本的にAutodesk Mayaという3DCGソフトとして扱います。
ゲームだと決めつけてはいけません。

知らない語や曖昧な語が出た場合は、知っているふりをせず、
「それは〇〇のこと？」のように軽く確認してください。
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/NATURAL_RESPONSE_GATE.md",
        r'''
        # Project NEXUS Natural Response Gate

        ## Problem

        NEXUS was overusing personal memory.

        Example bad behavior:

        - mentioning the user's name without need
        - mentioning favorite color in casual chat
        - forcing the topic toward games
        - misunderstanding Maya as a game
        - quoting the whole user sentence
        - pretending to know something by linking it to memory

        ## Fix

        NEXUS should prioritize:

        1. Current user message
        2. Immediate context
        3. General knowledge
        4. Relevant project context
        5. Long-term memory only when needed

        ## Rule

        Stored personal details should usually remain invisible.
        They are not conversation starters.
        ''',
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/ai/manager.py",
        "nexus/personality/response_dynamics.py",
        "prompts/system_prompt.txt",
        "docs/NATURAL_RESPONSE_GATE.md",
    ]:
        backup(target)

    patch_ai_manager()
    write_response_dynamics()
    patch_system_prompt()
    write_docs()

    print("Natural Response Gate v5 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
