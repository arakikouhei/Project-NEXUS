# Project NEXUS v0.9 Plan

## Current Position

Project NEXUS has reached v0.8 completed.

Confirmed:

- Dashboard Backend v1 completed
- Dashboard Frontend v1 completed
- Dashboard Status Panel v1 completed
- Dashboard File Panel v1 completed
- Dashboard Production Panel v1 completed
- Dashboard Launch Command v1 completed
- Release Snapshot v0.8 completed
- Project Memory v0.8 Sync completed
- Major Command Test Suite: PASS 77 / FAIL 0
- GitHub push completed
- Working tree clean

## v0.9 Goal

v0.9 focuses on integrated testing, stabilization, and safety before v1.0.

The goal is:

> Make Project NEXUS stable enough to approach practical daily use.

## Main Direction

v0.9 should not add many large new features.

Priority:

1. Verify existing systems work together
2. Improve test coverage
3. Stabilize dashboard behavior
4. Confirm safety boundaries
5. Reduce confusion in commands and version display
6. Prepare v1.0 release conditions

## Candidate Work

### 1. Integrated Dashboard Test v1

Purpose:

- Run all dashboard-related tests together
- Confirm backend, frontend, status panel, file panel, production panel, and launch command are stable

Candidate script:

- scripts/test_dashboard_all.py

Priority: High

---

### 2. System Stability Check v1

Purpose:

- Create a single command or script that checks:
  - major command tests
  - dashboard tests
  - py_compile
  - git status
  - project memory current stage

Candidate command:

- NEXUS安定性確認

Priority: High

---

### 3. Dashboard Safety Review v1

Purpose:

- Verify dashboard safe command allowlist
- Confirm dangerous commands are blocked
- Confirm no delete/edit/git buttons exist
- Confirm local dashboard cost note is clear

Priority: High

---

### 4. Command Map Review v1

Purpose:

- Review major NEXUS commands
- Check duplicates
- Check confusing command names
- Check DashboardTool / DashboardLaunchTool ordering
- Check command help consistency

Priority: Medium

---

### 5. Release Readiness Checklist v1

Purpose:

- Define what must be true before v1.0

Possible checklist:

- Tests pass
- Dashboard opens
- Safe commands only
- Project Memory current
- Release snapshot exists
- Git clean
- Backup workflow clear
- Cost / local behavior explained

Priority: High

---

### 6. v0.9 Release Snapshot

Purpose:

- Save stable v0.9 point before v1.0 planning

Priority: High

## v0.9 Stable Conditions

v0.9 can be considered stable when:

- All major command tests pass
- All dashboard tests pass
- Integrated dashboard test exists
- Stability check exists or is documented
- Dashboard safety review exists
- Release readiness checklist exists
- Project Memory is synced to v0.9 completed
- Release Snapshot v0.9 exists
- GitHub push completed
- Working tree clean

## Safety Rules

- Do not add destructive dashboard actions
- Do not add arbitrary shell execution from dashboard
- Do not add file editing from dashboard unless backup and confirmation exist
- Keep terminal fallback available
- Keep test suite updated
- Commit and push only after tests pass

## Relationship to v1.0

v0.9 is the final stabilization stage before v1.0.

v1.0 should focus on practical daily-use readiness:

- Clear launch flow
- Stable dashboard
- Stable command system
- Clear safety rules
- Reliable memory state
- Reliable backup / test / git workflow

## Full Roadmap Position

- v0.1-v0.3: Foundation completed
- v0.4: Knowledge import and research workflow completed
- v0.5: Consolidation completed
- v0.6: Memory system strengthening completed
- v0.7: File / production support / UI preparation completed
- v0.8: Dedicated UI and interaction layer completed
- v0.9: Integrated testing and stabilization in progress
- v1.0: Practical daily-use NEXUS
