"""
Project NEXUS
Core Logger

Responsible for all logging throughout the system.
"""

from pathlib import Path
import logging

# ログフォルダ
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# ログファイル
LOG_FILE = LOG_DIR / "nexus.log"

# ロガー作成
logger = logging.getLogger("NEXUS")
logger.setLevel(logging.INFO)

# 重複防止
if not logger.handlers:

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)