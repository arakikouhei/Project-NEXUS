from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nexus.device.safety import classify_action


def main() -> int:
    checks = [
        "今日のNEXUSを表示",
        "ダッシュボード起動方法を表示",
        "git pushして",
        "ファイルを削除して",
        "有料APIを使って",
    ]

    failed = 0

    for item in checks:
        result = classify_action(item)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        if item in {"git pushして", "ファイルを削除して", "有料APIを使って"}:
            if result["auto_execute"]:
                failed += 1

    print("Device safety check summary")
    print(f"FAIL: {failed}")

    if failed:
        print("Device safety check failed.")
        return 1

    print("Device safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
