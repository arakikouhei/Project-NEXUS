"""
Project NEXUS
Global Settings

This file stores global configuration values
used throughout the entire system.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "Project NEXUS"
    VERSION: str = "0.7.0-dev"
    ROADMAP_STAGE: str = "v0.7 file / production support / UI prep"
    AI_NAME: str = "NEXUS"
    LANGUAGE: str = "ja-JP"
    DEBUG: bool = True

    # 使用するAIエンジン
    AI_ENGINE: str = "qwen"
    # 将来は "qwen" に切り替えるだけ


settings = Settings()
