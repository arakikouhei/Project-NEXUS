# Project NEXUS Sphere Transfer Guide

This document explains how to prepare NEXUS data for a future sphere-side environment.

## Goal

The current goal is not to control real sphere hardware yet.

The goal is to make NEXUS transferable at any time.

## Transfer Package

Use this command inside NEXUS:

```text
移行パッケージ作成
```

NEXUS will create:

```text
exports/sphere_transfer_YYYYMMDD_HHMMSS.zip
```

## Included Data

- Source code
- Configuration
- Prompts
- Documentation
- Memory data
- Work log data

## Excluded Data

- Git history
- Logs
- Backups
- Python cache files

## Next Stage

After the physical sphere hardware is ready, this transfer package can be moved to the sphere-side environment.

Real hardware control should only be enabled after Safety Core is implemented.
