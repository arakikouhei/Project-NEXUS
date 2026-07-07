# Project NEXUS Release Snapshot v0.8

## Status

Project NEXUS v0.8 dashboard / interaction layer snapshot.

This snapshot marks the stable point after the first dedicated dashboard prototype work.

## Current Stage

- Stage: v0.8 dashboard / interaction layer
- Direction: toward v1.0 practical daily-use version
- Focus: local browser dashboard, safe command buttons, status display, file panel, production panel, and dashboard launch guide

## Completed v0.8 Work

### v0.8 Planning

Created:

- docs/V0_8_PLAN.md

Purpose:

- Defines v0.8 goal
- Plans local web dashboard direction
- Keeps destructive actions out of the dashboard prototype
- Keeps terminal fallback available

---

### Dashboard Backend v1

Created:

- nexus/dashboard/__init__.py
- nexus/dashboard/server.py
- docs/DASHBOARD_BACKEND_V1.md
- scripts/test_dashboard_backend.py

Purpose:

- Provides local dashboard backend
- Runs on `127.0.0.1:8765`
- Exposes `/api/status`
- Exposes `/api/run`
- Uses fixed safe command allowlist
- Blocks dangerous or unknown commands

Run:

```bash
python3 -m nexus.dashboard.server
```

Open:

```text
http://127.0.0.1:8765
```

---

### Dashboard Frontend v1

Created:

- nexus/dashboard/static/index.html
- docs/DASHBOARD_FRONTEND_V1.md
- scripts/test_dashboard_frontend.py

Purpose:

- Adds first browser UI
- Shows command buttons
- Shows result panel
- Calls Dashboard Backend safe API

---

### Dashboard Status Panel v1

Created:

- docs/DASHBOARD_STATUS_PANEL_V1.md
- scripts/test_dashboard_status_panel.py

Updated:

- nexus/dashboard/server.py
- nexus/dashboard/static/index.html

Purpose:

- Shows project version
- Shows roadmap stage
- Shows safe command count
- Shows backend status

---

### Dashboard File Panel v1

Created:

- docs/DASHBOARD_FILE_PANEL_V1.md
- scripts/test_dashboard_file_panel.py

Updated:

- nexus/dashboard/static/index.html

Purpose:

- Adds visual file navigation area
- Uses existing File Index commands
- Keeps file operations read-only

Buttons:

- Important Files
- docs
- tools
- scripts
- prompts
- File Index

---

### Dashboard Production Panel v1

Created:

- docs/DASHBOARD_PRODUCTION_PANEL_V1.md
- scripts/test_dashboard_production_panel.py

Updated:

- nexus/dashboard/static/index.html

Purpose:

- Adds visual creative production support area
- Uses existing Production Support commands

Buttons:

- Production Memos
- Search: Maya
- 3DCG Check
- Maya Memos

---

### Dashboard Launch Command v1

Created:

- nexus/tools/dashboard_launch.py
- docs/DASHBOARD_LAUNCH_COMMAND_V1.md

Updated:

- nexus/tools/manager.py
- nexus/agent/agent.py
- prompts/system_prompt.txt
- scripts/test_major_commands.py

Commands:

- NEXUSダッシュボード
- NEXUSダッシュボード起動方法
- ダッシュボード起動方法

Purpose:

- Shows dashboard start command from inside NEXUS
- Shows local URL
- Shows stop method
- Explains that local dashboard startup itself does not cost money

## Current Test Result

Major command test suite:

- PASS: 77
- FAIL: 0

Dashboard tests:

- Dashboard Backend tests passed
- Dashboard Frontend tests passed
- Dashboard Status Panel tests passed
- Dashboard File Panel tests passed
- Dashboard Production Panel tests passed

## Current Git State

Expected:

- GitHub push completed
- Working tree clean

## Current Latest Commits

Recent v0.8 commits:

- Add dashboard launch command
- Add dashboard production panel
- Add dashboard file panel
- Add dashboard status panel
- Add dashboard frontend
- Add dashboard backend
- Add v0.8 planning document

## Key Safety Rules

Dashboard safety:

1. Fixed safe commands only
2. No shell execution from dashboard
3. No delete actions
4. No file editing
5. No git commit / push buttons
6. No arbitrary command input in early prototype
7. Terminal fallback remains available

Before major changes:

1. Run `知識エクスポート`
2. Run `NEXUSバックアップ`
3. Run `システム健康診断`
4. Run `python3 scripts/test_major_commands.py`

After changes:

1. Run py_compile
2. Run dashboard tests
3. Run major command tests
4. Run tool collision check
5. Commit
6. Push

## Known Notes

- v0.8 is a dashboard prototype, not the final daily-use UI.
- The dashboard is local and runs on the user's Mac.
- Starting the dashboard itself does not cost money.
- The dashboard currently uses safe command buttons only.
- Voice and camera are not implemented yet.
- File editing from dashboard is not implemented yet.
- Production memo add form is not implemented yet.
- Git operations remain terminal-only for now.
- Test commands that create memory snapshots may generate untracked snapshot files; remove unnecessary test snapshots before final clean state.

## Next Recommended Stage

After v0.8 snapshot:

1. Project Memory v0.8 Sync
2. v0.9 planning
3. Dashboard stabilization
4. Interaction safety improvements
5. Later: voice input preparation
6. Later: camera input preparation
7. v1.0 practical daily-use NEXUS

## Full Roadmap Position

- v0.1-v0.3: Foundation completed
- v0.4: Knowledge import and research workflow completed
- v0.5: Consolidation completed
- v0.6: Memory system strengthening completed
- v0.7: File / production support / UI preparation completed
- v0.8: Dedicated UI and interaction layer completed
- v0.9: Integrated testing and stabilization
- v1.0: Practical daily-use NEXUS
