import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import settings
from nexus.agent.agent import NexusAgent


def run_command(command: list[str], label: str) -> bool:
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


def check_settings() -> bool:
    print("")
    print("=" * 70)
    print("Version / Roadmap Stage")
    print("=" * 70)

    print("VERSION:", settings.VERSION)
    print("ROADMAP_STAGE:", settings.ROADMAP_STAGE)

    ok = bool(settings.VERSION) and bool(settings.ROADMAP_STAGE)

    if ok:
        print("[PASS] Version settings")
        return True

    print("[FAIL] Version settings")
    return False


def check_project_memory() -> bool:
    print("")
    print("=" * 70)
    print("Project Memory Current Position")
    print("=" * 70)

    agent = NexusAgent()
    handled, result = agent.process("NEXUS現在地")

    print("handled:", handled)
    print(result or "")

    if handled and result and "Current Stage" in result and "v1.0 practical daily-use NEXUS completed" in result:
        print("[PASS] Project Memory current stage")
        return True

    print("[FAIL] Project Memory current stage")
    return False



def clean_test_snapshots() -> bool:
    print("")
    print("=" * 70)
    print("Clean Test Snapshots")
    print("=" * 70)

    snapshot_dir = Path("data/project/snapshots")
    if not snapshot_dir.exists():
        print("snapshot directory missing; nothing to clean")
        print("[PASS] Clean test snapshots")
        return True

    result = subprocess.run(
        ["git", "clean", "-f", "data/project/snapshots/"],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("[FAIL] git clean for test snapshots failed")
        print(result.stderr)
        return False

    output = result.stdout.strip()
    if output:
        print(output)
    else:
        print("no untracked test snapshots to clean")

    print("[PASS] Clean test snapshots")
    return True


def check_git_status() -> bool:
    print("")
    print("=" * 70)
    print("Git Status")
    print("=" * 70)

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("[FAIL] git status command failed")
        print(result.stderr)
        return False

    output = result.stdout.strip()

    if output:
        print(output)
        print("[WARN] Working tree is not clean")
        return False

    print("working tree clean")
    print("[PASS] Git status")
    return True


def check_project_memory_file() -> bool:
    print("")
    print("=" * 70)
    print("Project Memory File")
    print("=" * 70)

    path = Path("data/project/project_memory.json")

    if not path.exists():
        print("[FAIL] project_memory.json missing")
        return False

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("[FAIL] project_memory.json invalid JSON")
        return False

    current_stage = data.get("current_stage", "")
    next_stage = data.get("recommended_next_stage", "")

    print("current_stage:", current_stage)
    print("recommended_next_stage:", next_stage)

    if current_stage == "v1.0 practical daily-use NEXUS completed" and next_stage == "v1.1 expanded interaction / daily command refinement":
        print("[PASS] Project Memory file")
        return True

    print("[FAIL] Project Memory file")
    return False


def main() -> int:
    print("Project NEXUS System Stability Check v1")

    checks = [
        check_settings(),
        check_project_memory_file(),
        check_project_memory(),
        run_command([sys.executable, "scripts/test_dashboard_all.py"], "Integrated Dashboard Tests"),
        run_command([sys.executable, "scripts/test_major_commands.py"], "Major Command Tests"),
        clean_test_snapshots(),
        check_git_status(),
    ]

    passed = sum(1 for item in checks if item)
    failed = len(checks) - passed

    print("")
    print("=" * 70)
    print("System Stability Summary")
    print("=" * 70)
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("")
        print("System stability check failed.")
        return 1

    print("")
    print("System stability check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
