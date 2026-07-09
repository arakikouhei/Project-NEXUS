from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nexus.device.voice_mock import build_voice_mock_response


def main() -> int:
    samples = [
        "今日のNEXUS",
        "ダッシュボードを開きたい",
        "git pushして",
        "制作メモを確認",
    ]

    for sample in samples:
        print(json.dumps(build_voice_mock_response(sample), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
