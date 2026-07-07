# Project NEXUS v0.5 Plan

## Current Position

Project NEXUS is currently in v0.4 active.

Recent completed work:

- Knowledge Import v1
- Research Workflow v1
- Project Memory v2
- Safe Refactor v1
- Major Command Test Suite: PASS 26 / FAIL 0
- GitHub saved
- Working tree clean

## v0.5 Goal

v0.5 should become a stable consolidation release.

The goal is:

> Make the current v0.4 feature set easier to maintain, easier to verify, and safer to extend.

## v0.5 Priorities

### 1. System Health v3

Improve system health so it can detect more project conditions.

Candidate checks:

- Major test suite status
- Project memory stage
- Latest release plan file
- Backup/export availability
- Git identity warning note
- Refactor status

Priority: High

Reason:

System Health is the safety dashboard.

---

### 2. Command Help v2

Update command help to include newer v0.4 commands.

Add or confirm:

- Knowledge Import commands
- Research Workflow commands
- Project Memory v2 commands
- Safe Refactor documentation reference
- Test suite command

Priority: High

Reason:

Commands are increasing. Help must stay current.

---

### 3. Project Memory Sync v1

Update project memory to reflect v0.5 planning.

Candidate update:

- current_stage: v0.5 planning
- recommended_next_stage: System Health v3
- milestone: Safe Refactor v1 completed

Priority: Medium

Reason:

Project Memory should match actual project status.

---

### 4. Test Suite v2

Expand major command tests after new help and health features.

Candidate additions:

- v0.5 plan existence check
- command help newer command check
- project memory v2 update command checks
- research workflow duplicate handling check

Priority: Medium

Reason:

More features need broader safety tests.

---

### 5. Release Snapshot v0.5

Create a release snapshot after v0.5 features are complete.

Candidate file:

- docs/RELEASE_SNAPSHOT_V0_5.md

Priority: Final step

Reason:

Marks a stable recovery point.

## Recommended Implementation Order

1. System Health v3
2. Command Help v2
3. Project Memory Sync v1
4. Test Suite v2
5. Release Snapshot v0.5

## v0.5 Stable Conditions

v0.5 can be considered stable when:

- Major command tests pass
- System Health reports no critical issues
- Project Memory shows v0.5 stable or v0.5 completed
- Command Help includes current commands
- Release snapshot exists
- GitHub push completed
- Working tree clean

## Safety Rules

Before large changes:

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
