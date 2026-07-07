# Dashboard Backend v1

Dashboard Backend v1 adds the first local backend for the future Project NEXUS dashboard.

## Purpose

The backend allows a future browser dashboard to run safe NEXUS commands through a local API.

This is the first step toward v0.8 dedicated UI / dashboard prototype.

## Files

- nexus/dashboard/__init__.py
- nexus/dashboard/server.py

## Local Server

Default local URL:

- http://127.0.0.1:8765

Run command:

- python3 -m nexus.dashboard.server

Stop:

- Ctrl+C

## API

- GET /
- GET /api/status
- GET /api/run?command=COMMAND
- POST /api/run

## Safety

Dashboard Backend v1 only allows fixed safe commands.

It does not allow:

- shell execution
- arbitrary commands
- file deletion
- file editing
- git commit / push
- backup deletion

Dangerous or unknown commands return:

- Command is not allowed in Dashboard Backend v1.

## Current Status

Implemented:

- Backend class
- Safe command allowlist
- GET /api/status
- GET /api/run
- POST /api/run
- Simple index page
- Dangerous command blocking

Not implemented yet:

- Full frontend dashboard
- Button UI
- File panel
- Status panel
- Production panel
- Voice / camera
