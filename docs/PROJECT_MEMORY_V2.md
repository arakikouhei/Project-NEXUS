# Project Memory v2

Adds safe update commands for Project NEXUS project memory.

## Commands

- NEXUS現在地更新: text
- NEXUS次段階更新: text
- NEXUSマイルストーン追加: name | summary
- NEXUS記憶保存状況

## Safety

- Backs up data/project/project_memory.json before updates
- Does not delete milestones
- Milestones are append-only
- Current stage and recommended next stage can be updated
