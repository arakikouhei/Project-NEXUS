# Dashboard Launch Command v1

Dashboard Launch Command v1 adds NEXUS commands that explain how to launch the local dashboard.

## Commands

- NEXUSダッシュボード
- NEXUSダッシュボード起動方法
- ダッシュボード起動方法

## Purpose

- Show the dashboard launch command from inside NEXUS
- Show the local browser URL
- Show how to stop the server
- Explain that local dashboard startup itself does not cost money

## Launch

```bash
cd /Users/araikouichirou/Documents/Project-NEXUS
python3 -m nexus.dashboard.server
```

Open:

```text
http://127.0.0.1:8765
```

Stop:

```text
Ctrl + C
```

## Safety

- Read-only guide command
- Does not start shell commands automatically
- Does not edit files
- Does not delete files
