# Project NEXUS v0.6 Plan

## Current Position

Project NEXUS has reached v0.5 consolidation stable.

Confirmed:

- Release Snapshot v0.5 completed
- System Health v3 completed
- Command Help v2 completed
- Project Memory Sync v1 completed
- Test Suite v2: PASS 36 / FAIL 0
- GitHub push completed
- Working tree clean
- Git identity configured

## v0.6 Goal

v0.6 focuses on strengthening memory.

The goal is:

> Make NEXUS better at remembering project state, user-created notes, research context, and ongoing work without becoming noisy or unsafe.

## Candidate Features

### 1. Memory Index v1

Create a clearer index of important memory-related files and entries.

Targets:

- data/project/project_memory.json
- data/knowledge/knowledge.json
- data/knowledge/source_registry.json
- docs release snapshots
- imported local notes
- research notes

Example commands:

- 記憶インデックス
- 記憶カテゴリ一覧
- 記憶重要項目

Priority: High

---

### 2. Project Memory Snapshot v1

Create a command that saves the current Project Memory state as a dated snapshot.

Example commands:

- NEXUS記憶スナップショット
- NEXUS記憶履歴
- NEXUS記憶復元候補

Priority: High

---

### 3. Personal Work Notes v1

Create a safe area for user work notes, separate from system knowledge.

Example commands:

- 作業メモ追加: text
- 作業メモ一覧
- 作業メモ検索: query
- 作業メモ知識化: memo-id

Priority: Medium

---

### 4. Memory Review v1

Review memory for outdated, duplicate, or risky entries.

Example commands:

- 記憶レビュー
- 古い記憶候補
- 重複記憶候補
- 記憶安全確認

Priority: Medium

---

### 5. Memory Answer v1

Allow NEXUS to answer questions using project memory and knowledge together.

Example commands:

- 記憶回答: question
- NEXUSは今どこまで進んだ？
- 次に何を作るべき？

Priority: Medium

## Recommended Implementation Order

1. Memory Index v1
2. Project Memory Snapshot v1
3. Personal Work Notes v1
4. Memory Review v1
5. Memory Answer v1

## v0.6 Stable Conditions

v0.6 can be considered stable when:

- Memory Index works
- Project Memory snapshots work
- Work notes can be added and searched
- Memory review does not delete anything automatically
- Major command tests pass
- System Health confirms no critical issues
- Release Snapshot v0.6 exists
- GitHub push completed
- Working tree clean

## Safety Rules

- Do not delete memory automatically
- Prefer archive / snapshot over overwrite
- Before memory-related changes, run NEXUSバックアップ
- After changes, run python3 scripts/test_major_commands.py
- Keep Auto Recall OFF by default
- Keep Archive Filter excluding archived entries by default

## Future Relation to UI

v0.6 memory improvements should prepare for a future dedicated UI / dashboard.

Later UI should be able to show:

- Current NEXUS stage
- Recent project memory
- Important work notes
- Research notes
- Health status
- Next recommended action
