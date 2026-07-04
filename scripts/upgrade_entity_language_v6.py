from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import shutil
import textwrap


ROOT = Path.cwd()
BACKUP_DIR = ROOT / "backups" / "entity_language_v6" / datetime.now().strftime("%Y%m%d_%H%M%S")


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


def write_json(path_text: str, data: dict) -> None:
    path = ROOT / path_text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

    if "ai_input = self.response_dynamics.wrap_user_input(user_input)" not in text:
        text = text.replace(
            "        response = self.engine.generate_response(user_input)\n",
            "        ai_input = self.response_dynamics.wrap_user_input(user_input)\n"
            "        response = self.engine.generate_response(ai_input)\n",
        )

    path.write_text(text, encoding="utf-8")


def write_entity_aliases() -> None:
    aliases = {
        "version": 1,
        "description": "Entity aliases for Project NEXUS. Add user-specific abbreviations here.",
        "aliases": {
            "東京造形": {
                "canonical": "東京造形大学",
                "category": "university",
                "confidence": "high",
                "note": "美術・デザイン系大学の略称として扱う。東京と造形に分解しない。"
            },
            "東京造形大": {
                "canonical": "東京造形大学",
                "category": "university",
                "confidence": "high",
                "note": "東京造形大学の略称。"
            },
            "造形大": {
                "canonical": "東京造形大学",
                "category": "university",
                "confidence": "medium",
                "note": "文脈によって他大学の可能性もあるので、必要なら確認する。"
            },
            "多摩美": {
                "canonical": "多摩美術大学",
                "category": "university",
                "confidence": "high",
                "note": "美術大学の略称。"
            },
            "武蔵美": {
                "canonical": "武蔵野美術大学",
                "category": "university",
                "confidence": "high",
                "note": "美術大学の略称。"
            },
            "ムサビ": {
                "canonical": "武蔵野美術大学",
                "category": "university",
                "confidence": "high",
                "note": "武蔵野美術大学の通称。"
            },
            "日芸": {
                "canonical": "日本大学芸術学部",
                "category": "university_department",
                "confidence": "high",
                "note": "芸術系学部の略称。"
            },
            "女子美": {
                "canonical": "女子美術大学",
                "category": "university",
                "confidence": "high",
                "note": "美術大学の略称。"
            },
            "東藝大": {
                "canonical": "東京藝術大学",
                "category": "university",
                "confidence": "high",
                "note": "東京藝術大学の略称。"
            },
            "芸大": {
                "canonical": "東京藝術大学",
                "category": "university",
                "confidence": "medium",
                "note": "地域により別大学を指す可能性があるため、必要なら確認する。"
            },
            "Maya": {
                "canonical": "Autodesk Maya",
                "category": "software",
                "confidence": "high",
                "note": "3DCGソフト。ゲームだと決めつけない。"
            },
            "maya": {
                "canonical": "Autodesk Maya",
                "category": "software",
                "confidence": "high",
                "note": "3DCGソフト。文脈が制作ならAutodesk Mayaとして扱う。"
            },
            "マヤ": {
                "canonical": "Autodesk Maya",
                "category": "software_or_other",
                "confidence": "medium",
                "note": "3DCG文脈ならAutodesk Maya。神話・文明の可能性もある。"
            },
            "クリスタ": {
                "canonical": "CLIP STUDIO PAINT",
                "category": "software",
                "confidence": "high",
                "note": "イラスト制作ソフト。"
            },
            "イラレ": {
                "canonical": "Adobe Illustrator",
                "category": "software",
                "confidence": "high",
                "note": "Adobe Illustratorの略称。"
            },
            "プレミア": {
                "canonical": "Adobe Premiere Pro",
                "category": "software",
                "confidence": "medium",
                "note": "映像編集文脈ならPremiere Pro。"
            },
            "Premiere": {
                "canonical": "Adobe Premiere Pro",
                "category": "software",
                "confidence": "high",
                "note": "映像編集ソフト。"
            },
            "Premiere Pro": {
                "canonical": "Adobe Premiere Pro",
                "category": "software",
                "confidence": "high",
                "note": "映像編集ソフト。"
            },
            "Mudbox": {
                "canonical": "Autodesk Mudbox",
                "category": "software",
                "confidence": "high",
                "note": "3Dスカルプト系ソフト。"
            },
            "マッドボックス": {
                "canonical": "Autodesk Mudbox",
                "category": "software",
                "confidence": "high",
                "note": "3Dスカルプト系ソフト。"
            },
            "C4D": {
                "canonical": "Cinema 4D",
                "category": "software",
                "confidence": "high",
                "note": "3DCGソフト。"
            },
            "AE": {
                "canonical": "Adobe After Effects",
                "category": "software",
                "confidence": "medium",
                "note": "映像文脈ならAfter Effects。"
            },
            "After Effects": {
                "canonical": "Adobe After Effects",
                "category": "software",
                "confidence": "high",
                "note": "映像・モーショングラフィックスソフト。"
            }
        }
    }

    write_json("data/entity_aliases.json", aliases)


def write_entity_resolver() -> None:
    write(
        "nexus/personality/entity_resolver.py",
        r'''
        """
        Project NEXUS
        Entity Resolver

        This layer helps NEXUS treat abbreviations and compound terms as entities,
        instead of splitting them into unrelated words.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from pathlib import Path
        import json
        import re


        @dataclass
        class EntityMatch:
            alias: str
            canonical: str
            category: str
            confidence: str
            note: str


        class EntityResolver:
            """Resolves aliases and likely proper nouns."""

            def __init__(self, alias_path: str = "data/entity_aliases.json") -> None:
                self.alias_path = Path(alias_path)
                self.aliases = self._load_aliases()

            def _load_aliases(self) -> dict[str, dict[str, str]]:
                if not self.alias_path.exists():
                    return {}

                try:
                    data = json.loads(self.alias_path.read_text(encoding="utf-8"))
                    return data.get("aliases", {})
                except Exception:
                    return {}

            def analyze(self, text: str) -> str:
                matches = self.find_matches(text)
                proper_candidate = self.find_possible_proper_noun(text)

                lines = []

                if matches:
                    lines.append("Detected entity aliases:")
                    for match in matches:
                        lines.append(
                            f"- '{match.alias}' likely means '{match.canonical}' "
                            f"(category: {match.category}, confidence: {match.confidence}). "
                            f"Note: {match.note}"
                        )

                    lines.append(
                        "Entity rule: Treat detected aliases as whole entities. "
                        "Do not split them into separate common words."
                    )

                elif proper_candidate:
                    lines.append(
                        f"Possible proper noun or abbreviation detected: '{proper_candidate}'. "
                        "Treat it as a single phrase first. Do not split it into unrelated words. "
                        "If meaning is unclear, ask a light clarification or say that a search would help."
                    )

                else:
                    lines.append(
                        "No special entity alias detected. Still avoid over-splitting unfamiliar compound terms."
                    )

                lines.append(
                    "If a user asks about an institution, school, software, title, product, or abbreviation, "
                    "first consider that the whole phrase may be the name of something."
                )

                return "\n".join(lines)

            def find_matches(self, text: str) -> list[EntityMatch]:
                results: list[EntityMatch] = []

                # Longest aliases first, so 東京造形大学-like aliases win over smaller fragments.
                for alias in sorted(self.aliases.keys(), key=len, reverse=True):
                    if alias and alias in text:
                        data = self.aliases[alias]
                        results.append(
                            EntityMatch(
                                alias=alias,
                                canonical=data.get("canonical", alias),
                                category=data.get("category", "unknown"),
                                confidence=data.get("confidence", "medium"),
                                note=data.get("note", ""),
                            )
                        )

                # Deduplicate canonical names.
                seen = set()
                deduped = []
                for item in results:
                    key = (item.alias, item.canonical)
                    if key in seen:
                        continue
                    seen.add(key)
                    deduped.append(item)

                return deduped[:5]

            def find_possible_proper_noun(self, text: str) -> str | None:
                patterns = [
                    r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})について",
                    r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})って(?:いうの)?(?:を)?",
                    r"最近(?:は)?([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})(?:っていうの)?を",
                    r"([A-Za-z0-9一-龥ぁ-んァ-ンー・]{2,30})知ってる",
                ]

                stopwords = {
                    "これ",
                    "それ",
                    "あれ",
                    "どう",
                    "なに",
                    "何",
                    "少し",
                    "最近",
                    "ゲームの話もいいけど最近は",
                }

                for pattern in patterns:
                    match = re.search(pattern, text)
                    if not match:
                        continue

                    candidate = match.group(1).strip(" 、。！？?")

                    if candidate in stopwords:
                        continue

                    if len(candidate) >= 2:
                        return candidate

                return None
        ''',
    )


def write_language_bank() -> None:
    write(
        "nexus/personality/language_bank.py",
        r'''
        """
        Project NEXUS
        Language Bank

        This creates a large surface-variation space for response guidance.
        It does not force exact phrases; it gives the model a varied palette.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from datetime import datetime
        import hashlib


        @dataclass
        class LanguagePalette:
            opening_style: str
            stance: str
            transition: str
            ending_style: str
            rhythm: str
            avoid_pattern: str
            combination_count: int


        class LanguageBank:
            """Provides a large combination space for natural response variation."""

            def __init__(self) -> None:
                self.opening_styles = [
                    "一拍置いて受ける",
                    "すぐ結論に入る",
                    "違和感を先に拾う",
                    "相手の観察を認める",
                    "静かに方向を修正する",
                    "軽く確認してから広げる",
                    "短く反応して次へ移る",
                    "問題の層を分けて入る",
                    "自然な相槌から入る",
                    "断定しすぎずに受ける",
                    "具体例から入る",
                    "抽象化してから戻す",
                    "今の話題だけに集中する",
                    "余計な記憶を出さずに答える",
                    "言葉の曖昧さを軽く確認する",
                    "前提を一つだけ整える",
                    "相手の意図を言い換える",
                    "誤解しそうな点を先に止める",
                    "作業の流れを崩さず答える",
                    "短い肯定のあと本題に入る",
                    "やや率直に問題点を言う",
                    "会話として自然に返す",
                    "技術的に切り分ける",
                    "今やるべきことへ絞る",
                    "相手が言語化しきれていない点を拾う",
                    "無理に盛り上げず落ち着いて返す",
                    "質問の中心を確認する",
                    "可能性を複数出す",
                    "一番ありそうな解釈から答える",
                    "必要なら調べる前提を置く",
                ]

                self.stances = [
                    "押しつけない",
                    "一緒に考える",
                    "今は安全側に寄せる",
                    "今は自然さを優先する",
                    "現在の発言を最優先する",
                    "過去情報を背景に留める",
                    "固有名詞として扱う",
                    "知らないことは知らないと言う",
                    "検索が必要ならそう言う",
                    "曖昧なら軽く確認する",
                    "相手の作業負荷を下げる",
                    "無駄な説明を削る",
                    "必要なところだけ深くする",
                    "人間っぽさを演技にしない",
                    "テンプレを避ける",
                    "言葉の温度を上げすぎない",
                    "軽すぎず硬すぎない",
                    "次の一手を残す",
                    "誤分類を避ける",
                    "一般知識から見る",
                    "略称として見る",
                    "文脈を読みすぎない",
                    "文脈を捨てすぎない",
                    "自信度を分ける",
                    "必要なら仮説として言う",
                    "話題を勝手に変えない",
                    "相手の語彙に合わせる",
                    "自然な会話の流れを保つ",
                    "過去の好みを勝手に使わない",
                    "判断理由を少しだけ見せる",
                ]

                self.transitions = [
                    "ここで大事なのは",
                    "たぶん問題はそこじゃなくて",
                    "この場合はまず",
                    "自然に見るなら",
                    "人間ならたぶん",
                    "今の文脈だと",
                    "無理に広げるより",
                    "そこは分けて考えた方がいい",
                    "一番ありそうなのは",
                    "もし違ってたら直すけど",
                    "ここは確認を挟む方が自然",
                    "逆に言うと",
                    "だから次は",
                    "この層を入れると",
                    "今のNEXUSに足りないのは",
                    "変えるなら",
                    "まず直すべきは",
                    "ここで過去記憶を出すと",
                    "今はその言葉を",
                    "その略称は",
                    "固有名詞として見るなら",
                    "単語に分けずに",
                    "検索が必要な場面なら",
                    "会話としては",
                    "返答の硬さを減らすなら",
                    "実装としては",
                    "プロンプトだけでは弱いから",
                    "コード側で止めるなら",
                    "次の改善は",
                    "ここまで来ると",
                ]

                self.ending_styles = [
                    "次に入れるコードを出す",
                    "一度テストする流れにする",
                    "短い確認質問で終える",
                    "次の一手だけ示す",
                    "保存タイミングを伝える",
                    "必要なら調べる選択肢を出す",
                    "今はここまでで区切る",
                    "比較例を一つだけ出す",
                    "理想の返答例を出す",
                    "まず最小修正で進める",
                    "あとで拡張できる形にする",
                    "危険な部分は後回しにする",
                    "ユーザーが貼るだけにする",
                    "テスト文を用意する",
                    "失敗時の戻し方も示す",
                    "修正対象を一つに絞る",
                    "期待する変化を明確にする",
                    "うまくいかなければ次の層を見る",
                    "今の違和感を設計に変換する",
                    "結果を貼ってもらう",
                    "会話例で確認する",
                    "曖昧さを残したまま進めない",
                    "保存してから次へ進める",
                    "自然さの基準を一つ決める",
                    "別案も軽く残す",
                    "やりすぎを避ける",
                    "今の会話に戻す",
                    "実装後の確認文を出す",
                    "必要なら辞書へ追加する",
                    "ここを基準点にする",
                ]

                self.rhythms = [
                    "短文多め",
                    "やや会話寄り",
                    "説明は少なめ",
                    "一文目を自然に",
                    "見出しは必要時だけ",
                    "箇条書きは少なめ",
                    "技術部分だけ整理",
                    "まず会話、あとで手順",
                    "硬い語を減らす",
                    "断定と確認を混ぜる",
                    "例を一つ挟む",
                    "最初に結論",
                    "最後に次の行動",
                    "語尾を固定しない",
                    "同じ始まりを避ける",
                    "少し余白を作る",
                    "説明より判断を出す",
                    "長くしすぎない",
                    "必要なら深くする",
                    "自然なテンポを優先",
                ]

                self.avoid_patterns = [
                    "毎回ユーザー名を呼ぶ",
                    "好きな色を雑談に出す",
                    "趣味へ勝手に誘導する",
                    "文を丸ごと引用する",
                    "知らないのに知っているふりをする",
                    "略称を普通名詞に分解する",
                    "何でも過去文脈へ結びつける",
                    "毎回同じ褒め方をする",
                    "毎回同じ見出し構成にする",
                    "無関係なNEXUS開発へ戻す",
                    "検索が必要な事実を断言する",
                    "質問に答える前に長く前置きする",
                    "雑談を面接みたいにする",
                    "会話の温度を上げすぎる",
                    "絵文字に頼る",
                    "不自然な比喩を入れる",
                    "相手の言葉を無視して話題転換する",
                    "過去の好みを会話ネタにする",
                    "曖昧語を勝手に確定する",
                    "安全性を軽く扱う",
                ]

            def combination_count(self) -> int:
                return (
                    len(self.opening_styles)
                    * len(self.stances)
                    * len(self.transitions)
                    * len(self.ending_styles)
                    * len(self.rhythms)
                    * len(self.avoid_patterns)
                )

            def pick(self, text: str, mode: str) -> LanguagePalette:
                salt = datetime.now().strftime("%Y%m%d%H")

                return LanguagePalette(
                    opening_style=self._pick(self.opening_styles, text + mode + salt + "opening"),
                    stance=self._pick(self.stances, text + mode + salt + "stance"),
                    transition=self._pick(self.transitions, text + mode + salt + "transition"),
                    ending_style=self._pick(self.ending_styles, text + mode + salt + "ending"),
                    rhythm=self._pick(self.rhythms, text + mode + salt + "rhythm"),
                    avoid_pattern=self._pick(self.avoid_patterns, text + mode + salt + "avoid"),
                    combination_count=self.combination_count(),
                )

            def instruction(self, text: str, mode: str) -> str:
                palette = self.pick(text, mode)

                return (
                    "Language palette for this turn:\n"
                    f"- Opening style: {palette.opening_style}\n"
                    f"- Stance: {palette.stance}\n"
                    f"- Transition tendency: {palette.transition}\n"
                    f"- Ending style: {palette.ending_style}\n"
                    f"- Rhythm: {palette.rhythm}\n"
                    f"- Avoid especially: {palette.avoid_pattern}\n"
                    f"- Current variation space: {palette.combination_count} possible guidance combinations\n"
                    "Use this as guidance, not as text to copy verbatim."
                )

            def _pick(self, items: list[str], seed: str) -> str:
                digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
                index = int(digest[:8], 16) % len(items)
                return items[index]
        ''',
    )


def write_response_dynamics() -> None:
    write(
        "nexus/personality/response_dynamics.py",
        r'''
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
        ''',
    )


def patch_system_prompt() -> None:
    path = ROOT / "prompts/system_prompt.txt"
    if not path.exists():
        write("prompts/system_prompt.txt", "あなたは Project NEXUS です。\n")

    text = path.read_text(encoding="utf-8")
    marker = "# Entity Resolution and Vocabulary Gate v6"

    if marker in text:
        return

    addition = r"""

# Entity Resolution and Vocabulary Gate v6

NEXUSは、略称・固有名詞・複合語を安易に分解してはいけません。

例:
- 東京造形 → 東京造形大学の可能性を先に考える
- 多摩美 → 多摩美術大学
- 武蔵美 / ムサビ → 武蔵野美術大学
- 日芸 → 日本大学芸術学部
- Maya → Autodesk Maya

「〇〇について」「〇〇って知ってる？」のような発言では、
〇〇をまず一つの固有名詞候補として扱います。

知らない場合は、知っているふりをしません。
「それは〇〇のこと？」と軽く確認するか、
「今の情報だけだと断定できない。調べた方がいい」と自然に返します。

会話表現では、固定テンプレートを避けます。
毎回同じ始まり方、同じ褒め方、同じ手順化をしないでください。
ただし、ランダムに崩すのではなく、文脈に合った言い換えを使います。
"""

    path.write_text(text.rstrip() + "\n\n" + addition.lstrip(), encoding="utf-8")


def write_docs() -> None:
    write(
        "docs/ENTITY_RESOLUTION_GATE.md",
        r'''
        # Entity Resolution Gate

        This layer prevents NEXUS from splitting compound terms too aggressively.

        Example:

        Bad:
        - 東京造形 -> 東京 + 造形

        Good:
        - 東京造形 -> likely 東京造形大学

        ## Priority

        1. Exact alias
        2. Possible proper noun
        3. General knowledge
        4. Clarification
        5. Search if available
        ''',
    )

    write(
        "docs/LANGUAGE_BANK_V6.md",
        r'''
        # Language Bank v6

        NEXUS uses a large response guidance combination space.

        The current bank combines:

        - opening style
        - stance
        - transition tendency
        - ending style
        - rhythm
        - avoid pattern

        This creates far more than 100 response guidance combinations.

        The goal is not random speech.
        The goal is contextual variation.
        ''',
    )


def main() -> None:
    if not (ROOT / "main.py").exists() or not (ROOT / "nexus").exists():
        raise SystemExit("Project-NEXUS のルートで実行してください。")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for target in [
        "nexus/ai/manager.py",
        "nexus/personality/response_dynamics.py",
        "nexus/personality/entity_resolver.py",
        "nexus/personality/language_bank.py",
        "prompts/system_prompt.txt",
        "data/entity_aliases.json",
    ]:
        backup(target)

    patch_ai_manager()
    write_entity_aliases()
    write_entity_resolver()
    write_language_bank()
    write_response_dynamics()
    patch_system_prompt()
    write_docs()

    print("Entity Resolution + Language Bank v6 applied.")
    print(f"Backup: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
