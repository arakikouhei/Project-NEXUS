from pathlib import Path

from nexus.dashboard.server import backend, STATIC_DIR


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    status = backend.status()

    assert_true(status["ok"] is True, "backend status should be ok")
    assert_true(status.get("project_version") == "0.7.0-dev", "project version mismatch")
    assert_true(
        status.get("roadmap_stage") == "v0.7 file / production support / UI prep",
        "roadmap stage mismatch",
    )
    assert_true(status.get("safe_command_count", 0) >= 18, "safe command count too small")
    assert_true("Current Stage" in status.get("current_position", ""), "current position missing Current Stage")

    html_path = STATIC_DIR / "index.html"
    assert_true(html_path.exists(), "index.html should exist")

    html = html_path.read_text(encoding="utf-8")
    required = [
        "Status Panel",
        "Project Version",
        "Roadmap Stage",
        "Safe Commands",
        "Backend",
        "project-version",
        "roadmap-stage",
        "safe-command-count",
        "backend-state",
    ]

    for item in required:
        assert_true(item in html, f"missing status panel text: {item}")

    print("Dashboard Status Panel tests passed")
    print("project_version:", status.get("project_version"))
    print("roadmap_stage:", status.get("roadmap_stage"))
    print("safe_command_count:", status.get("safe_command_count"))


if __name__ == "__main__":
    main()
