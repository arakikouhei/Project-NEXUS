# Project NEXUS v0.7 Plan

## Current Position

Project NEXUS has reached v0.6 memory strengthening stable.

Confirmed:

- Release Snapshot v0.6 completed
- Memory Index v1 completed
- Project Memory Snapshot v1 completed
- Personal Work Notes v1 completed
- Memory Review v1 completed
- Memory Answer v1 completed
- Project Memory v0.6 Sync completed
- Major Command Test Suite: PASS 55 / FAIL 0
- GitHub push completed
- Working tree clean

## v0.7 Goal

v0.7 focuses on file support, production support, and preparation for a future dedicated UI.

The goal is:

> Make NEXUS more useful for real project work before adding a full dashboard, voice, or camera interface.

## Candidate Features

### 1. File Index v1

Create an index of project files and important folders.

Example commands:

- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- data一覧
- tools一覧

Purpose:

- See project structure quickly
- Find important files without manually searching folders
- Prepare for future UI file browser

Priority: High

---

### 2. File Preview v1

Preview safe text files from inside NEXUS.

Example commands:

- ファイル確認: path
- docs確認: filename
- 設定確認: path

Purpose:

- View docs, configs, and small text files
- Avoid editing at first
- Read-only safety

Priority: High

---

### 3. Production Support v1

Add helper commands for creative work notes and 3DCG production support.

Example commands:

- 制作メモ追加: text
- 制作メモ一覧
- 3DCG作業確認
- Maya作業メモ

Purpose:

- Support real creative workflows
- Separate production notes from system notes
- Prepare for future UI panels

Priority: Medium

---

### 4. UI Preparation v1

Design the future NEXUS Dashboard structure.

Candidate doc:

- docs/NEXUS_DASHBOARD_PLAN.md

Possible panels:

- Chat
- Command buttons
- System Health
- Project Memory
- Knowledge Search
- Research Workflow
- Work Notes
- File Browser
- Backup / Export
- Future Voice
- Future Camera

Priority: High

---

### 5. Version Display Sync v1

The console still displays `0.3.0-alpha`.

Update displayed version or add roadmap stage display.

Example:

- Version: 0.7-dev
- Roadmap Stage: v0.7 planning

Priority: Medium

Reason:

Current boot string is outdated compared to actual roadmap progress.

## Recommended Implementation Order

1. File Index v1
2. File Preview v1
3. UI Preparation v1
4. Production Support v1
5. Version Display Sync v1
6. Release Snapshot v0.7

## v0.7 Stable Conditions

v0.7 can be considered stable when:

- File Index works
- File Preview is read-only and safe
- UI preparation document exists
- Production support notes work or are planned
- Version display is less confusing
- Major command tests pass
- System Health shows no critical issues
- Release Snapshot v0.7 exists
- GitHub push completed
- Working tree clean

## Safety Rules

- Do not allow arbitrary destructive file operations
- File preview should be read-only
- Editing files should be a later feature with backups
- Keep command tests updated
- Run `python3 scripts/test_major_commands.py` after changes
- Commit and push after successful tests

## Future Relation to UI / Voice / Camera

v0.7 prepares the structure for:

- v0.8 Dedicated UI / Dashboard
- v0.9 Voice and Camera integration
- v1.0 Practical daily-use NEXUS

The UI should eventually make common commands clickable:

- System Health
- Command Help
- Knowledge Search
- Research Workflow
- Work Notes
- File Preview
- Backup / Export
- Voice ON/OFF
- Camera ON/OFF
