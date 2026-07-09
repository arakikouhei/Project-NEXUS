import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nexus.dashboard.server import SAFE_COMMANDS, backend, STATIC_DIR


DANGEROUS_KEYWORDS = [
    "rm ",
    "rm -",
    "delete",
    "削除",
    "trash",
    "git commit",
    "git push",
    "git reset",
    "git clean",
    "subprocess",
    "os.system",
    "shell=True",
    "eval(",
    "exec(",
]

FORBIDDEN_COMMANDS = [
    "rm -rf /",
    "git push",
    "git commit",
    "ファイル削除",
    "ファイル編集",
    "バックアップ削除",
]


def check_safe_command_allowlist() -> bool:
    print("")
    print("=" * 70)
    print("Safe Command Allowlist")
    print("=" * 70)

    ok = True

    for command in SAFE_COMMANDS:
        lowered = command.lower()
        for keyword in DANGEROUS_KEYWORDS:
            if keyword.lower() in lowered:
                print(f"[FAIL] dangerous keyword in SAFE_COMMANDS: {command} / {keyword}")
                ok = False

    for command in FORBIDDEN_COMMANDS:
        result = backend.run_command(command)
        if result.get("ok") is not False:
            print(f"[FAIL] forbidden command was not blocked: {command}")
            ok = False
        else:
            print(f"[PASS] blocked: {command}")

    if ok:
        print("[PASS] Safe command allowlist")
    return ok


def check_frontend_buttons() -> bool:
    print("")
    print("=" * 70)
    print("Frontend Buttons")
    print("=" * 70)

    html_path = STATIC_DIR / "index.html"

    if not html_path.exists():
        print("[FAIL] index.html missing")
        return False

    html = html_path.read_text(encoding="utf-8")
    lowered = html.lower()

    ok = True

    forbidden_ui_texts = [
        "delete",
        "削除",
        "git commit",
        "git push",
        "rm -rf",
        "shell",
        "exec",
        "eval",
    ]

    for text in forbidden_ui_texts:
        if text in lowered:
            print(f"[FAIL] forbidden UI text found: {text}")
            ok = False

    required_texts = [
        "Safety: fixed safe commands only",
        "No shell execution",
        "No delete/edit actions",
        "Project NEXUS Dashboard",
        "Status Panel",
        "File Panel",
        "Production Panel",
    ]

    for text in required_texts:
        if text not in html:
            print(f"[FAIL] required safety/status text missing: {text}")
            ok = False
        else:
            print(f"[PASS] found: {text}")

    if ok:
        print("[PASS] Frontend safety text")
    return ok


def check_backend_source() -> bool:
    print("")
    print("=" * 70)
    print("Backend Source Safety")
    print("=" * 70)

    server_path = Path("nexus/dashboard/server.py")

    if not server_path.exists():
        print("[FAIL] server.py missing")
        return False

    source = server_path.read_text(encoding="utf-8")
    ok = True

    forbidden_source = [
        "shell=True",
        "os.system",
        "subprocess.run",
        "subprocess.Popen",
        "eval(",
        "exec(",
    ]

    for text in forbidden_source:
        if text in source:
            print(f"[FAIL] forbidden backend source text found: {text}")
            ok = False

    required_source = [
        "SAFE_COMMANDS",
        "Command is not allowed in Dashboard Backend v1.",
        "127.0.0.1",
        "run_command",
    ]

    for text in required_source:
        if text not in source:
            print(f"[FAIL] required backend safety text missing: {text}")
            ok = False
        else:
            print(f"[PASS] found: {text}")

    if ok:
        print("[PASS] Backend source safety")
    return ok


def check_cost_explanation() -> bool:
    print("")
    print("=" * 70)
    print("Cost Explanation")
    print("=" * 70)

    paths = [
        Path("nexus/tools/dashboard_launch.py"),
        Path("docs/DASHBOARD_LAUNCH_COMMAND_V1.md"),
    ]

    ok = True

    for path in paths:
        if not path.exists():
            print(f"[FAIL] missing file: {path}")
            ok = False
            continue

        text = path.read_text(encoding="utf-8")
        required = [
            "does not cost money",
            "127.0.0.1",
            "python3 -m nexus.dashboard.server",
        ]

        for item in required:
            if item not in text:
                print(f"[FAIL] {path} missing: {item}")
                ok = False
            else:
                print(f"[PASS] {path} contains: {item}")

    if ok:
        print("[PASS] Cost explanation")
    return ok


def main() -> int:
    print("Project NEXUS Dashboard Safety Review v1")

    checks = [
        check_safe_command_allowlist(),
        check_frontend_buttons(),
        check_backend_source(),
        check_cost_explanation(),
    ]

    passed = sum(1 for item in checks if item)
    failed = len(checks) - passed

    print("")
    print("=" * 70)
    print("Dashboard Safety Review Summary")
    print("=" * 70)
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    if failed:
        print("")
        print("Dashboard safety review failed.")
        return 1

    print("")
    print("Dashboard safety review passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
