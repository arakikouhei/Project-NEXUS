# Project NEXUS v1.0 Plan

## Status

Project NEXUS v1.0 planning document.

This plan defines the direction for moving from v0.9 stabilization to v1.0 practical daily-use readiness.

## Current Position

- v0.8: Dedicated UI / dashboard interaction layer completed
- v0.9: Integrated testing / stabilization completed
- Current stage: v1.0 planning
- Goal: practical daily-use NEXUS

## v1.0 Goal

The goal of v1.0 is to make Project NEXUS useful as a daily local assistant for development, production support, project memory, file awareness, and dashboard-based interaction.

v1.0 should not attempt to become a fully autonomous AI device yet.

It should focus on:

1. reliable local operation
2. clear daily-use commands
3. stable dashboard launch flow
4. project memory accuracy
5. safe file and production support
6. practical next-action guidance

## v1.0 Scope

### Included in v1.0

- Practical daily-use workflow
- Dashboard launch refinement
- Daily assistant commands
- Current task / next task guidance
- Project memory status commands
- File and docs overview commands
- Production support commands
- Stability and release checks
- Clear safety boundaries
- Final v1.0 release snapshot
- Project Memory v1.0 Sync

### Not Included in v1.0

- Voice input
- Voice output
- Camera input
- Autonomous internet access
- Paid API integration
- Dashboard file editing
- Dashboard git commit / push
- Arbitrary shell execution from dashboard
- Hardware device implementation
- Liquid cooling or physical sphere prototype

These can be planned for later versions after v1.0.

## Recommended v1.0 Work Order

### 1. Practical Daily-Use Readiness Review

Create a review that checks whether NEXUS is practically usable every day.

Focus:

- Can the user check the current project state?
- Can the user find the next action?
- Can the user inspect important files?
- Can the user review memory?
- Can the user launch the dashboard?
- Can the user confirm system health?
- Can the user recover safely if something fails?

Expected output:

- docs/PRACTICAL_DAILY_USE_READINESS_V1.md
- scripts/check_daily_use_readiness.py

---

### 2. Final Dashboard Launch Flow Refinement

Improve the dashboard launch guide and local-use explanation.

Focus:

- show exact launch command
- show local URL
- show stop method
- show cost note
- show safety note
- show terminal fallback

Expected commands:

- NEXUSダッシュボード
- NEXUSダッシュボード起動方法
- ダッシュボード起動方法

Expected output:

- docs/FINAL_DASHBOARD_LAUNCH_FLOW_V1.md

---

### 3. Daily Assistant Workflow v1

Create a simple workflow for daily usage.

Expected daily flow:

1. check current NEXUS position
2. check system health
3. check recommended next operation
4. check important files
5. check production notes
6. open dashboard if needed
7. run stability check before saving

Possible commands:

- 今日のNEXUS
- 今日の作業確認
- 次にやること
- 制作メモ確認
- 重要ファイル確認
- ダッシュボード案内

Expected output:

- docs/DAILY_ASSISTANT_WORKFLOW_V1.md

---

### 4. v1.0 Command Set Review

Review commands for daily use.

Focus:

- keep essential commands clear
- identify duplicated commands
- identify old development-only commands
- separate daily commands from maintenance commands
- avoid changing stable commands unnecessarily

Expected output:

- docs/V1_0_COMMAND_SET_REVIEW.md
- optional script if needed

---

### 5. v1.0 Release Readiness

Create a final v1.0 readiness check.

Focus:

- v1.0 plan exists
- daily-use readiness exists
- dashboard launch flow exists
- daily assistant workflow exists
- command review exists
- tests pass
- system stability passes
- release readiness passes
- git is clean

Expected output:

- scripts/check_v1_0_readiness.py
- docs/V1_0_RELEASE_READINESS.md

---

### 6. v1.0 Release Snapshot

Create the v1.0 stable snapshot.

Expected output:

- docs/RELEASE_SNAPSHOT_V1_0.md

---

### 7. Project Memory v1.0 Sync

Update Project Memory after v1.0 completion.

Expected memory state:

- current_stage: v1.0 practical daily-use NEXUS completed
- recommended_next_stage: v1.1 expanded interaction / voice preparation
- latest_confirmed_state updated
- v1.0 milestone added

## Safety Rules for v1.0

1. Dashboard remains local-only.
2. Dashboard must not run arbitrary shell commands.
3. Dashboard must not delete files.
4. Dashboard must not edit files.
5. Dashboard must not run git commit or git push.
6. Terminal remains the safe control point for development operations.
7. Paid API calls must not be added without explicit user approval.
8. Voice, camera, and hardware work remain future scope.

## Success Criteria

v1.0 can be considered complete when:

- major command tests pass
- system stability check passes
- release readiness check passes
- daily-use readiness check passes
- dashboard launch flow is documented
- daily assistant workflow is documented
- command set review is completed
- v1.0 release snapshot is created
- Project Memory is synced to v1.0
- GitHub is up to date
- working tree is clean

## Current Immediate Next Step

Start with:

1. Practical Daily-Use Readiness Review
2. Then Final Dashboard Launch Flow Refinement
3. Then Daily Assistant Workflow v1

## Full Roadmap Position

- v0.1-v0.3: Foundation completed
- v0.4: Knowledge import / research workflow completed
- v0.5: Consolidation completed
- v0.6: Memory strengthening completed
- v0.7: File / production support / UI preparation completed
- v0.8: Dashboard / interaction layer completed
- v0.9: Integrated testing / stabilization completed
- v1.0: Practical daily-use NEXUS in planning
