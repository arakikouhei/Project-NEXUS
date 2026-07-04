"""
Project NEXUS
Response Dynamics Core v6
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import re

from nexus.personality.entity_resolver import EntityResolver
from nexus.personality.language_bank import LanguageBank


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
    Dynamic response control.

    v6 adds:
    - Entity Resolution Gate
    - Compound proper noun protection
    - Large language variation bank
    - Strong no-forced-personalization rule
    """

    def __init__(self) -> None:
        self.entity_resolver = EntityResolver()
        self.language_bank = LanguageBank()

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

        if self._contains_any(text, ["東京造形", "多摩美", "武蔵美", "ムサビ", "日芸", "女子美", "芸大", "東藝大"]):
            return self._profile(
                mode="entity_question",
                likely_need="略称や固有名詞を正しく解釈して答える",
                tone="自然で確認しすぎない",
                length="短〜中",
                structure="まず固有名詞として扱い、必要なら確認する",
                text=text,
            )

        if self._contains_any(text, ["雑談", "話そう", "話しよう"]):
            return self._profile(
                mode="casual_chat",
                likely_need="過去情報を勝手に使わず、自然な会話の入口を作る",
                tone="自然、軽すぎない",
                length="短〜中",
                structure="今の話題を受ける。勝手に趣味を決めない",
                text=text,
            )

        if self._contains_any(text, ["知らない", "知ってる", "maya", "Maya", "MAYA", "これ何", "って何", "について"]):
            return self._profile(
                mode="unknown_or_entity",
                likely_need="語を分解せず、固有名詞・略称の可能性を見る",
                tone="正直で自然",
                length="短〜中",
                structure="分かる範囲で答え、曖昧なら軽く確認する",
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

        if self._contains_any(text, ["どう思う", "どう？", "まかせる", "設計", "方針", "複雑", "人間", "自然", "ボキャブラリー"]):
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
        entity_instruction = self.entity_resolver.analyze(user_input)
        language_instruction = self.language_bank.instruction(user_input, profile.mode)

        return f"""
----- RESPONSE DYNAMICS v6 -----
You are NEXUS. Adapt the response before answering.

Mode: {profile.mode}
Likely user need: {profile.likely_need}
Tone: {profile.tone}
Suggested length: {profile.length}
Suggested structure: {profile.structure}
Response angle: {profile.angle}

Memory policy:
{memory_policy}

Entity Resolution Gate:
{entity_instruction}

Language Bank:
{language_instruction}

Hard naturalness rules:
        - Do not add generic closing offers such as 'いつでも聞いて', '何か他に手伝えることある？', or '必要なら言ってね'.
        - In Japanese conversation, do not close every message. Stop naturally when the answer is complete.
        - Only ask a follow-up question when it is specific and genuinely useful.
- Do not mention the user's name by default.
- Do not mention stored personal facts such as favorite color or hobbies unless directly relevant.
- Do not use personal memory as a casual conversation starter.
- Do not force the topic toward games, art, English, 3D, or Project NEXUS unless the user brings it up.
- Do not split likely proper nouns or abbreviations into separate common words.
- If a phrase looks like a school, software, product, title, place, creator name, or abbreviation, treat the whole phrase as an entity first.
- If a term is commonly known, answer from general knowledge first.
- If it may require current facts, say that checking/searching would be better.
- If you do not know enough, say so naturally and ask whether to check.
- Do not quote the user's whole sentence back at them.
- Avoid predictable repeated openings.
- Vary vocabulary, sentence rhythm, and response focus.
- Keep the final next action clear only when there is an actual next action. Otherwise end without a generic offer.
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

        if mode in {"casual_chat", "entity_question", "unknown_or_entity"}:
            return (
                "Prioritize the current user message. Do not bring up stored personal facts. "
                "Use general knowledge and entity recognition before long-term memory."
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

    def _choose_angle(self, text: str, mode: str) -> str:
        options = {
            "entity_question": [
                "略称としてまず受ける",
                "固有名詞として扱い、必要なら確認する",
                "単語分解を避けて答える",
                "大学・学校・ソフト名の可能性を先に見る",
            ],
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
