# Dashboard Frontend v1

Dashboard Frontend v1 adds the first browser-based UI prototype for Project NEXUS v0.8.

## Purpose

The frontend provides a simple local dashboard where safe NEXUS commands can be run with buttons.

This is the first visible step toward a daily-use NEXUS interface.

## Files

- nexus/dashboard/static/index.html
- nexus/dashboard/server.py

## How to Run

```bash
python3 -m nexus.dashboard.server
```

Open in browser:

```text
http://127.0.0.1:8765
```

Stop server:

- Ctrl+C

## Current UI

The dashboard currently includes:

- Header
- Backend status display
- Command button panel
- Result display panel
- Memory command buttons
- File command buttons
- Production command buttons

## Safety

Dashboard Frontend v1 only calls Dashboard Backend v1 APIs.

Current safety rules:

- Fixed safe commands only
- No shell execution
- No delete actions
- No file editing
- No git commit / push buttons
- No arbitrary command input yet

## Implemented Buttons

General:

- NEXUS現在地
- NEXUS開発状況
- システム健康診断
- コマンド一覧
- おすすめ次操作

Memory:

- 記憶インデックス
- 記憶の状態を教えて
- 記憶レビュー

Files:

- ファイルインデックス
- 重要ファイル一覧
- docs一覧
- tools一覧
- scripts一覧
- prompts一覧

Production:

- 制作メモ一覧
- 制作メモ検索: Maya
- 3DCG作業確認
- Maya作業メモ

## Not Implemented Yet

- Full chat input
- File picker
- File preview panel
- Status card layout
- Git status panel
- Test status panel
- Voice / camera controls
- Production memo add form
