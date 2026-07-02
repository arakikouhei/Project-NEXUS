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
    VERSION: str = "0.1.0"
    AI_NAME: str = "NEXUS"
    LANGUAGE: str = "ja-JP"
    DEBUG: bool = True

    # 使用するAIエンジン
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
    VERSION: str = "0.1.0"
    AI_NAME: str = "NEXUS"
    LANGUAGE: str = "ja-JP"
    DEBUG: bool = True

    # 使用するAIエンジン
    AI_ENGINE = "qwen"
    # 将来は "qwen" に切り替えるだけ


settings = Settings()
    # 将来は "qwen" に切り替えるだけ


settings = Settings()