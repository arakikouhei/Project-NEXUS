# Project NEXUS Release Snapshot

Version: v0.3.0-alpha / Knowledge Foundation Snapshot  
Date: 2026-07-04

## Overview

This snapshot records the current knowledge-focused state of Project NEXUS.

Project NEXUS now has a local knowledge foundation for:

- saving knowledge
- registering trusted sources
- fetching world/news updates
- searching arXiv papers
- saving paper metadata and abstracts
- analyzing saved papers
- searching knowledge across categories
- creating knowledge digests
- archiving duplicated/old entries safely
- filtering archived entries
- reviewing source trust
- answering with evidence from saved knowledge
- optional auto recall with ON/OFF guard
- system health checks

The current design avoids direct model retraining.  
Instead, NEXUS uses local tools, structured memory, source metadata, and evidence-based retrieval.

---

## Major Features

### Knowledge Core

Commands:

- `知識ヘルプ`
- `知識追加: category | content`
- `知識検索: query`
- `知識一覧`
- `知識詳細: knowledge-id`

Storage:

- `data/knowledge/knowledge.json`

Purpose:

- Stores long-term local knowledge.
- Supports categories such as `papers`, `world`, `3dcg`, `development`, and `general`.

---

### Source Registry

Commands:

- `情報源ヘルプ`
- `情報源一覧`
- `情報源検索: query`
- `情報源追加: category | name | url | note | trust`

Storage:

- `data/knowledge/source_registry.json`

Purpose:

- Registers reliable or useful information sources.
- Supports official documentation, paper sources, 3DCG sources, and development sources.

---

### World Update v1/v2

Commands:

- `更新ヘルプ`
- `世界情勢更新`
- `AIニュース更新`
- `3DCGニュース更新`
- `開発ニュース更新`
- `更新整理: ai`
- `更新重要度: ai`
- `更新知識化: ai`
- `知識更新状況`

Storage:

- `data/knowledge/world_update_sources.json`
- `data/knowledge/world_updates.json`

Purpose:

- Fetches RSS-based updates.
- Stores time-sensitive update logs.
- Organizes updates by topic.
- Saves selected digests into Knowledge Core.

Safety:

- RSS/news items are treated as time-sensitive.
- `world_update_v2` is considered supporting information, not final truth.
- Important claims require official or multiple-source confirmation.

---

### Paper Intake v1/v2

Commands:

- `論文ヘルプ`
- `論文検索: computer graphics`
- `論文保存: arXiv ID`
- `論文一覧`
- `論文詳細: papers-xxxxxxxx`
- `論文要点整理: papers-xxxxxxxx`
- `論文キーワード抽出: papers-xxxxxxxx`
- `論文3行まとめ: papers-xxxxxxxx`
- `論文安全評価: papers-xxxxxxxx`

Purpose:

- Searches arXiv.
- Saves paper metadata and Abstract only.
- Does not bulk-download PDFs.
- Does not redistribute full text.
- Provides simple Abstract-based analysis.

Safety:

- arXiv is useful but not always peer-reviewed.
- Paper content requires original paper confirmation before serious use.
- Licenses must be checked before implementation or commercial use.

---

### Knowledge Search v2

Commands:

- `知識横断検索: diffusion`
- `知識まとめ: diffusion`
- `知識関連検索: papers-fafab9fc`
- `知識ソース確認: diffusion`

Purpose:

- Searches across saved knowledge categories.
- Shows related knowledge.
- Summarizes matched entries.
- Checks source distribution.

---

### Knowledge Digest v1

Commands:

- `知識ダイジェスト`
- `知識カテゴリ整理`
- `知識重複チェック`
- `知識古さチェック`
- `知識メンテナンス`

Purpose:

- Reviews Knowledge Core status.
- Shows category distribution.
- Detects duplicate candidates.
- Detects time-sensitive or old knowledge candidates.
- Does not delete or rewrite entries.

---

### Knowledge Cleanup v1

Commands:

- `知識アーカイブ候補`
- `知識アーカイブ: knowledge-id`
- `知識アーカイブ一覧`
- `知識復元: knowledge-id`

Purpose:

- Archives duplicated or outdated entries safely.
- Uses `archived=true`.
- Does not delete entries.
- Allows restoration.

---

### Archive Filter v1

Commands:

- `知識検索設定`
- `知識検索アーカイブ含む`
- `知識検索アーカイブ除外`

Storage:

- `data/knowledge/search_settings.json`

Purpose:

- Excludes archived entries from normal search and digest operations.
- Allows temporary inclusion of archived entries.

Default:

- `include_archived: false`

---

### Source Trust v1

Commands:

- `情報源信頼度一覧`
- `情報源信頼度チェック`
- `知識信頼度確認: diffusion`
- `知識信頼度確認: papers-fafab9fc`

Purpose:

- Gives heuristic trust scores to saved knowledge.
- Treats official sources and documentation as stronger.
- Treats arXiv as useful but not fully peer-reviewed.
- Treats news/world updates as supporting information.
- Treats manual/user knowledge as needing source confirmation.

---

### Knowledge Answer v1/v2

Commands:

- `知識回答: PointDiTは何の論文？`
- `知識回答: diffusionとは？`
- `知識回答: MayaのUVとは？`

Purpose:

- Answers using saved Knowledge Core entries.
- Shows Evidence ID.
- Shows category, source, match score, and trust score.
- Does not answer if no evidence is found.
- v2 improves Japanese readability while preserving evidence.

---

### Natural Knowledge Answer Routing

Examples:

- `PointDiTって何？`
- `MayaのUVとは？`
- `diffusionについて根拠つきで教えて`

Purpose:

- Routes selected natural knowledge questions to Knowledge Answer.
- Avoids taking over casual chat.
- Works with Auto Recall setting.

---

### Knowledge Auto Recall Guard v1

Commands:

- `知識自動参照設定`
- `知識自動参照ON`
- `知識自動参照OFF`
- `知識自動参照テスト: MayaのUV`
- `知識自動参照テスト: PointDiT`

Storage:

- `data/knowledge/auto_recall_settings.json`

Default:

- `enabled: false`

Purpose:

- Adds ON/OFF guard before automatic knowledge recall.
- Allows testing related knowledge candidates.

---

### Knowledge Auto Recall v1

Behavior:

- Works only when `知識自動参照ON` is enabled.
- Does not hijack existing commands.
- Does not hijack casual chat.
- Does not hijack translation, English practice, or Korean practice.
- Routes only selected domain-like questions to Knowledge Answer.

Examples:

- `PointDiTって何？`
- `MayaのUVってどう使うの？`
- `diffusionって3DCGに関係ある？`

---

### System Health v1

Commands:

- `システム健康診断`
- `NEXUS状態確認`
- `機能一覧`
- `設定一覧`

Purpose:

- Checks Git status.
- Runs Python compile checks.
- Shows Knowledge counts.
- Shows paper count.
- Shows world update log count.
- Shows archive/search settings.
- Shows auto recall setting.
- Shows detected major features.

---

## Current Safety Principles

Project NEXUS currently follows these safety principles:

1. Do not retrain the model directly for new knowledge.
2. Store knowledge locally in structured files.
3. Keep source information whenever possible.
4. Treat news and world updates as temporary and time-sensitive.
5. Treat arXiv as useful but not necessarily peer-reviewed.
6. Keep archive reversible.
7. Avoid deleting knowledge automatically.
8. Do not answer from knowledge when evidence is missing.
9. Allow auto recall only when explicitly enabled.
10. Keep diagnostics available to check system health.

---

## Important Current Commands

Daily / normal checks:

- `システム健康診断`
- `NEXUS状態確認`
- `機能一覧`
- `設定一覧`

Knowledge use:

- `知識検索: query`
- `知識横断検索: query`
- `知識回答: question`
- `知識ダイジェスト`

Papers:

- `論文検索: query`
- `論文保存: arXiv ID`
- `論文一覧`
- `論文3行まとめ: papers-id`

World updates:

- `AIニュース更新`
- `更新整理: ai`
- `更新知識化: ai`

Maintenance:

- `知識重複チェック`
- `知識アーカイブ候補`
- `知識アーカイブ一覧`
- `知識検索設定`
- `知識自動参照設定`

---

## Current Status Summary

As of this snapshot, expected feature status:

- Knowledge Core: enabled
- Source Registry: enabled
- World Update: enabled
- Paper Intake: enabled
- Knowledge Search v2: enabled
- Knowledge Digest v1: enabled
- Knowledge Cleanup v1: enabled
- Archive Filter v1: enabled
- Source Trust v1: enabled
- Knowledge Answer v2: enabled
- Knowledge Auto Recall Guard: enabled
- Knowledge Auto Recall v1: enabled
- System Health v1: enabled

---

## Next Possible Development

Recommended next steps:

1. Improve System Health with automatic issue suggestions.
2. Add release notes generation.
3. Add controlled backup/export commands.
4. Add source registry trust integration into Source Trust.
5. Add paper source expansion beyond arXiv.
6. Add safer multi-source verification for world updates.
7. Add better natural Japanese summarization for knowledge answers.
8. Add tests for all major commands.

---

## Notes

This snapshot is documentation only.  
It does not change runtime behavior.

