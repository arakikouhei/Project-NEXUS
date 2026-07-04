"""
Project NEXUS
Device Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class DeviceInterface(ABC):
    """Base interface for future physical devices."""

    @abstractmethod
    def status(self) -> dict:
        """Return device status."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return whether the device is connected."""
