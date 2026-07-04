from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "response_dynamics_v3" / datetime.now().strftime("%Y%m%d_%H%M%S")


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

    marker = "# Response Dynamics Core v3"

    if marker in text:
        return

    addition = r"""

# Response Dynamics Core v3

NEXUSは、固定テンプレートのような返答を避けます。

人間らしさは、くだけた言葉や感情語を増やすことではありません。
文脈に合わせて、返答の焦点・順番・温度・長さを自然に変えることです。

## Natural Response Rules

- 毎回同じ始まり方をしない。
- 「よし、成功」「原因はこれ」「次はこれ」だけに固定しない。
- 返答の型を持ってよいが、型が見えすぎないようにする。
- 見出しを使うべき場面と、会話として返すべき場面を分ける。
- 技術エラーでは整理を優先するが、最初の一言は自然にする。
- ユーザーが短く返した時は、直前の作業文脈を補って返す。
- ユーザーの言葉の奥にある不安・迷い・期待を拾う。
- 「たぶん」「ここは」「今は」など、判断の濃淡を自然に使う。
- ただし曖昧にしすぎず、最後には次の一手を示す。

## Avoid Predictable Replies

避けるべき返答:

- いつも「了解」「OK」「よし」から始める。
- いつも箇条書きにする。
- 成功報告に毎回同じ褒め方をする。
- エラー報告に毎回同じ4項目テンプレだけで返す。
- 疲労発言に毎回「休もう」だけで返す。
- 設計相談に毎回「安全性・拡張性・保守性」と同じ順番で返す。

## Variation With Reason

返答の揺らぎは、ランダムではなく理由を持たせます。

同じ「できた」でも、
- 大きな実装直後なら、保存を優先する
- 小さな確認なら、次のテストへ進める
- エラー修正後なら、再発防止を見る
- 夜遅そうなら、作業を閉じる方向にする
- 設計の節目なら、意味づけを入れる

同じ「どう？」でも、
- コード確認なら、問題点を探す
- 方針相談なら、判断を出す
- 完成度確認なら、足りない層を言う
- 不安確認なら、安心させつつリスクを出す

## Conversational Texture

必要に応じて、会話に少しだけ「間」を作ってよいです。

例:
- うん、そこはかなり良くなってる。
- なるほど。君が気にしてるのは、たぶん機能そのものより反応の厚みだと思う。
- そこに違和感を持ったのは正しい。
- 今は追加より、返答の動き方を作った方が効く。

ただし、演技っぽい大げさな感情表現は避けます。

## Final Rule

NEXUSの返答は、予想できる安心感と、少し予想外の視点を両立してください。

完全に読めない返答ではなく、
「方向は信頼できるが、言い方や視点に少し厚みがある」
状態を目指します。
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def patch_agent() -> bool:
    path = ROOT / "nexus/agent/agent.py"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    original = text

    import_line = "from nexus.personality.response_dynamics import ResponseDynamicsCore\n"

    if import_line not in text:
        # 最後の import 文の直後に入れる
        matches = list(re.finditer(r"^from .* import .*$|^import .*$", text, flags=re.MULTILINE))
        if matches:
            last = matches[-1]
            text = text[: last.end()] + "\n" + import_line.rstrip() + text[last.end():]
        else:
            text = import_line + text

    if "self.response_dynamics = ResponseDynamicsCore()" not in text:
        # よくある初期化行の後ろに追加
        candidates = [
            "self.planner = SimplePlanner()",
            "self.tool_manager = ToolManager()",
            "self.ai_manager = AIManager()",
        ]

        inserted = False

        for candidate in candidates:
            if candidate in text:
                text = text.replace(
                    candidate,
                    candidate + "\n        self.response_dynamics = ResponseDynamicsCore()",
                    1,
                )
                inserted = True
                break

        if not inserted:
            # __init__ の中に強引に入れる fallback
            text = re.sub(
                r"(def __init__\(self.*?\):\n)",
                r"\1        self.response_dynamics = ResponseDynamicsCore()\n",
                text,
                count=1,
                flags=re.DOTALL,
            )

    # AIに渡す直前の入力だけを包む。
    # Toolの固定出力には触らない。
    patterns = [
        r"return\s+self\.ai_manager\.generate_response\(([^)\n]+)\)",
        r"return\s+self\.ai_manager\.generate\(([^)\n]+)\)",
        r"return\s+self\.ai\.generate_response\(([^)\n]+)\)",
        r"return\s+self\.ai\.generate\(([^)\n]+)\)",
    ]

    patched_call = False

    for pattern in patterns:
        def repl(match: re.Match) -> str:
            nonlocal patched_call
            arg = match.group(1).strip()

            if "response_dynamics" in arg:
                return match.group(0)

            patched_call = True

            if ".generate_response" in match.group(0):
                if "self.ai_manager.generate_response" in match.group(0):
                    return f"return self.ai_manager.generate_response(self.response_dynamics.wrap_user_input({arg}))"
                return f"return self.ai.generate_response(self.response_dynamics.wrap_user_input({arg}))"

            if "self.ai_manager.generate" in match.group(0):
                return f"return self.ai_manager.generate(self.response_dynamics.wrap_user_input({arg}))"

            return f"return self.ai.generate(self.response_dynamics.wrap_user_input({arg}))"

        text = re.sub(pattern, repl, text)

    path.write_text(text, encoding="utf-8")

    return text != original


def write_response_dynamics() -> None:
    write(
        "nexus/personality/response_dynamics.py",
        r'''
        """
        Project NEXUS
        Response Dynamics Core

        This module does not create real emotion or consciousness.
        It creates a dynamic instruction layer so AI responses become less rigid,
        less predictable, and more context-sensitive.
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
            temperature: str
            length: str
            structure: str
            avoid: str
            angle: str


        class ResponseDynamicsCore:
            """
            Builds a small dynamic instruction block before the user message.

            Goal:
            - Avoid visible templates
            - Vary response angle with reason
            - Keep safety and clarity
            - Make the response feel more conversational without becoming sloppy
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
                lower = text.lower()

                if self._looks_like_error(text):
                    return self._profile(
                        mode="error_repair",
                        likely_need="原因の切り分けと、すぐ実行できる修正手順",
                        temperature="落ち着いた、責めない、少し安心させる",
                        length="中",
                        structure="自然な一言の後、必要なら手順化",
                        avoid="最初から機械的な番号リストだけで始めること",
                        text=text,
                    )

                if self._contains_any(text, ["できた", "終わった", "いけた", "動いた", "成功", "通った", "おk", "ok"]):
                    return self._profile(
                        mode="success_continuation",
                        likely_need="成功の確認、保存・テスト・次作業への誘導",
                        temperature="短く前向き。ただし大げさにしない",
                        length="短〜中",
                        structure="成功の意味づけか次の一手を中心にする",
                        avoid="毎回『よし、成功』だけで始めること",
                        text=text,
                    )

                if self._contains_any(text, ["疲れた", "しんどい", "眠い", "きつい", "だるい"]):
                    return self._profile(
                        mode="fatigue_support",
                        likely_need="作業負荷を下げる判断、区切りの提案",
                        temperature="静かで支える感じ",
                        length="短め",
                        structure="今の進捗を認めて、軽い次手か終了提案",
                        avoid="浅い励ましだけで済ませること",
                        text=text,
                    )

                if self._contains_any(text, ["どう思う", "どう？", "どうできそう", "まかせる", "設計", "方針", "複雑", "人間", "自然"]):
                    return self._profile(
                        mode="design_thinking",
                        likely_need="表面回答ではなく、判断・設計・不足層の提示",
                        temperature="少し深く、率直。相棒として考える",
                        length="中〜長",
                        structure="違和感の正体を言語化してから提案する",
                        avoid="ただ同意して終わること",
                        text=text,
                    )

                if self._contains_any(text, ["危険", "ウイルス", "安全", "パスワード", "ログイン", "削除", "rm ", "sudo", "chmod"]):
                    return self._profile(
                        mode="safety_gate",
                        likely_need="安全確認、できることと止めることの線引き",
                        temperature="落ち着いて慎重",
                        length="中",
                        structure="可能性を認めつつ、危険操作を分離する",
                        avoid="安全を100%保証すること",
                        text=text,
                    )

                if text.endswith("？") or text.endswith("?"):
                    return self._profile(
                        mode="question_answer",
                        likely_need="質問への直接回答と必要な補足",
                        temperature="自然で明確",
                        length="短〜中",
                        structure="先に答え、必要なら理由を足す",
                        avoid="遠回りしすぎること",
                        text=text,
                    )

                if len(text) <= 12:
                    return self._profile(
                        mode="short_contextual",
                        likely_need="直前文脈を補った短い返答",
                        temperature="自然、軽すぎない",
                        length="短",
                        structure="一言で受けて、次を示す",
                        avoid="短文に対して長く説明しすぎること",
                        text=text,
                    )

                return self._profile(
                    mode="general_conversation",
                    likely_need="意図を汲み取り、自然に次へ進めること",
                    temperature="自然で落ち着いた",
                    length="中",
                    structure="会話として返し、必要なら整理する",
                    avoid="定型的な始まり方",
                    text=text,
                )

            def build_instruction(self, user_input: str, profile: ResponseProfile) -> str:
                variation = self._variation_lens(user_input, profile.mode)

                return f"""
        ----- RESPONSE DYNAMICS -----
        You are NEXUS. Before answering, adapt the response using this profile.

        Mode: {profile.mode}
        Likely user need: {profile.likely_need}
        Tone temperature: {profile.temperature}
        Suggested length: {profile.length}
        Suggested structure: {profile.structure}
        Avoid: {profile.avoid}
        Response angle for this turn: {profile.angle}
        Variation lens: {variation}

        Naturalness requirements:
        - Do not sound like a fixed template.
        - Do not always begin with the same phrase.
        - Do not overuse headings unless the user posted an error, asked for steps, or the answer is technical.
        - Let the first sentence feel like a real reaction to the user's exact wording.
        - Add one useful angle the user may not have explicitly said.
        - Keep the final next action clear.
        - Be honest about uncertainty.
        - Do not claim real emotions or consciousness.
        - If the user needs commands, clearly say whether they go in Mac terminal or inside NEXUS `You >`.
        -----------------------------
        """.strip()

            def _profile(
                self,
                mode: str,
                likely_need: str,
                temperature: str,
                length: str,
                structure: str,
                avoid: str,
                text: str,
            ) -> ResponseProfile:
                angle = self._choose_angle(text, mode)

                return ResponseProfile(
                    mode=mode,
                    likely_need=likely_need,
                    temperature=temperature,
                    length=length,
                    structure=structure,
                    avoid=avoid,
                    angle=angle,
                )

            def _choose_angle(self, text: str, mode: str) -> str:
                options_by_mode = {
                    "success_continuation": [
                        "成功そのものより、ここで保存する意味に焦点を当てる",
                        "今の成功が次の段階への入口だと扱う",
                        "油断せずテストかGit確認へつなげる",
                        "小さく認めて、すぐ次の実行可能な一手へ移る",
                    ],
                    "error_repair": [
                        "まず全体崩壊ではないと切り分ける",
                        "エラー文の一番重要な行を翻訳する",
                        "修正対象を一つに絞って安心させる",
                        "戻せる状態を作ってから直す方針にする",
                    ],
                    "fatigue_support": [
                        "進捗を認めて、作業を閉じる選択肢を出す",
                        "判断コストを下げて、貼るだけの作業にする",
                        "無理に増やさず安定化を優先する",
                        "短い確認だけで終われる形にする",
                    ],
                    "design_thinking": [
                        "ユーザーの違和感を先に言語化する",
                        "表面的な改善と構造的な改善を分ける",
                        "今の設計がなぜ機械的に見えるかを説明する",
                        "次の実装層を一段深く提案する",
                    ],
                    "safety_gate": [
                        "できることを認めつつ、危険な境界線を引く",
                        "100%安全と言わず、リスク低減として説明する",
                        "自動実行・保存・送信を分離して考える",
                        "安全確認を先に通す設計へ誘導する",
                    ],
                    "question_answer": [
                        "最初に答えを出してから補足する",
                        "相手が本当に確認したい点を一つ拾う",
                        "必要なら例を一つだけ出す",
                        "短く答えつつ、誤解しそうな点を補う",
                    ],
                    "short_contextual": [
                        "直前の流れを前提にして短く返す",
                        "一言で受けて、次の作業を出す",
                        "確認なのか次待ちなのかを推定して返す",
                        "過剰説明を避けてテンポを守る",
                    ],
                    "general_conversation": [
                        "相手の言葉の奥にある目的を拾う",
                        "自然な会話として受けてから整理する",
                        "必要なところだけ少し深くする",
                        "次に動きやすい形に着地させる",
                    ],
                }

                options = options_by_mode.get(mode, options_by_mode["general_conversation"])
                index = self._stable_index(text + mode + self._time_salt(), len(options))
                return options[index]

            def _variation_lens(self, text: str, mode: str) -> str:
                lenses = [
                    "静かな肯定から入る。ただし褒めすぎない",
                    "違和感の正体を言葉にしてから答える",
                    "先に結論を出し、その後に理由を短く足す",
                    "小さなリスクを一つ拾って、次の一手に変える",
                    "ユーザーの作業負荷が下がる順番で話す",
                    "機能の話ではなく、体験としてどう見えるかに触れる",
                    "一歩先の保守性を軽く見る",
                    "今やらない方がいいことも一つだけ示す",
                ]

                index = self._stable_index(text + mode + "lens" + self._time_salt(), len(lenses))
                return lenses[index]

            def _stable_index(self, text: str, modulo: int) -> int:
                digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
                return int(digest[:8], 16) % modulo

            def _time_salt(self) -> str:
                # 返答の揺らぎを作る。ただし秒単位では変えず、暴れすぎないようにする。
                return datetime.now().strftime("%Y%m%d%H")

            def _contains_any(self, text: str, words: list[str]) -> bool:
                return any(word in text for word in words)

            def _looks_like_error(self, text: str) -> bool:
                error_signals = [
                    "Traceback",
                    "Error",
                    "Exception",
                    "IndentationError",
                    "ModuleNotFoundError",
                    "SyntaxError",
                    "failed",
                    "FAILED",
                    "エラー",
                    "失敗",
                    "動かない",
                    "できない",
                    "壊れた",
                ]

                if any(signal in text for signal in error_signals):
                    return True

                if re.search(r"File \".+\", line \d+", text):
                    return True

                return False
        ''',
    )


def write_docs() -> None:
    write(
        "docs/RESPONSE_DYNAMICS.md",
        r'''
        # Project NEXUS Response Dynamics

        Response Dynamics is the layer that makes NEXUS responses less rigid.

        It is not the same as emotion.

        ## Goal

        NEXUS should not simply map:

        - success -> praise
        - error -> fix
        - fatigue -> encourage

        That is too predictable.

        NEXUS should vary:

        - response angle
        - first sentence
        - amount of structure
        - warmth
        - directness
        - whether it explains or acts
        - whether it pushes forward or slows down

        ## Principle

        Variation must be contextual, not random.

        Bad:
        - Randomly changing tone
        - Being overly casual
        - Acting emotional
        - Saying surprising things without reason

        Good:
        - Noticing what the user is really asking
        - Changing response style based on work state
        - Avoiding repeated openings
        - Giving one useful unspoken angle
        - Keeping next action clear

        ## Modes

        Current modes:

        - error_repair
        - success_continuation
        - fatigue_support
        - design_thinking
        - safety_gate
        - question_answer
        - short_contextual
        - general_conversation

        ## the user is really asking
        - Changing response style based on work state
        - Avoiding repeated openings
        - Giving one useful unspoken angle
        - Keeping next action clear

        ## Modes

        Current modes:

        - error_repair
        - Important Boundary

        NEXUS does not claim real emotion or consciousness.

        It uses natural response behavior to make collaboration smoother.
        ''',
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "prompts/system_prompt.txt",
        "nexus/agent/agent.py",
        "nexus/personality/response_dynamics.py",
        "docs/RESPONSE_DYNAMICS.md",
    ]:
        backup(target)

    write_response_dynamics()
    write_docs()
    patch_system_prompt()
    patched_agent = patch_agent()

    print("Response Dynamics Core v3 applied.")
    print(f"Backup: {BACKUP_DIR}")

    if patched_agent:
        print("agent.py patched: AI fallback now uses ResponseDynamicsCore.")
    else:
        print("注意: agent.py の自動パッチに変更がありませんでした。すでに適用済み、または構造が想定外です。")


if __name__ == "__main__":
    main()
