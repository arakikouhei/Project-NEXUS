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
