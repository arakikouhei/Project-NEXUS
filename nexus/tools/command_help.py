"""
Project NEXUS
Command Help Tool v1

Shows grouped command help for Project NEXUS.
"""

from __future__ import annotations

from nexus.tools.base_tool import BaseTool


class CommandHelpTool(BaseTool):
    """Shows grouped command lists."""

    name = "command_help"
    description = "NEXUSの主要コマンドを用途別に表示します"

    def can_handle(self, user_input: str) -> bool:
        text = user_input.strip()

        return text in {
            "コマンド一覧",
            "知識コマンド",
            "論文コマンド",
            "更新コマンド",
            "バックアップコマンド",
            "診断コマンド",
            "おすすめ次操作",
        }

    def execute(self, user_input: str) -> str:
        text = user_input.strip()

        if text == "コマンド一覧":
            return self._all_commands()

        if text == "知識コマンド":
            return self._knowledge_commands()

        if text == "論文コマンド":
            return self._paper_commands()

        if text == "更新コマンド":
            return self._update_commands()

        if text == "バックアップコマンド":
            return self._backup_commands()

        if text == "診断コマンド":
            return self._diagnostic_commands()

        if text == "おすすめ次操作":
            return self._recommended_next_actions()

        return "対応していないヘルプ操作です。"

    def _all_commands(self) -> str:
        return """## NEXUS Command List

用途別コマンド:

### 基本確認
- 診断コマンド
- システム健康診断
- NEXUS状態確認
- 機能一覧
- 設定一覧

### 知識
- 知識コマンド
- 知識検索: query
- 知識横断検索: query
- 知識回答: question
- 知識ダイジェスト

### 論文
- 論文コマンド
- 論文検索: computer graphics
- 論文保存: arXiv ID
- 論文一覧

### 更新情報
- 更新コマンド
- AIニュース更新
- 更新整理: ai
- 更新知識化: ai

### バックアップ
- バックアップコマンド
- 知識エクスポート
- NEXUSバックアップ
- バックアップ一覧

### 次に迷ったら
- おすすめ次操作
"""

    def _knowledge_commands(self) -> str:
        return """## Knowledge Commands

### 基本
- 知識ヘルプ
- 知識追加: category | content
- 知識検索: query
- 知識一覧
- 知識詳細: knowledge-id

### 横断検索
- 知識横断検索: diffusion
- 知識まとめ: diffusion
- 知識関連検索: papers-fafab9fc
- 知識ソース確認: diffusion

### 回答
- 知識回答: PointDiTは何の論文？
- 知識回答: diffusionとは？
- 知識回答: MayaのUVとは？

### 整理
- 知識ダイジェスト
- 知識カテゴリ整理
- 知識重複チェック
- 知識古さチェック
- 知識メンテナンス

### アーカイブ
- 知識アーカイブ候補
- 知識アーカイブ: knowledge-id
- 知識アーカイブ一覧
- 知識復元: knowledge-id

### 設定
- 知識検索設定
- 知識検索アーカイブ含む
- 知識検索アーカイブ除外
- 知識自動参照設定
- 知識自動参照ON
- 知識自動参照OFF
- 知識自動参照テスト: MayaのUV

### 信頼度
- 情報源信頼度一覧
- 情報源信頼度チェック
- 知識信頼度確認: diffusion
- 知識信頼度確認: papers-fafab9fc
"""

    def _paper_commands(self) -> str:
        return """## Paper Commands

### arXiv検索
- 論文ヘルプ
- 論文検索: artificial intelligence
- 論文検索: computer graphics
- 論文検索: 3D reconstruction

### 保存・確認
- 論文保存: arXiv ID
- 論文一覧
- 論文詳細: papers-xxxxxxxx

### 保存済み論文の整理
- 論文要点整理: papers-xxxxxxxx
- 論文キーワード抽出: papers-xxxxxxxx
- 論文3行まとめ: papers-xxxxxxxx
- 論文安全評価: papers-xxxxxxxx

注意:
- v1/v2ではメタ情報とAbstract中心です。
- PDF全文の大量保存はしません。
- arXivは有用ですが査読済みとは限りません。
"""

    def _update_commands(self) -> str:
        return """## World / Update Commands

### 更新取得
- 更新ヘルプ
- 世界情勢更新
- 社会情勢更新
- AIニュース更新
- 3DCGニュース更新
- 開発ニュース更新

### 整理
- 更新ログ一覧
- 更新ログ一覧: ai
- 更新整理: ai
- 更新重要度: ai
- 更新知識化: ai

### 状態
- 知識更新状況
- 更新ソース一覧
- 更新ソース追加: category | name | rss-url | ttl-days

注意:
- RSS/ニュースは時間で古くなります。
- world_update系は補助情報扱いです。
- 重要判断には公式情報や複数ソース確認が必要です。
"""

    def _backup_commands(self) -> str:
        return """## Backup / Export Commands

### 軽め
- 知識エクスポート
- バックアップ一覧

### しっかり保存
- 知識バックアップ
- NEXUSバックアップ

保存先:
- backups/
- exports/

方針:
- 削除しません。
- 元データを書き換えません。
- Gitとは別のローカル保険です。
"""

    def _diagnostic_commands(self) -> str:
        return """## Diagnostic Commands

### システム状態
- システム健康診断
- NEXUS状態確認
- 機能一覧
- 設定一覧

### ツール診断
- ツール順序
- ツール衝突チェック
- ツール診断: コマンド

### Git / テスト
- git状態
- テスト実行

おすすめ:
- 大きい作業前: システム健康診断
- コマンド追加後: ツール衝突チェック
- 保存前: git状態
"""

    def _recommended_next_actions(self) -> str:
        return """## Recommended Next Actions

今のNEXUSで迷った時のおすすめ:

### まず状態確認
1. システム健康診断
2. NEXUS状態確認
3. git状態

### 知識を使う
1. 知識横断検索: query
2. 知識回答: question
3. 知識信頼度確認: query

### 論文を増やす
1. 論文検索: computer graphics
2. 論文保存: arXiv ID
3. 論文3行まとめ: papers-id

### ニュースを入れる
1. AIニュース更新
2. 更新整理: ai
3. 更新知識化: ai

### メンテナンス
1. 知識ダイジェスト
2. 知識重複チェック
3. 知識アーカイブ候補

### 大きな改造前
1. 知識エクスポート
2. NEXUSバックアップ
3. システム健康診断
"""
