# System Health v2

Adds Recommended Fixes to Project NEXUS system health output.

## Updated Commands

- システム健康診断
- NEXUS状態確認

## Behavior

System Health v2 appends a `Recommended Fixes` section.

Examples:

- Gitがcleanではない場合、`git status` を促す
- Python compile error がある場合、対象ファイル修正を促す
- Archive Filter が archived include の場合、除外モードをすすめる
- Knowledge Auto Recall がONの場合、通常はOFFをすすめる
- 問題がない場合、通常運用OKと表示する

## Safety

- 状態確認のみ
- ファイル削除なし
- 元データ変更なし
