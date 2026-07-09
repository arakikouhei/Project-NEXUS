from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nexus.daily.workflow import build_today_report


def main() -> int:
    print(build_today_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
