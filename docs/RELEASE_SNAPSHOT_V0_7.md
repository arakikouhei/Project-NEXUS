# Project NEXUS Release Snapshot v0.7

## Status

Project NEXUS v0.7 file / production support / UI preparation snapshot.

This snapshot marks the stable point after the v0.7 implementation work.

## Current Stage

- Stage: v0.7 file / production support / UI prep
- Direction: toward v1.0 practical daily-use version
- Focus: project file visibility, safe file preview, production support, dashboard preparation, and version display sync

## Completed v0.7 Work

### File Index v1

Commands:

- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- data一覧
- tools一覧
- scripts一覧
- prompts一覧

Purpose:

- Shows important project directories
- Lists important project files
- Prepares for future dashboard file browser
- Read-only

Docs:

- docs/FILE_INDEX_V1.md

---

### File Preview v1

Commands:

- ファイル確認: path
- docs確認: filename
- 設定確認: path

Purpose:

- Safely previews allowed text files
- Supports docs, prompts, scripts, configs, and JSON files
- Blocks unsafe paths and suffixes
- Read-only

Docs:

- docs/FILE_PREVIEW_V1.md

---

### UI Preparation v1

Created:

- docs/NEXUS_DASHBOARD_PLAN.md

Purpose:

- Defines future dedicated NEXUS dashboard direction
- Plans clickable command buttons
- Plans roadmap / position panel
- Plans system health, memory, knowledge, file browser, production support, backup, voice, and camera panels
- Keeps actual UI implementation for v0.8 or later

Related update:

- docs/V0_7_PLAN.md synced with dashboard planning progress

---

### Production Support v1

Commands:

- 制作メモヘルプ
- 制作メモ追加: text
- 制作メモ一覧
- 制作メモ検索: query
- 制作メモ詳細: memo-id
- 3DCG作業確認
- Maya作業メモ

Purpose:

- Stores creative production notes
- Supports 3DCG / Maya work tracking
- Prepares for future production dashboard panels

Data:

- data/production/production_notes.json

Docs:

- docs/PRODUCTION_SUPPORT_V1.md

---

### Version Display Sync v1

Updated:

- config/settings.py
- nexus/core/core.py

Current values:

- VERSION: 0.7.0-dev
- ROADMAP_STAGE: v0.7 file / production support / UI prep

Purpose:

- Fixes outdated boot display that previously showed 0.3.0-alpha
- Adds roadmap stage display at startup

Docs:

- docs/VERSION_DISPLAY_SYNC_V1.md

## Current Test Result

Major command test suite:

- PASS: 74
- FAIL: 0

Run command:

```bash
python3 scripts/test_major_commands.py
```

## Current Git State

Expected:

- GitHub push completed
- Working tree clean

## Current Latest Commits

Recent v0.7 commits:

- Sync version display for v0.7
- Add production support tool
- Sync v0.7 plan with dashboard planning
- Add NEXUS dashboard plan
- Add file preview tool
- Add file index tool

## Key Safety Rules

Before major changes:

1. Run `知識エクスポート`
2. Run `NEXUSバックアップ`
3. Run `システム健康診断`
4. Run `python3 scripts/test_major_commands.py`

After changes:

1. Run py_compile
2. Run major command tests
3. Run tool collision check
4. Commit
5. Push

## Known Notes

- v0.7 is still a development stage, not v1.0.
- Actual dedicated UI is not implemented yet.
- Dashboard implementation is planned for v0.8 or later.
- Voice and camera are future stages, not v0.7.
- File Preview is read-only and intentionally blocks risky paths.
- Production notes are separate from Project Memory and Work Notes.
- Test commands that create memory snapshots may generate untracked snapshot files; remove unnecessary test snapshots before final clean state.

## Next Recommended Stage

After v0.7 snapshot:

1. Project Memory v0.7 Sync
2. v0.8 planning
3. Dedicated UI / dashboard prototype
4. Later: voice input
5. Later: camera input
6. Later: daily-use NEXUS dashboard

## Full Roadmap Position

- v0.1-v0.3: Foundation completed
- v0.4: Knowledge import and research workflow completed
- v0.5: Consolidation completed
- v0.6: Memory system strengthening completed
- v0.7: File / production support / UI preparation completed
- v0.8: Dedicated UI and interaction layer
- v0.9: Integrated testing and stabilization
- v1.0: Practical daily-use NEXUS
