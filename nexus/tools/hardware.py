"""
Project NEXUS
Hardware Tool
"""

from nexus.device.mock import MockSphereDevice
from nexus.tools.base_tool import BaseTool


class HardwareTool(BaseTool):
    """Shows pre-sphere hardware readiness."""

    name = "hardware"
    description = "球体AI用ハードウェア準備状況を表示します"

    def __init__(self) -> None:
        self.device = MockSphereDevice()

    def can_handle(self, user_input: str) -> bool:
        keywords = {
            "ハードウェア状態",
            "球体準備",
            "sphere readiness",
            "デバイス状態",
            "球体状態",
        }
        return any(keyword in user_input for keyword in keywords)

    def execute(self, user_input: str) -> str:
        status = self.device.status()

        lines = [
            "## Hardware Status",
            "",
            f"Device: {status['device']}",
            f"Connected: {status['connected']}",
            f"Microphone: {status['microphone']}",
            f"Speaker: {status['speaker']}",
            f"Camera: {status['camera']}",
            f"Sensors: {status['sensors']}",
            f"Motion: {status['motion']}",
            f"Safety: {status['safety']}",
            "",
            "## Sphere Readiness",
            "",
            "- Software Core: ready",
            "- Tool System: ready",
            "- Context System: ready",
            "- Voice Output: basic ready",
            "- Hardware Interface: mock ready",
            "- Real Hardware Control: not enabled",
            "",
            "次の段階では、実機のマイク・スピーカー・カメラを安全層経由で接続します。",
        ]

        return "\n".join(lines)
