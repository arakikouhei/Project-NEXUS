"""
Project NEXUS
Mock Sphere Device
"""

from nexus.device.interface import DeviceInterface


class MockSphereDevice(DeviceInterface):
    """Mock device used before real sphere hardware is connected."""

    def status(self) -> dict:
        return {
            "device": "Mock Sphere Device",
            "connected": False,
            "microphone": "not connected",
            "speaker": "software voice only",
            "camera": "not connected",
            "sensors": "not connected",
            "motion": "disabled",
            "safety": "hardware control disabled",
        }

    def is_connected(self) -> bool:
        return False
