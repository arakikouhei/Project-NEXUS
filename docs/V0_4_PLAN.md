# Project NEXUS v0.4 Plan

## Current Stable Point

Project NEXUS is currently at a stable v0.3.5-level state.

Confirmed:

- Knowledge Foundation completed
- Release Snapshot completed
- Backup / Export v1 completed
- Command Help v1 completed
- Major Command Test Suite completed
- System Health v2 completed
- Project Memory v1 completed
- Major command tests: PASS 19 / FAIL 0
- Git working tree clean

## v0.4 Goal

v0.4 should improve how NEXUS grows safely from a knowledge-capable local AI into a more practical research and project assistant.

The main goal is:

> Make NEXUS better at taking in information, organizing it, and using it safely.

## Candidate Features

### 1. Knowledge Import v1

Import text files or markdown notes into Knowledge Core.

Example commands:

- 知識インポート: path
- メモ取り込み: path
- インポート候補確認: path

Purpose:

- Take local notes into NEXUS knowledge
- Preserve source path
- Avoid overwriting existing knowledge
- Add category and tags safely

Priority: High

Reason:

This directly strengthens the knowledge system.

---

### 2. Research Workflow v1

Create a guided workflow:

1. Search paper
2. Save paper
3. Summarize
4. Extract keywords
5. Convert to knowledge

Example commands:

- 研究ワークフロー開始: topic
- 論文から知識化: papers-id
- 研究まとめ: topic

Priority: High

Reason:

This connects Paper Intake and Knowledge Core.

---

### 3. Safe Refactor v1

Clean up accumulated safe patches and organize code.

Targets:

- knowledge.py monkey patches
- diagnostics.py patches
- agent.py routing blocks
- command lists

Priority: Medium

Reason:

Important for long-term maintenance, but should be done carefully after backups and tests.

---

### 4. Project Memory v2

Make Project Memory updateable.

Example commands:

- NEXUSマイルストーン追加
- NEXUS現在地更新
- NEXUS次段階更新

Priority: Medium

Reason:

Useful, but editing project memory needs safety checks.

---

## Recommended Implementation Order

1. Knowledge Import v1
2. Research Workflow v1
3. Project Memory v2
4. Safe Refactor v1

## Safety Rules for v0.4

Before any major change:

1. Run `知識エクスポート`
2. Run `NEXUSバックアップ`
3. Run `システム健康診断`
4. Run `python3 scripts/test_major_commands.py`

After implementation:

1. Run Python compile checks
2. Run major command tests
3. Run tool collision check
4. Commit with a clear message
5. Push to GitHub

## Current Recommendation

Start v0.4 with:

> Knowledge Import v1

This is the safest and most useful next feature.
