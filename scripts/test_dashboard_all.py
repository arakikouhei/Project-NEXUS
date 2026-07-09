import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


TESTS = [
    "scripts/test_dashboard_backend.py",
    "scripts/test_dashboard_frontend.py",
    "scripts/test_dashboard_status_panel.py",
    "scripts/test_dashboard_file_panel.py",
    "scripts/test_dashboard_production_panel.py",
]


def run_test(path: str) -> bool:
    print("")
    print("=" * 70)
    print(f"Running: {path}")
    print("=" * 70)

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not existing_pythonpath
        else str(PROJECT_ROOT) + os.pathsep + existing_pythonpath
    )

    result = subprocess.run(
        [sys.executable, path],
        text=True,
        cwd=PROJECT_ROOT,
        env=env,
    )

    if result.returncode == 0:
        print(f"[PASS] {path}")
        return True

    print(f"[FAIL] {path}")
    return False


def main() -> int:
    print("Project NEXUS Integrated Dashboard Test v1")
    print("")

    missing = [path for path in TESTS if not Path(path).exists()]
    if missing:
        print("Missing test files:")
        for path in missing:
            print(f"- {path}")
        return 1

    passed = 0
    failed = 0

    for path in TESTS:
        if run_test(path):
            passed += 1
        else:
            failed += 1

    print("")
    print("=" * 70)
    print("Integrated Dashboard Test Summary")
    print("=" * 70)
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("")
        print("Some dashboard tests failed.")
        return 1

    print("")
    print("All dashboard tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
