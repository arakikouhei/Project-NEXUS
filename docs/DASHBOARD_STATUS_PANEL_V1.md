# Dashboard Status Panel v1

Dashboard Status Panel v1 adds visible project status cards to the Project NEXUS dashboard.

## Purpose

The dashboard should always show the current project state without needing to type commands.

This matches the workflow rule:

- Show the whole roadmap position
- Show the current local task position
- Make NEXUS status visible

## Updated Files

- nexus/dashboard/server.py
- nexus/dashboard/static/index.html

## Backend Changes

`/api/status` now returns:

- project_version
- roadmap_stage
- safe_command_count
- current_position
- allowed_commands

Current values:

- project_version: 0.7.0-dev
- roadmap_stage: v0.7 file / production support / UI prep

## Frontend Changes

The dashboard now includes a Status Panel with cards for:

- Project Version
- Roadmap Stage
- Safe Commands
- Backend

## Safety

- Read-only status display
- No destructive actions
- No shell execution
- No file editing
- Uses existing Dashboard Backend safe API
