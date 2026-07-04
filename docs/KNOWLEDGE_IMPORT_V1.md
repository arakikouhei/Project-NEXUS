# Knowledge Import v1

Adds safe local text / markdown import into Project NEXUS Knowledge Core.

## Commands

- インポート確認: path
- 知識インポート: path
- メモ取り込み: path

## Supported Files

- .txt
- .md
- .markdown

## Safety

- Does not delete source files
- Does not overwrite existing knowledge
- Saves source_path and digest
- Skips duplicate digest or source_path
- v1 limit: 300KB
