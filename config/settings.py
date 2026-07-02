"""from config.settings import settings
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


settings = Settings()