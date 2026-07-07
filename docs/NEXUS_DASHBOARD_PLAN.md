# NEXUS Dashboard Plan

## Purpose

This document defines the future dedicated UI / dashboard direction for Project NEXUS.

The current terminal interface is useful for development, but daily use should eventually move toward a clearer interface with buttons, panels, and simple navigation.

## Current Position

Roadmap position:

- v0.6: Memory system strengthening completed
- v0.7: File / production support / UI preparation in progress
- v0.8: Dedicated UI / interaction layer planned
- v1.0: Practical daily-use NEXUS target

Current v0.7 completed work:

- File Index v1
- File Preview v1

## UI Goal

The NEXUS dashboard should make common actions easy to use without remembering many text commands.

Main goals:

- Show current roadmap position
- Show system health
- Make common commands clickable
- Show memory and knowledge status
- Preview project files safely
- Support creative production workflows
- Prepare for future voice and camera input

## Core Layout

### 1. Chat Panel

Purpose:

- Main conversation area
- User can type normal requests
- NEXUS can answer and execute commands

Possible elements:

- Message history
- Input box
- Send button
- Clear button
- Command suggestion area

---

### 2. Command Button Panel

Purpose:

Common commands should be clickable.

Possible buttons:

- システム健康診断
- コマンド一覧
- おすすめ次操作
- NEXUS現在地
- NEXUS開発状況
- 記憶インデックス
- 記憶レビュー
- 記憶の状態を教えて
- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- tools一覧
- scripts一覧
- バックアップ一覧
- 知識ダイジェスト

---

### 3. Roadmap / Position Panel

Purpose:

Always show where NEXUS is in the whole project.

Display example:

- Overall Roadmap Position
- Current Stage
- Current Feature
- Current Split Step
- Next Recommended Stage

This matches the user's requested workflow style:

- Always show where we are in the full roadmap
- Also show the current local task position

---

### 4. System Health Panel

Purpose:

Show NEXUS stability at a glance.

Possible fields:

- System Health result
- Major command test result
- Git status
- Current branch
- Latest commit
- Backup status
- Known warnings

---

### 5. Memory Panel

Purpose:

Show memory-related information.

Possible sections:

- Project Memory
- Memory Index
- Work Notes
- Memory Review
- Memory Answer
- Snapshot History

Possible buttons:

- NEXUS記憶
- NEXUS現在地
- NEXUSマイルストーン
- 記憶インデックス
- 作業メモ一覧
- 記憶レビュー
- NEXUS記憶履歴

---

### 6. Knowledge Panel

Purpose:

Search and review Knowledge Core.

Possible elements:

- Search box
- Recent knowledge
- Knowledge digest
- Import preview
- Research workflow controls

Possible buttons:

- 知識検索
- 知識ダイジェスト
- 知識回答
- インポート確認
- 研究ワークフロー開始
- 研究まとめ

---

### 7. File Browser Panel

Purpose:

Use v0.7 File Index and File Preview from a visual interface.

Possible elements:

- Important folder list
- docs list
- tools list
- scripts list
- prompts list
- selected file preview

Possible buttons:

- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- data一覧
- tools一覧
- scripts一覧
- prompts一覧
- ファイル確認

Safety:

- Preview only at first
- No delete button in early UI
- Editing should require backups and confirmation

---

### 8. Production Support Panel

Purpose:

Support creative work and project notes.

Possible sections:

- 制作メモ
- 3DCG作業メモ
- Maya作業メモ
- Current creative project
- Daily task list

Possible future commands:

- 制作メモ追加
- 制作メモ一覧
- Maya作業確認
- 今日の制作予定
- 次の制作作業

---

### 9. Backup / Export Panel

Purpose:

Make safety operations easy.

Possible buttons:

- 知識エクスポート
- NEXUSバックアップ
- バックアップ一覧
- システム健康診断
- テスト実行

Safety:

- Backup before editing
- Show latest backup
- Warn before risky changes

---

### 10. Future Voice / Camera Panel

Purpose:

Prepare for future interaction modes.

Possible controls:

- Voice input ON/OFF
- Camera input ON/OFF
- Microphone status
- Camera status
- Permission status

Future use cases:

- Voice commands
- Hands-free project control
- Camera-based object / drawing / screen assistance

This is not implemented in v0.7. It belongs to later stages.

## Suggested UI Technology Options

Possible future choices:

### Option A: Local Web Dashboard

Example stack:

- Python backend
- Local web UI
- Browser-based dashboard

Pros:

- Easy to build step by step
- Works on Mac
- UI can have buttons and panels
- Good for future expansion

Cons:

- Requires local server

### Option B: Desktop App

Example stack:

- Python GUI
- Electron-style app
- Native app wrapper

Pros:

- Feels like a real app
- Can be packaged later

Cons:

- More complex than local web dashboard

### Recommended Direction

Start with a local web dashboard.

Reason:

- Easier to develop safely
- Easier to add panels
- Easier to connect existing command system
- Good bridge from terminal to daily-use UI

## v0.8 Candidate Goal

v0.8 should create the first working dashboard prototype.

Minimum useful prototype:

- Chat panel
- Command buttons
- Roadmap / position display
- System health display
- File index display
- File preview display

## Safety Rules

- UI should call existing safe tools first
- Destructive actions should be disabled early
- Editing files should require backup
- Commands should be logged
- Git state should be visible
- Test results should be visible

## Next Steps After This Document

1. Add UI Preparation docs
2. Add command help entries for UI planning if needed
3. Keep v0.7 focused on file and production support
4. Move actual dashboard implementation to v0.8
