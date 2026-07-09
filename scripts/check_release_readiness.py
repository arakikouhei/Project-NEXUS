import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import settings
from nexus.agent.agent import NexusAgent


REQUIRED_DOCS = [
    "docs/RELEASE_SNAPSHOT_V0_6.md",
    "docs/RELEASE_SNAPSHOT_V0_7.md",
    "docs/RELEASE_SNAPSHOT_V0_8.md",
    "docs/V0_9_PLAN.md",
    "docs/DASHBOARD_SAFETY_REVIEW_V1.md",
    "docs/SYSTEM_STABILITY_CHECK_V1.md",
    "docs/INTEGRATED_DASHBOARD_TEST_V1.md",
]

REQUIRED_SCRIPTS = [
    "scripts/test_dashboard_all.py",
    "scripts/check_system_stability.py",
    "scripts/review_dashboard_safety.py",
]


def run_check(command: list[str], label: str) -> bool:
    print("")
    print("=" * 70)
    print(label)
    print("=" * 70)

    result = subprocess.run(command, text=True)

    if result.returncode == 0:
        print(f"[PASS] {label}")
        return True

    print(f"[FAIL] {label}")
    return False


def check_required_files() -> bool:
    print("")
    print("=" * 70)
    print("Required Release Files")
    print("=" * 70)

    ok = True

    for item in REQUIRED_DOCS + REQUIRED_SCRIPTS:
        path = Path(item)
        if path.exists():
            print(f"[PASS] {item}")
        else:
            print(f"[FAIL] missing: {item}")
            ok = False

    return ok


def check_settings() -> bool:
    print("")
    print("=" * 70)
    print("Settings")
    print("=" * 70)

    print("VERSION:", settings.VERSION)
    print("ROADMAP_STAGE:", settings.ROADMAP_STAGE)

    if settings.VERSION and settings.ROADMAP_STAGE:
        print("[PASS] Settings available")
        return True

    print("[FAIL] Settings missing")
    return False


def check_project_memory_position() -> bool:
    print("")
    print("=" * 70)
    print("Project Memory Position")
    print("=" * 70)

    agent = NexusAgent()
    handled, result = agent.process("NEXUS現在地")

    print("handled:", handled)
    print(result or "")

    if (
        handled
        and result
        and "v0.8 dashboard / interaction layer completed" in result
        and "v0.9 planning / stabilization" in result
    ):
        print("[PASS] Project Memory position")
        return True

    print("[FAIL] Project Memory position")
    return False


def check_dashboard_launch_guide() -> bool:
    print("")
    print("=" * 70)
    print("Dashboard Launch Guide")
    print("=" * 70)

    agent = NexusAgent()
    handled, result = agent.process("NEXUSダッシュボード")

    print("handled:", handled)
    print((result or "")[:1200])

    required = [
        "python3 -m nexus.dashboard.server",
        "http://127.0.0.1:8765",
        "does not cost money",
    ]

    if not handled or not result:
        print("[FAIL] Dashboard launch guide not handled")
        return False

    ok = True
    for item in required:
        if item in result:
            print(f"[PASS] contains: {item}")
        else:
            print(f"[FAIL] missing: {item}")
            ok = False

    return ok


def check_git_clean() -> bool:
    print("")
    print("=" * 70)
    print("Git Clean")
    print("=" * 70)

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("[FAIL] git status failed")
        print(result.stderr)
        return False

    output = result.stdout.strip()

    if output:
        print(output)
        print("[WARN] Working tree is not clean")
        return False

    print("working tree clean")
    print("[PASS] Git clean")
    return True


def main() -> int:
    print("Project NEXUS Release Readiness Checklist v1")
    print("Target: prepare for v1.0 planning after v0.9 stabilization")

    checks = [
        check_required_files(),
        check_settings(),
        check_project_memory_position(),
        check_dashboard_launch_guide(),
        run_check([sys.executable, "scripts/test_dashboard_all.py"], "Integrated Dashboard Tests"),
        run_check([sys.executable, "scripts/review_dashboard_safety.py"], "Dashboard Safety Review"),
        run_check([sys.executable, "scripts/check_system_stability.py"], "System Stability Check"),
        check_git_clean(),
    ]

    passed = sum(1 for item in checks if item)
    failed = len(checks) - passed

    print("")
    print("=" * 70)
    print("Release Readiness Summary")
    print("=" * 70)
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("")
        print("Release readiness check failed.")
        return 1

    print("")
    print("Release readiness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
