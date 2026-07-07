# Project NEXUS v0.8 Plan

## Current Position

Project NEXUS has reached v0.7 completed.

Confirmed:

- File Index v1 completed
- File Preview v1 completed
- UI Preparation v1 completed
- Production Support v1 completed
- Version Display Sync v1 completed
- Release Snapshot v0.7 completed
- Project Memory v0.7 Sync completed
- Major Command Test Suite: PASS 74 / FAIL 0
- GitHub push completed
- Working tree clean

## v0.8 Goal

v0.8 focuses on the first dedicated UI / dashboard prototype.

The goal is:

> Make NEXUS easier to use every day by adding a local dashboard with clickable buttons and visible project status.

## Important Direction

v0.8 should not try to become a full polished app immediately.

It should start as a safe local prototype.

Priority:

1. See current NEXUS status visually
2. Click common commands
3. Preview command results
4. Keep terminal fallback available
5. Avoid destructive UI actions at first

## Candidate Implementation

### Local Web Dashboard v1

Recommended direction:

- Python backend
- Local web interface
- Browser-based dashboard
- Uses existing NEXUS command system

Reason:

- Easier than a native desktop app
- Works on Mac
- Can be expanded panel by panel
- Good bridge from terminal to daily-use UI

## Candidate Features

### 1. Dashboard Backend v1

Purpose:

- Start a local server
- Receive dashboard requests
- Call existing NEXUS commands
- Return command results safely

Example future command:

- NEXUSダッシュボード起動

Priority: High

---

### 2. Dashboard Frontend v1

Purpose:

- Simple browser page
- Buttons for common commands
- Text result display

Minimum panels:

- Chat / Command result area
- Command buttons
- Roadmap / current position
- System health
- File tools

Priority: High

---

### 3. Command Button v1

Purpose:

Make common commands clickable.

Initial buttons:

- NEXUS現在地
- システム健康診断
- コマンド一覧
- 記憶インデックス
- 記憶の状態を教えて
- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- tools一覧
- 制作メモ一覧
- 3DCG作業確認

Priority: High

---

### 4. Status Panel v1

Purpose:

Show project status without typing commands.

Fields:

- Current roadmap stage
- Version
- Roadmap Stage
- Latest Git commit
- Test status
- Working tree status
- Recommended next action

Priority: High

---

### 5. File Panel v1

Purpose:

Use v0.7 File Index / File Preview visually.

Features:

- List docs
- List tools
- List scripts
- Preview selected text file
- Read-only at first

Priority: Medium

---

### 6. Production Panel v1

Purpose:

Use Production Support from the dashboard.

Features:

- Show production memos
- Add production memo
- Search production memo
- 3DCG checklist
- Maya memo list

Priority: Medium

---

### 7. Safety Layer v1

Purpose:

Keep dashboard safe.

Rules:

- Read-only by default
- No delete actions
- No arbitrary file editing
- No shell command execution from UI
- Commit / push should remain terminal-only at first
- Any future edit action must require backup and confirmation

Priority: High

## Recommended Implementation Order

1. Dashboard Backend v1
2. Dashboard Frontend v1
3. Command Button v1
4. Status Panel v1
5. File Panel v1
6. Production Panel v1
7. v0.8 Release Snapshot

## v0.8 Stable Conditions

v0.8 can be considered stable when:

- Dashboard can start locally
- Browser page opens
- Buttons can run safe NEXUS commands
- Results are shown in the page
- Current position is visible
- File index / preview can be accessed safely
- No destructive actions exist in dashboard
- Major command tests still pass
- GitHub push completed
- Working tree clean
- Release Snapshot v0.8 exists

## Relationship to Future Voice / Camera

v0.8 should prepare the UI space for voice and camera, but not implement them yet.

Future stages:

- v0.9: interaction stabilization and possible voice/camera preparation
- v1.0: practical daily-use NEXUS

Possible future UI controls:

- Voice input ON/OFF
- Camera input ON/OFF
- Permission status
- Device status
- Input mode selector

## Notes

Terminal remains the main development interface during v0.8.

The dashboard should be treated as a safe prototype, not a replacement for all terminal operations yet.

## Full Roadmap Position

- v0.1-v0.3: Foundation completed
- v0.4: Knowledge import and research workflow completed
- v0.5: Consolidation completed
- v0.6: Memory system strengthening completed
- v0.7: File / production support / UI preparation completed
- v0.8: Dedicated UI and interaction layer in progress
- v0.9: Integrated testing and stabilization
- v1.0: Practical daily-use NEXUS
