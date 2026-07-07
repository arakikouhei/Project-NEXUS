# Version Display Sync v1

Version Display Sync v1 updates the Project NEXUS boot/version display for v0.7.

## Purpose

The console previously displayed:

- Version: 0.3.0-alpha

This was outdated compared to the current roadmap stage.

## Updated Settings

File:

- config/settings.py

Current values:

- VERSION: 0.7.0-dev
- ROADMAP_STAGE: v0.7 file / production support / UI prep
- AI_ENGINE: qwen

## Updated Boot Display

File:

- nexus/core/core.py

Boot display now shows:

- Project name
- NEXUS Core
- Version
- Roadmap Stage
- Status

## Reason

Project NEXUS has already completed:

- v0.6 memory strengthening stable
- File Index v1
- File Preview v1
- UI Preparation v1
- Production Support v1

So the boot display needed to match the actual roadmap progress.

## Safety

- No command behavior changed
- No data migration
- Only version / roadmap display settings were updated
