# File Preview v1

File Preview v1 adds read-only safe text file preview commands for Project NEXUS v0.7.

## Commands

- ファイル確認: path
- docs確認: filename
- 設定確認: path

## Purpose

- Preview project text files from NEXUS
- Confirm docs, configs, scripts, and JSON files
- Prepare for future dashboard file browser

## Safety

- Read-only
- Does not edit files
- Does not delete files
- Blocks backup folders
- Blocks git and cache folders
- Blocks parent directory traversal
- Blocks unsafe suffixes
- Limits preview size and line count
