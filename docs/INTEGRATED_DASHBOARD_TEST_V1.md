# Integrated Dashboard Test v1

Integrated Dashboard Test v1 adds a single script for running all dashboard-related tests.

## Purpose

v0.9 focuses on integrated testing and stabilization.

Before this, dashboard tests were separate:

- test_dashboard_backend.py
- test_dashboard_frontend.py
- test_dashboard_status_panel.py
- test_dashboard_file_panel.py
- test_dashboard_production_panel.py

This feature adds one integrated runner.

## Script

- scripts/test_dashboard_all.py

## Run

```bash
python3 scripts/test_dashboard_all.py
```

## Expected Result

```text
All dashboard tests passed.
PASS: 5
FAIL: 0
```

## Included Tests

- Dashboard Backend
- Dashboard Frontend
- Dashboard Status Panel
- Dashboard File Panel
- Dashboard Production Panel

## Safety

- Test only
- No dashboard server startup required
- No destructive actions
- No shell commands from dashboard
- Uses existing test scripts
