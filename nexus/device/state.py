from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class DeviceState:
    device_name: str
    mode: str
    power: str
    battery_level: int
    temperature_c: float
    network: str
    storage: str
    safety: str
    hardware_ready: bool
    note: str
    updated_at: str


def build_device_state() -> dict:
    state = DeviceState(
        device_name="Project NEXUS Sphere Mock",
        mode="software_mock",
        power="external_mac_power",
        battery_level=100,
        temperature_c=35.0,
        network="local_only",
        storage="project_files",
        safety="safe_mock_mode",
        hardware_ready=False,
        note="実物ハードウェアなし。Mac上のソフトウェアモック。",
        updated_at=datetime.now().replace(microsecond=0).isoformat(),
    )
    return asdict(state)


if __name__ == "__main__":
    import json
    print(json.dumps(build_device_state(), ensure_ascii=False, indent=2))
