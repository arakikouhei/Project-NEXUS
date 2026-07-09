from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

checks: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        print(f"  {detail}")


def exists(path: str) -> bool:
    return (PROJECT_ROOT / path).exists()


def run_check(name: str, command: list[str], expected_text: str | None = None) -> None:
    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    output = (result.stdout or "") + (result.stderr or "")
    print(output.strip())

    ok = result.returncode == 0

    if expected_text and expected_text not in output:
        ok = False
        detail = f"missing expected text: {expected_text}"
    else:
        detail = " ".join(command)

    check(name, ok, detail)


def check_git_clean() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )
    output = result.stdout.strip()
    check("Git clean", output == "", output or "working tree clean")


def main() -> int:
    print("Project NEXUS v3.0 Readiness Check")
    print("=" * 70)

    required_files = [
        "docs/V2_1_DAILY_COMMAND_IMPLEMENTATION.md",
        "docs/V2_2_NEXT_ACTION_WORKFLOW.md",
        "docs/V2_3_DASHBOARD_DAILY_PANEL.md",
        "docs/V2_4_SPHERE_DISPLAY_MOCK.md",
        "docs/V2_5_VOICE_IO_MOCK.md",
        "docs/V2_6_DEVICE_STATE_MOCK.md",
        "docs/V2_7_DEVICE_SAFETY_SYSTEM.md",
        "docs/V2_8_LOCAL_AI_CONNECTION_PREP.md",
        "docs/V2_9_INTEGRATED_SOFTWARE_STABILITY.md",
        "docs/RELEASE_SNAPSHOT_V3_0.md",
        "nexus/daily/workflow.py",
        "nexus/device/state.py",
        "nexus/device/sphere_display.py",
        "nexus/device/voice_mock.py",
        "nexus/device/safety.py",
        "scripts/nexus_today.py",
        "scripts/device_state_mock.py",
        "scripts/sphere_display_mock.py",
        "scripts/voice_io_mock.py",
        "scripts/device_safety_check.py",
        "scripts/check_v3_0_readiness.py",
    ]

    for item in required_files:
        check(f"Required v3.0 file: {item}", exists(item))

    run_check("Today NEXUS", [sys.executable, "scripts/nexus_today.py"], "今日のNEXUS")
    run_check("Device State Mock", [sys.executable, "scripts/device_state_mock.py"], "Project NEXUS Sphere Mock")
    run_check("Sphere Display Mock", [sys.executable, "scripts/sphere_display_mock.py"], "NEXUS Sphere Display Mock")
    run_check("Voice IO Mock", [sys.executable, "scripts/voice_io_mock.py"], "mock_response")
    run_check("Device Safety Check", [sys.executable, "scripts/device_safety_check.py"], "Device safety check passed.")
    run_check("Major Command Tests", [sys.executable, "scripts/test_major_commands.py"], "FAIL: 0")
    run_check("System Stability Check", [sys.executable, "scripts/check_system_stability.py"], "FAIL: 0")
    run_check("Release Readiness Check", [sys.executable, "scripts/check_release_readiness.py"], "FAIL: 0")

    subprocess.run(["git", "clean", "-f", "data/project/snapshots/"], cwd=PROJECT_ROOT, text=True)
    check_git_clean()

    passed = sum(1 for _, ok, _ in checks if ok)
    failed = len(checks) - passed

    print()
    print("=" * 70)
    print("v3.0 Readiness Summary")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("v3.0 readiness check failed.")
        return 1

    print("v3.0 readiness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
