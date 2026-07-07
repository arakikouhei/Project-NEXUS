"""
Project NEXUS
Agent
"""

from nexus.agent.planner import SimplePlanner
from nexus.core.input_normalizer import InputNormalizer
from nexus.tools.manager import ToolManager
from nexus.personality.response_dynamics import ResponseDynamicsCore


class NexusAgent:
    """Controls high-level thinking."""

    def __init__(self) -> None:
        self.tools = ToolManager()
        self.planner = SimplePlanner()
        self.response_dynamics = ResponseDynamicsCore()
        self.normalizer = InputNormalizer()

    def process(self, user_input: str) -> tuple[bool, str | None]:
        # VISION_ROUTING_BYPASS_V2
        # 画像系コマンドは InputNormalizer より前に VisionTool へ渡す。
        stripped_input = user_input.strip()
        vision_prefixes = (
            "画像ヘルプ",
            "vision help",
            "画像安全確認:",
            "画像安全確認：",
            "画像分析:",
            "画像分析：",
            "画像意味分析:",
            "画像意味分析：",
        )

        if stripped_input.startswith(vision_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # KNOWLEDGE_ROUTING_BYPASS_V1
        # 知識系コマンドは InputNormalizer により「ヘルプ」へ誤補正される可能性があるため、
        # 正規化前にKnowledgeToolへ渡す。
        knowledge_prefixes = (
            "知識ヘルプ",
            "知識カテゴリ",
            "知識一覧",
            "知識追加:",
            "知識追加：",
            "知識検索:",
            "知識検索：",
            "知識詳細:",
            "知識詳細：",
            "知識横断検索:",
            "知識横断検索：",
            "知識まとめ:",
            "知識まとめ：",
            "知識関連検索:",
            "知識関連検索：",
            "知識ソース確認:",
            "知識ソース確認：",
        )

        if stripped_input.startswith(knowledge_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # SOURCE_REGISTRY_ROUTING_BYPASS_V1
        # 情報源系コマンドはInputNormalizerより前に専用ツールへ渡す。
        source_prefixes = (
            "情報源ヘルプ",
            "情報源カテゴリ",
            "情報源一覧",
            "情報源追加:",
            "情報源追加：",
            "情報源検索:",
            "情報源検索：",
            "情報源詳細:",
            "情報源詳細：",
        )

        if stripped_input.startswith(source_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # WORLD_UPDATE_ROUTING_BYPASS_V1
        update_prefixes = (
            "更新ヘルプ",
            "知識更新状況",
            "更新ソース一覧",
            "更新ログ一覧",
            "更新ログ一覧:",
            "更新ログ一覧：",
            "更新ソース追加:",
            "更新ソース追加：",
            "更新整理:",
            "更新整理：",
            "更新重要度:",
            "更新重要度：",
            "更新知識化:",
            "更新知識化：",
            "世界情勢更新",
            "社会情勢更新",
            "AIニュース更新",
            "3DCGニュース更新",
            "開発ニュース更新",
        )

        if stripped_input.startswith(update_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # KNOWLEDGE_ANSWER_POLISH_V1
        def looks_like_knowledge_question(value: str) -> bool:
            stripped = value.strip()

            if not stripped:
                return False

            # 既存の明示コマンドは邪魔しない
            command_prefixes = (
                "知識",
                "論文",
                "画像",
                "更新",
                "情報源",
                "安全検索",
                "調べて",
                "web",
                "url",
                "git",
                "コミット",
                "テスト",
                "計算",
                "単位変換",
                "アプリ",
                "ダッシュボード",
                "できること",
                "exit",
                "quit",
                "終了",
            )

            if stripped.startswith(command_prefixes):
                return False

            question_markers = (
                "とは",
                "って何",
                "ってなに",
                "は何",
                "はなに",
                "について教えて",
                "根拠つきで",
                "根拠付きで",
            )

            known_terms = (
                "PointDiT",
                "diffusion",
                "Diffusion",
                "Maya",
                "UV",
                "arXiv",
                "geometry",
                "3DCG",
            )

            return (
                any(marker in stripped for marker in question_markers)
                and any(term in stripped for term in known_terms)
            )

        # KNOWLEDGE_ANSWER_POLISH_RESPECT_AUTO_RECALL_V1
        def polish_auto_recall_enabled() -> bool:
            import json
            from pathlib import Path

            settings_path = Path("data/knowledge/auto_recall_settings.json")

            if not settings_path.exists():
                return False

            try:
                data = json.loads(settings_path.read_text(encoding="utf-8"))
                return bool(data.get("enabled", False))
            except Exception:
                return False

        if polish_auto_recall_enabled() and looks_like_knowledge_question(stripped_input):
            knowledge_query = f"知識回答: {stripped_input}"
            result = self.tools.execute(knowledge_query)

            if result is not None:
                return True, result

        # SYSTEM_HEALTH_ROUTING_BYPASS_V1
        system_health_commands = (
            "システム健康診断",
            "NEXUS状態確認",
            "機能一覧",
            "設定一覧",
            "NEXUSバックアップ",
            "知識バックアップ",
            "知識エクスポート",
            "バックアップ一覧",
            "コマンド一覧",
            "知識コマンド",
            "論文コマンド",
            "更新コマンド",
            "バックアップコマンド",
            "診断コマンド",
            "おすすめ次操作",
            "研究コマンド",
            "インポートコマンド",
            "NEXUS記憶コマンド",
            "開発コマンド",
            "記憶インデックス",
            "記憶カテゴリ一覧",
            "記憶重要項目",
            "記憶ファイル一覧",
            "NEXUS記憶",
            "NEXUS開発状況",
            "NEXUS現在地",
            "NEXUSマイルストーン",
            "NEXUS現在地更新:",
            "NEXUS次段階更新:",
            "NEXUSマイルストーン追加:",
            "NEXUS記憶保存状況",
            "知識インポート:",
            "メモ取り込み:",
            "インポート確認:",
            "研究ワークフロー開始:",
            "論文ワークフロー:",
            "論文から知識化:",
            "研究まとめ:",
        )

        if stripped_input in system_health_commands:
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        # KNOWLEDGE_AUTO_RECALL_V1
        def auto_recall_enabled() -> bool:
            import json
            from pathlib import Path

            settings_path = Path("data/knowledge/auto_recall_settings.json")

            if not settings_path.exists():
                return False

            try:
                data = json.loads(settings_path.read_text(encoding="utf-8"))
                return bool(data.get("enabled", False))
            except Exception:
                return False

        def should_auto_recall(value: str) -> bool:
            stripped = value.strip()

            if not stripped:
                return False

            # 既存コマンドは絶対に邪魔しない
            command_prefixes = (
                "知識",
                "論文",
                "画像",
                "更新",
                "情報源",
                "安全検索",
                "調べて",
                "web",
                "url",
                "git",
                "コミット",
                "テスト",
                "計算",
                "単位変換",
                "アプリ",
                "ダッシュボード",
                "できること",
                "exit",
                "quit",
                "終了",
            )

            if stripped.startswith(command_prefixes):
                return False

            # 雑談・英語練習っぽいものは奪わない
            casual_blockers = (
                "疲れた",
                "眠い",
                "おはよう",
                "こんにちは",
                "こんばんは",
                "ありがとう",
                "英語で",
                "英訳",
                "翻訳",
                "発音",
                "韓国語",
            )

            if any(word in stripped for word in casual_blockers):
                return False

            question_markers = (
                "とは",
                "って何",
                "ってなに",
                "は何",
                "はなに",
                "について教えて",
                "根拠つきで",
                "根拠付きで",
                "どう使う",
                "関係ある",
                "何の論文",
            )

            domain_hints = (
                "Maya",
                "UV",
                "PointDiT",
                "diffusion",
                "Diffusion",
                "arXiv",
                "3DCG",
                "geometry",
                "ジオメトリ",
                "論文",
            )

            return (
                any(marker in stripped for marker in question_markers)
                and any(hint in stripped for hint in domain_hints)
            )

        if auto_recall_enabled() and should_auto_recall(stripped_input):
            knowledge_query = f"知識回答: {stripped_input}"
            result = self.tools.execute(knowledge_query)

            if result is not None and "根拠になる知識が見つかりませんでした" not in result:
                return True, result

        # PAPER_INTAKE_ROUTING_BYPASS_V1
        paper_prefixes = (
            "論文ヘルプ",
            "論文一覧",
            "論文検索:",
            "論文検索：",
            "論文保存:",
            "論文保存：",
            "論文詳細:",
            "論文詳細：",
            "論文要点整理:",
            "論文要点整理：",
            "論文キーワード抽出:",
            "論文キーワード抽出：",
            "論文3行まとめ:",
            "論文3行まとめ：",
            "論文安全評価:",
            "論文安全評価：",
        )

        if stripped_input.startswith(paper_prefixes):
            result = self.tools.execute(stripped_input)

            if result is not None:
                return True, result

            return False, None

        normalized = self.normalizer.normalize(user_input)

        result = self.tools.execute(normalized.text)

        if result is not None:
            if normalized.corrected:
                return (
                    True,
                    f"入力補正: {normalized.original} → {normalized.text}\n\n{result}",
                )

            return True, result

        return False, None

    def plan(self, user_input: str) -> list[str]:
        normalized = self.normalizer.normalize(user_input)
        return self.planner.plan(normalized.text)
