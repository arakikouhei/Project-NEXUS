class DashboardLaunchTool:
    """Dashboard launch guide tool for Project NEXUS."""

    COMMANDS = {
        "NEXUSダッシュボード",
        "NEXUSダッシュボード起動方法",
        "ダッシュボード起動方法",
    }

    def can_handle(self, text: str) -> bool:
        return text.strip() in self.COMMANDS

    def execute(self, text: str) -> str:
        return self.handle(text)

    def handle(self, text: str) -> str:
        return """## NEXUS Dashboard

Project NEXUS dashboard launch guide.

### Start

Run this in Mac terminal:

```bash
cd /Users/araikouichirou/Documents/Project-NEXUS
python3 -m nexus.dashboard.server
```

### Open

Open this URL in Safari or Chrome:

```text
http://127.0.0.1:8765
```

### Stop

In the terminal running the dashboard server:

```text
Ctrl + C
```

### Current Dashboard Features

- Safe local backend
- Browser frontend
- Command buttons
- Status panel
- File panel
- Production panel
- Result display

### Cost

Starting this dashboard itself does not cost money.

Reason:

- It runs locally on your Mac
- `127.0.0.1` means your own computer
- The dashboard uses fixed safe local NEXUS commands

Note:

If a future dashboard button calls an external paid AI API, that API part may cost money.
Dashboard Backend v1 currently focuses on safe local commands.
"""
