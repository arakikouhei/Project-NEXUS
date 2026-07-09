# Release Readiness Checklist v1

Release Readiness Checklist v1 defines the conditions Project NEXUS should satisfy before moving toward v1.0 planning.

## Purpose

v0.9 focuses on integrated testing and stabilization.

This checklist verifies that the project has enough stability to approach practical daily-use readiness.

## Script

- scripts/check_release_readiness.py

## Run

```bash
python3 scripts/check_release_readiness.py
```

## Checks

The script checks:

- Required release documents exist
- Required v0.9 stabilization scripts exist
- Version / Roadmap Stage settings exist
- Project Memory current position is v0.8 completed / v0.9 next
- Dashboard launch guide exists and explains:
  - start command
  - local URL
  - cost note
- Integrated dashboard tests pass
- Dashboard safety review passes
- System stability check passes
- Git working tree is clean

## Expected Result

```text
Release readiness check passed.
PASS: 8
FAIL: 0
```

## v1.0 Readiness Direction

Before v1.0, Project NEXUS should have:

- stable dashboard launch flow
- safe command allowlist
- passing major command tests
- passing dashboard tests
- passing system stability check
- passing safety review
- clean Project Memory state
- release snapshots
- clean Git state
- clear explanation that local dashboard startup itself does not cost money

## Safety

- Check only
- No destructive actions
- Does not edit files
- Does not delete files
- Does not commit or push
